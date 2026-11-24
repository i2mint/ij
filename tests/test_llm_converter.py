"""Tests for LLM-based converter.

Tests use mocks by default. The live-API tests are opt-in: they run only when
IJ_RUN_REAL_API_TESTS is set, since they are non-hermetic, need network, cost
money, and are fragile to model drift. They also need OPENAI_API_KEY.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

# Skip all tests in this file if openai is not installed
pytest.importorskip("openai")

from ij.converters.llm_converter import LLMConverter
from ij.core import DiagramIR


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = """flowchart TD
    start([Start])
    check{Authenticated?}
    dashboard[Show Dashboard]
    login[Show Login]
    start --> check
    check -->|Yes| dashboard
    check -->|No| login"""

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    return mock_client


def test_llm_converter_init_without_key():
    """Test initialization fails without API key."""
    # Clear env var if present
    old_key = os.environ.pop("OPENAI_API_KEY", None)

    try:
        with pytest.raises(ValueError, match="OpenAI API key required"):
            LLMConverter()
    finally:
        if old_key:
            os.environ["OPENAI_API_KEY"] = old_key


def test_llm_converter_init_with_key():
    """Test initialization with API key."""
    converter = LLMConverter(api_key="test-key")
    assert converter.api_key == "test-key"
    assert converter.model == "gpt-4o-mini"
    assert converter.temperature == 0.3


@patch("ij.converters.llm_converter.openai")
def test_llm_converter_convert_mock(mock_openai, mock_openai_client):
    """Test conversion with mocked OpenAI API."""
    mock_openai.OpenAI.return_value = mock_openai_client

    converter = LLMConverter(api_key="test-key")
    diagram = converter.convert("User authentication process")

    # Verify API was called
    assert mock_openai_client.chat.completions.create.called

    # Verify diagram was created
    assert isinstance(diagram, DiagramIR)
    assert len(diagram.nodes) > 0
    assert len(diagram.edges) > 0
    assert diagram.validate()


@patch("ij.converters.llm_converter.openai")
def test_llm_converter_with_title(mock_openai, mock_openai_client):
    """Test conversion with title."""
    mock_openai.OpenAI.return_value = mock_openai_client

    converter = LLMConverter(api_key="test-key")
    diagram = converter.convert("User login", title="Login Flow")

    assert diagram.metadata.get("title") == "Login Flow"


@patch("ij.converters.llm_converter.openai")
def test_llm_converter_refine(mock_openai, mock_openai_client):
    """Test diagram refinement."""
    mock_openai.OpenAI.return_value = mock_openai_client

    converter = LLMConverter(api_key="test-key")
    diagram = converter.convert("Simple process")

    # Mock refined response
    mock_openai_client.chat.completions.create.return_value.choices[
        0
    ].message.content = """flowchart TD
    start([Start])
    process[Process]
    extra[Extra Step]
    end([End])
    start --> process
    process --> extra
    extra --> end"""

    from ij.renderers import MermaidRenderer

    mermaid = MermaidRenderer().render(diagram)
    refined = converter.refine(diagram, "Add an extra step", mermaid)

    assert isinstance(refined, DiagramIR)
    assert refined.validate()


@patch("ij.converters.llm_converter.openai")
def test_llm_converter_code_block_cleanup(mock_openai):
    """Test that code blocks are properly cleaned up."""
    # Mock response with code blocks
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = """```mermaid
flowchart TD
    A[Start] --> B[End]
```"""

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.OpenAI.return_value = mock_client

    converter = LLMConverter(api_key="test-key")
    diagram = converter.convert("Simple flow")

    assert isinstance(diagram, DiagramIR)
    assert diagram.validate()


@patch("ij.converters.llm_converter.openai")
def test_llm_converter_with_examples(mock_openai, mock_openai_client):
    """Test few-shot learning with examples."""
    mock_openai.OpenAI.return_value = mock_openai_client

    converter = LLMConverter(api_key="test-key")
    examples = [
        {
            "description": "Login process",
            "mermaid": "flowchart TD\n    A[Start] --> B[Login]",
        }
    ]

    diagram = converter.convert_with_examples("Signup process", examples)

    assert isinstance(diagram, DiagramIR)
    assert diagram.validate()


def _mock_openai_returning(mermaid_code):
    """Build a mocked openai module whose completion returns mermaid_code."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = mermaid_code

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    mock_openai = MagicMock()
    mock_openai.OpenAI.return_value = mock_client
    return mock_openai


def test_llm_converter_survives_edge_label_drift():
    """Test model drift in edge-label syntax no longer costs the decision node.

    Hermetic stand-in for test_llm_converter_real_api_with_decision: this is
    the output gpt-4o-mini actually produced, with the invalid
    `check_user --|Yes|--> show_dashboard` edge-label spelling. It used to yield
    zero DECISION nodes, silently.
    """
    drifted_output = """flowchart TD
    start([Start]) --> check_user{Is user authenticated?}
    check_user --|Yes|--> show_dashboard([Show Dashboard])
    check_user --|No|--> show_login([Show Login])
    show_dashboard --> end([End])
    show_login --> end([End])"""

    from ij.core import NodeType

    with patch(
        "ij.converters.llm_converter.openai", _mock_openai_returning(drifted_output)
    ):
        converter = LLMConverter(api_key="test-key")
        diagram = converter.convert(
            "Check if user is authenticated. If yes, show dashboard. If no, show login."
        )

    decision_nodes = [n for n in diagram.nodes if n.node_type == NodeType.DECISION]
    assert len(decision_nodes) >= 1
    assert len(diagram.edges) == 5
    assert diagram.validate()


def test_llm_converter_rejects_unusable_output():
    """Test output holding no diagram raises instead of returning an empty one."""
    with patch(
        "ij.converters.llm_converter.openai",
        _mock_openai_returning("I'm sorry, I can't help with that request."),
    ):
        converter = LLMConverter(api_key="test-key")
        with pytest.raises(ValueError, match="did not return a usable Mermaid diagram"):
            converter.convert("Anything")


# Optional real API tests - only run if IJ_RUN_REAL_API_TESTS is set
@pytest.mark.skipif(
    not os.environ.get("IJ_RUN_REAL_API_TESTS"),
    reason="IJ_RUN_REAL_API_TESTS not set - skipping live-API tests",
)
def test_llm_converter_real_api_simple():
    """Test with real OpenAI API - simple case.

    This test only runs if the IJ_RUN_REAL_API_TESTS environment variable is
    set (and OPENAI_API_KEY with it).
    Uses gpt-4o-mini which is cheap (~$0.00015 per request).
    """
    converter = LLMConverter(model="gpt-4o-mini", temperature=0.1)
    diagram = converter.convert("A simple two-step process")

    # Verify basic structure
    assert isinstance(diagram, DiagramIR)
    assert len(diagram.nodes) >= 2
    assert len(diagram.edges) >= 1
    assert diagram.validate()


@pytest.mark.skipif(
    not os.environ.get("IJ_RUN_REAL_API_TESTS"),
    reason="IJ_RUN_REAL_API_TESTS not set - skipping live-API tests",
)
def test_llm_converter_real_api_with_decision():
    """Test with real OpenAI API - decision logic.

    This test only runs if the IJ_RUN_REAL_API_TESTS environment variable is
    set (and OPENAI_API_KEY with it). See
    test_llm_converter_survives_edge_label_drift for the hermetic equivalent.
    """
    converter = LLMConverter(model="gpt-4o-mini", temperature=0.1)
    diagram = converter.convert(
        "Check if user is authenticated. If yes, show dashboard. If no, show login."
    )

    # Should have decision node
    from ij.core import NodeType

    decision_nodes = [n for n in diagram.nodes if n.node_type == NodeType.DECISION]
    assert len(decision_nodes) >= 1
    assert diagram.validate()


# --- validate-then-retry (#6) -------------------------------------------------

GOOD = "flowchart TD\n    a[Start] --> b[End]"
BAD = "this is not mermaid at all"


def _converter_answering(answers, **kwargs):
    """An LLMConverter whose model returns ``answers`` in turn (no network)."""
    converter = LLMConverter(api_key="test-key", **kwargs)
    responses = []
    for text in answers:
        r = MagicMock()
        r.choices = [MagicMock()]
        r.choices[0].message.content = text
        responses.append(r)
    converter.client = MagicMock()
    converter.client.chat.completions.create.side_effect = responses
    return converter


def test_by_default_an_unusable_answer_raises_after_one_call():
    from ij.converters.llm_converter import UnusableDiagramError

    converter = _converter_answering([BAD, GOOD])
    with pytest.warns(Warning), pytest.raises(UnusableDiagramError) as info:
        converter.convert("a start and an end")
    assert converter.client.chat.completions.create.call_count == 1
    assert info.value.raw == BAD and info.value.unparsed_lines == [BAD]
    assert isinstance(info.value, ValueError)  # what callers caught before


def test_a_retry_shows_the_model_its_unparsed_lines_and_takes_the_repair():
    converter = _converter_answering([BAD, GOOD], max_retries=2)
    with pytest.warns(Warning):
        diagram = converter.convert("a start and an end")
    assert {n.id for n in diagram.nodes} == {"a", "b"}
    calls = converter.client.chat.completions.create.call_args_list
    assert len(calls) == 2
    repair = calls[1].kwargs["messages"][-1]["content"]
    assert repair.startswith("Create a Mermaid flowchart for:\n\na start and an end")
    assert BAD in repair and "could not be parsed" in repair


def test_retries_stop_at_the_budget():
    from ij.converters.llm_converter import UnusableDiagramError

    converter = _converter_answering([BAD, BAD, BAD, GOOD], max_retries=2)
    with pytest.warns(Warning), pytest.raises(UnusableDiagramError):
        converter.convert("x")
    assert converter.client.chat.completions.create.call_count == 3


def test_a_negative_retry_budget_is_refused():
    with pytest.raises(ValueError, match="max_retries"):
        LLMConverter(api_key="test-key", max_retries=-1)
