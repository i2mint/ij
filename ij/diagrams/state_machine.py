"""State Machine diagram support.

Provides tools for creating and rendering finite state machines.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set


class StateType(Enum):
    """Type of state."""

    NORMAL = "normal"
    INITIAL = "initial"
    FINAL = "final"


@dataclass
class State:
    """A state in a state machine."""

    name: str
    state_type: StateType = StateType.NORMAL
    on_enter: Optional[str] = None
    on_exit: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class Transition:
    """A transition between states."""

    from_state: str
    to_state: str
    trigger: str
    condition: Optional[str] = None
    action: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class StateMachine:
    """Finite State Machine diagram."""

    def __init__(
        self, name: str = "StateMachine", initial_state: Optional[str] = None
    ):
        """Initialize state machine.

        Args:
            name: State machine name
            initial_state: Name of initial state
        """
        self.name = name
        self.initial_state = initial_state
        self.states: List[State] = []
        self.transitions: List[Transition] = []

    def add_state(
        self,
        name: str,
        state_type: StateType = StateType.NORMAL,
        on_enter: Optional[str] = None,
        on_exit: Optional[str] = None,
    ):
        """Add a state to the machine.

        Args:
            name: State name
            state_type: Type of state (NORMAL, INITIAL, FINAL)
            on_enter: Action to perform on entering state
            on_exit: Action to perform on exiting state
        """
        state = State(
            name=name, state_type=state_type, on_enter=on_enter, on_exit=on_exit
        )
        self.states.append(state)

        # Set as initial if specified
        if state_type == StateType.INITIAL and self.initial_state is None:
            self.initial_state = name

    def add_transition(
        self,
        from_state: str,
        trigger: str,
        to_state: str,
        condition: Optional[str] = None,
        action: Optional[str] = None,
    ):
        """Add a transition between states.

        Args:
            from_state: Source state name
            trigger: Event that triggers the transition
            to_state: Target state name
            condition: Optional condition guard
            action: Optional action to perform during transition
        """
        transition = Transition(
            from_state=from_state,
            to_state=to_state,
            trigger=trigger,
            condition=condition,
            action=action,
        )
        self.transitions.append(transition)

    def to_mermaid(self) -> str:
        """Render state machine as Mermaid state diagram.

        Returns:
            Mermaid state diagram syntax
        """
        lines = ["stateDiagram-v2"]

        # Add initial state marker
        if self.initial_state:
            lines.append(f"    [*] --> {self.initial_state}")

        # Add state definitions with actions
        for state in self.states:
            if state.on_enter or state.on_exit:
                lines.append(f"    state {state.name} {{")
                if state.on_enter:
                    lines.append(f"        entry: {state.on_enter}")
                if state.on_exit:
                    lines.append(f"        exit: {state.on_exit}")
                lines.append("    }")

        # Add transitions
        for trans in self.transitions:
            # Build label
            label_parts = [trans.trigger]
            if trans.condition:
                label_parts.append(f"[{trans.condition}]")
            if trans.action:
                label_parts.append(f"/ {trans.action}")

            label = " ".join(label_parts)
            lines.append(f"    {trans.from_state} --> {trans.to_state}: {label}")

        # Add final state markers
        for state in self.states:
            if state.state_type == StateType.FINAL:
                lines.append(f"    {state.name} --> [*]")

        return "\n".join(lines)

    def to_plantuml(self) -> str:
        """Render state machine as PlantUML state diagram.

        Returns:
            PlantUML syntax
        """
        lines = ["@startuml"]
        lines.append(f"title {self.name}")

        # Add initial state
        if self.initial_state:
            lines.append(f"[*] --> {self.initial_state}")

        # Add states with actions
        for state in self.states:
            if state.on_enter or state.on_exit:
                lines.append(f"state {state.name} {{")
                if state.on_enter:
                    lines.append(f"  {state.name} : entry / {state.on_enter}")
                if state.on_exit:
                    lines.append(f"  {state.name} : exit / {state.on_exit}")
                lines.append("}")

        # Add transitions
        for trans in self.transitions:
            label_parts = [trans.trigger]
            if trans.condition:
                label_parts.append(f"[{trans.condition}]")
            if trans.action:
                label_parts.append(f"/ {trans.action}")

            label = " ".join(label_parts)
            lines.append(f"{trans.from_state} --> {trans.to_state} : {label}")

        # Add final states
        for state in self.states:
            if state.state_type == StateType.FINAL:
                lines.append(f"{state.name} --> [*]")

        lines.append("@enduml")
        return "\n".join(lines)

    def to_d2(self) -> str:
        """Render state machine as D2 diagram.

        Returns:
            D2 syntax
        """
        lines = [f"# {self.name}", ""]

        # Add states
        for state in self.states:
            shape = "oval" if state.state_type != StateType.NORMAL else "rectangle"
            lines.append(f"{state.name}: {{")
            lines.append(f"  shape: {shape}")

            if state.on_enter:
                lines.append(f"  entry: {state.on_enter}")
            if state.on_exit:
                lines.append(f"  exit: {state.on_exit}")

            lines.append("}")

        # Add transitions
        for trans in self.transitions:
            label_parts = [trans.trigger]
            if trans.condition:
                label_parts.append(f"[{trans.condition}]")
            if trans.action:
                label_parts.append(f"/ {trans.action}")

            label = " ".join(label_parts)
            lines.append(f'{trans.from_state} -> {trans.to_state}: "{label}"')

        return "\n".join(lines)

    def validate(self) -> List[str]:
        """Validate state machine for common issues.

        Returns:
            List of validation issues (empty if valid)
        """
        issues = []

        # Check for initial state
        if not self.initial_state:
            issues.append("No initial state defined")

        # Check for unreachable states
        reachable = self._get_reachable_states()
        all_states = {s.name for s in self.states}
        unreachable = all_states - reachable

        if unreachable:
            issues.append(f"Unreachable states: {', '.join(unreachable)}")

        # Check for undefined states in transitions
        for trans in self.transitions:
            if trans.from_state not in all_states:
                issues.append(
                    f"Transition from undefined state: {trans.from_state}"
                )
            if trans.to_state not in all_states:
                issues.append(f"Transition to undefined state: {trans.to_state}")

        # Check for duplicate transitions
        trans_sigs = set()
        for trans in self.transitions:
            sig = (trans.from_state, trans.trigger, trans.to_state)
            if sig in trans_sigs:
                issues.append(
                    f"Duplicate transition: {trans.from_state} --{trans.trigger}--> {trans.to_state}"
                )
            trans_sigs.add(sig)

        return issues

    def _get_reachable_states(self) -> Set[str]:
        """Get all states reachable from initial state."""
        if not self.initial_state:
            return set()

        reachable = {self.initial_state}
        changed = True

        while changed:
            changed = False
            for trans in self.transitions:
                if trans.from_state in reachable and trans.to_state not in reachable:
                    reachable.add(trans.to_state)
                    changed = True

        return reachable

    def get_triggers_from_state(self, state_name: str) -> List[str]:
        """Get all possible triggers from a given state.

        Args:
            state_name: State name

        Returns:
            List of trigger names
        """
        return [t.trigger for t in self.transitions if t.from_state == state_name]

    def simulate(self, initial_state: str, events: List[str]) -> List[str]:
        """Simulate state machine execution.

        Args:
            initial_state: Starting state
            events: List of trigger events

        Returns:
            List of states visited (including initial)
        """
        current_state = initial_state
        path = [current_state]

        for event in events:
            # Find matching transition
            next_state = None
            for trans in self.transitions:
                if trans.from_state == current_state and trans.trigger == event:
                    next_state = trans.to_state
                    break

            if next_state:
                current_state = next_state
                path.append(current_state)
            else:
                # Invalid transition
                path.append(f"<error: no transition for {event} from {current_state}>")
                break

        return path


class StateMachineBuilder:
    """Builder for creating state machines from various sources."""

    @staticmethod
    def from_dict(spec: Dict) -> StateMachine:
        """Create state machine from dictionary specification.

        Args:
            spec: Dictionary describing states and transitions

        Returns:
            StateMachine instance

        Example:
            >>> spec = {
            ...     "name": "DoorLock",
            ...     "initial": "locked",
            ...     "states": {
            ...         "locked": {"type": "initial"},
            ...         "unlocked": {},
            ...         "error": {"type": "final"}
            ...     },
            ...     "transitions": [
            ...         {"from": "locked", "trigger": "unlock", "to": "unlocked"},
            ...         {"from": "unlocked", "trigger": "lock", "to": "locked"}
            ...     ]
            ... }
            >>> sm = StateMachineBuilder.from_dict(spec)
        """
        name = spec.get("name", "StateMachine")
        initial = spec.get("initial")

        sm = StateMachine(name=name, initial_state=initial)

        # Add states
        for state_name, state_props in spec.get("states", {}).items():
            state_type_str = state_props.get("type", "normal")
            state_type = StateType(state_type_str)

            sm.add_state(
                name=state_name,
                state_type=state_type,
                on_enter=state_props.get("on_enter"),
                on_exit=state_props.get("on_exit"),
            )

        # Add transitions
        for trans_def in spec.get("transitions", []):
            sm.add_transition(
                from_state=trans_def["from"],
                trigger=trans_def["trigger"],
                to_state=trans_def["to"],
                condition=trans_def.get("condition"),
                action=trans_def.get("action"),
            )

        return sm

    @staticmethod
    def from_code(code: str) -> StateMachine:
        """Extract state machine from simple DSL.

        Args:
            code: State machine DSL code

        Returns:
            StateMachine instance

        Example:
            >>> code = '''
            ... INITIAL locked
            ... STATE unlocked
            ... STATE error FINAL
            ...
            ... locked --unlock--> unlocked
            ... unlocked --lock--> locked
            ... '''
            >>> sm = StateMachineBuilder.from_code(code)
        """
        sm = StateMachine()

        lines = [line.strip() for line in code.split("\n") if line.strip()]

        for line in lines:
            # Parse STATE declarations
            if line.upper().startswith("STATE "):
                parts = line.split()
                state_name = parts[1]
                state_type = StateType.FINAL if "FINAL" in line.upper() else StateType.NORMAL
                sm.add_state(state_name, state_type=state_type)

            elif line.upper().startswith("INITIAL "):
                state_name = line.split()[1]
                sm.add_state(state_name, state_type=StateType.INITIAL)
                sm.initial_state = state_name

            # Parse transitions: from --trigger--> to
            elif "--" in line and "-->" in line:
                import re

                match = re.match(r"(\w+)\s+--(\w+)-->\s+(\w+)", line)
                if match:
                    from_state, trigger, to_state = match.groups()
                    sm.add_transition(from_state, trigger, to_state)

        return sm
