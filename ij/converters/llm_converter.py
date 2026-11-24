"""AI/LLM-based text to diagram converter.

Uses OpenAI API for intelligent natural language understanding and
diagram generation. Follows research recommendations for AI-powered
diagram generation (10-20x faster initial drafts).
"""

import json
import os
from typing import Dict, List, Optional

try:
    import openai
except ImportError:
    openai = None

from ..core import DiagramIR, Edge, EdgeType, Node, NodeType
from ..parsers import MermaidParser


class UnusableDiagramError(ValueError):
    """Model output that holds no usable diagram.

    Attributes:
        raw: The model's output, as returned
        unparsed_lines: The lines of it the Mermaid parser could not read
    """

    def __init__(self, message: str, *, raw: str, unparsed_lines: List[str]):
        super().__init__(message)
        self.raw = raw
        self.unparsed_lines = list(unparsed_lines)


class LLMConverter:
    """AI-powered text to diagram converter using LLMs.

    Uses OpenAI API with carefully crafted prompts to generate diagrams
    from natural language descriptions. Supports iterative refinement.
    """

    SYSTEM_PROMPT = """You are an expert at converting natural language descriptions into Mermaid flowchart diagrams.

When given a description, create a clear, well-structured Mermaid flowchart that accurately represents the process or system described.

Guidelines:
1. Use appropriate node types:
   - ([...]) for start/end nodes
   - [...] for process steps
   - {...} for decisions
   - [(...)] for data/storage
2. Use meaningful node IDs (e.g., 'start', 'check_user', 'save_data')
3. Add clear labels to decision edges (e.g., |Yes|, |No|)
4. Keep the diagram focused and avoid unnecessary complexity
5. Use flowchart TD (top-down) or LR (left-right) as appropriate

Output ONLY the Mermaid code, no explanations or markdown code blocks."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.3,
        *,
        max_retries: int = 0,
    ):
        """Initialize LLM converter.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (gpt-4o-mini is cheap and effective)
            temperature: Sampling temperature (lower = more deterministic)
            max_retries: How many more times to ask the model when its output
                holds no usable diagram, each time showing it the error and the
                lines the parser could not read. Each retry is a paid call, so
                the default is 0: an unusable output raises at once.
        """
        if max_retries < 0:
            raise ValueError(f"max_retries must be 0 or more, got {max_retries!r}")
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries

        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        if openai is None:
            raise ImportError(
                "OpenAI library required for LLM conversion. "
                "Install with: pip install openai"
            )

        self.client = openai.OpenAI(api_key=self.api_key)

    def convert(
        self, text: str, title: Optional[str] = None, direction: str = "TD"
    ) -> DiagramIR:
        """Convert natural language to DiagramIR using LLM.

        Args:
            text: Natural language description
            title: Optional diagram title
            direction: Diagram direction (TD, LR, etc.)

        Returns:
            DiagramIR representation

        Example:
            >>> converter = LLMConverter()  # doctest: +SKIP
            >>> diagram = converter.convert(  # doctest: +SKIP
            ...     "A user logs into the system. If authentication succeeds, "
            ...     "they see the dashboard. Otherwise, they see an error message."
            ... )
        """
        # Build user prompt
        user_prompt = f"Create a Mermaid flowchart for:\n\n{text}"
        if title:
            user_prompt += f"\n\nTitle: {title}"
        if direction != "TD":
            user_prompt += f"\n\nUse direction: {direction}"

        # Call the model, and parse what it returns to DiagramIR
        diagram = self._generate_diagram(user_prompt)

        # Add title if provided
        if title and "title" not in diagram.metadata:
            diagram.metadata["title"] = title

        return diagram

    def refine(
        self, diagram: DiagramIR, feedback: str, current_mermaid: str
    ) -> DiagramIR:
        """Refine an existing diagram based on feedback.

        Args:
            diagram: Current diagram
            feedback: User feedback/instructions
            current_mermaid: Current Mermaid representation

        Returns:
            Refined DiagramIR

        Example:
            >>> diagram = converter.convert("User login process")  # doctest: +SKIP
            >>> from ij.renderers import MermaidRenderer
            >>> mermaid = MermaidRenderer().render(diagram)  # doctest: +SKIP
            >>> refined = converter.refine(  # doctest: +SKIP
            ...     diagram,
            ...     "Add a step for password reset if login fails",
            ...     mermaid
            ... )
        """
        user_prompt = f"""Current diagram:
```mermaid
{current_mermaid}
```

Please modify it based on this feedback:
{feedback}

Output the updated Mermaid code."""

        # Generate the refined version, parsed back to DiagramIR
        refined_diagram = self._generate_diagram(user_prompt)

        # Preserve metadata
        refined_diagram.metadata.update(diagram.metadata)

        return refined_diagram

    def _parse_mermaid(self, mermaid_code: str) -> DiagramIR:
        """Parse model-generated Mermaid, failing loudly on unusable output.

        Model output is not trustworthy -- it drifts between model versions.
        Parsing it without checking turns that drift into a silently wrong
        diagram, so lines the parser could not read are surfaced by
        ``MermaidParser`` (as a ``MermaidParseWarning``) and output that yields
        no usable diagram at all is refused here rather than returned empty.

        Args:
            mermaid_code: Mermaid code as returned by the model

        Returns:
            DiagramIR parsed from ``mermaid_code``

        Raises:
            UnusableDiagramError: If the output holds no valid diagram (a
                ``ValueError``, carrying the raw output and unparsed lines)
        """
        parser = MermaidParser()
        diagram = parser.parse(mermaid_code)

        if not diagram.nodes or not diagram.validate():
            raise UnusableDiagramError(
                f"{self.model} did not return a usable Mermaid diagram.\n"
                f"Raw model output:\n{mermaid_code}",
                raw=mermaid_code,
                unparsed_lines=parser.unparsed_lines,
            )

        return diagram

    def _generate_diagram(self, user_prompt: str) -> DiagramIR:
        """Ask the model for a diagram, retrying up to ``max_retries`` times.

        A retry repeats the request with the unusable output, the error and
        the lines the parser could not read appended, so the model repairs
        its answer rather than drawing again from scratch.
        """
        prompt = user_prompt
        for attempt in range(self.max_retries + 1):
            mermaid_code = self._generate_mermaid(prompt)
            try:
                return self._parse_mermaid(mermaid_code)
            except UnusableDiagramError as error:
                if attempt == self.max_retries:
                    raise
                prompt = self._repair_prompt(user_prompt, error)
        raise AssertionError("unreachable: the last attempt returns or raises")

    @staticmethod
    def _repair_prompt(user_prompt: str, error: "UnusableDiagramError") -> str:
        """The original request, plus what was wrong with the last answer."""
        unreadable = "\n".join(error.unparsed_lines) or "(none: no node or edge was found)"
        return (
            f"{user_prompt}\n\n"
            "Your previous answer was not a usable Mermaid flowchart:\n"
            f"```\n{error.raw}\n```\n"
            f"Lines that could not be parsed:\n{unreadable}\n\n"
            "Answer again with valid Mermaid flowchart code only."
        )

    def _generate_mermaid(self, user_prompt: str) -> str:
        """Call OpenAI API to generate Mermaid code.

        Args:
            user_prompt: User's prompt

        Returns:
            Generated Mermaid code
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.temperature,
            max_tokens=1000,
        )

        mermaid_code = response.choices[0].message.content.strip()

        # Clean up if wrapped in code blocks
        if mermaid_code.startswith("```"):
            lines = mermaid_code.split("\n")
            # Remove first line (```mermaid or ```) and last line (```)
            mermaid_code = "\n".join(lines[1:-1])

        return mermaid_code

    def convert_with_examples(
        self, text: str, examples: List[Dict[str, str]], title: Optional[str] = None
    ) -> DiagramIR:
        """Convert with few-shot examples for better quality.

        Args:
            text: Natural language description
            examples: List of {"description": "...", "mermaid": "..."} examples
            title: Optional diagram title

        Returns:
            DiagramIR representation
        """
        # Build few-shot prompt
        examples_text = "\n\n".join(
            [
                f"Example {i + 1}:\nDescription: {ex['description']}\n\nMermaid:\n{ex['mermaid']}"
                for i, ex in enumerate(examples)
            ]
        )

        user_prompt = f"""{examples_text}

Now create a diagram for:
{text}"""

        if title:
            user_prompt += f"\n\nTitle: {title}"

        diagram = self._generate_diagram(user_prompt)

        if title:
            diagram.metadata["title"] = title

        return diagram
