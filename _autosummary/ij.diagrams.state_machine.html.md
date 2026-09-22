# ij.diagrams.state_machine

State Machine diagram support.

Provides tools for creating and rendering finite state machines.

### Classes

| [`State`](#ij.diagrams.state_machine.State)(name[, state_type, on_enter, on_exit, ...])   | A state in a state machine.                               |
|------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| [`StateMachine`](#ij.diagrams.state_machine.StateMachine)([name, initial_state])                 | Finite State Machine diagram.                             |
| [`StateMachineBuilder`](#ij.diagrams.state_machine.StateMachineBuilder)()                               | Builder for creating state machines from various sources. |
| [`StateType`](#ij.diagrams.state_machine.StateType)(\*values)                                 | Type of state.                                            |
| [`Transition`](#ij.diagrams.state_machine.Transition)(from_state, to_state, trigger[, ...])    | A transition between states.                              |

### *class* ij.diagrams.state_machine.State(name, state_type=StateType.NORMAL, on_enter=None, on_exit=None, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A state in a state machine.

### *class* ij.diagrams.state_machine.StateMachine(name='StateMachine', initial_state=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Finite State Machine diagram.

#### add_state(name, state_type=StateType.NORMAL, on_enter=None, on_exit=None)

Add a state to the machine.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – State name
  * **state_type** ([`StateType`](#ij.diagrams.state_machine.StateType)) – Type of state (NORMAL, INITIAL, FINAL)
  * **on_enter** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Action to perform on entering state
  * **on_exit** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Action to perform on exiting state

#### add_transition(from_state, trigger, to_state, condition=None, action=None)

Add a transition between states.

* **Parameters:**
  * **from_state** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Source state name
  * **trigger** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Event that triggers the transition
  * **to_state** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Target state name
  * **condition** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional condition guard
  * **action** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional action to perform during transition

#### get_triggers_from_state(state_name)

Get all possible triggers from a given state.

* **Parameters:**
  **state_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – State name
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of trigger names

#### simulate(initial_state, events)

Simulate state machine execution.

* **Parameters:**
  * **initial_state** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Starting state
  * **events** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – List of trigger events
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of states visited (including initial)

#### to_d2()

Render state machine as D2 diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  D2 syntax

#### to_mermaid()

Render state machine as Mermaid state diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid state diagram syntax

#### to_plantuml()

Render state machine as PlantUML state diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  PlantUML syntax

#### validate()

Validate state machine for common issues.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of validation issues (empty if valid)

### *class* ij.diagrams.state_machine.StateMachineBuilder

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Builder for creating state machines from various sources.

#### *static* from_code(code)

Extract state machine from simple DSL.

* **Parameters:**
  **code** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – State machine DSL code
* **Return type:**
  [`StateMachine`](#ij.diagrams.state_machine.StateMachine)
* **Returns:**
  StateMachine instance

### Example

```pycon
>>> code = '''
... INITIAL locked
... STATE unlocked
... STATE error FINAL
...
... locked --unlock--> unlocked
... unlocked --lock--> locked
... '''
>>> sm = StateMachineBuilder.from_code(code)
```

#### *static* from_dict(spec)

Create state machine from dictionary specification.

* **Parameters:**
  **spec** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)) – Dictionary describing states and transitions
* **Return type:**
  [`StateMachine`](#ij.diagrams.state_machine.StateMachine)
* **Returns:**
  StateMachine instance

### Example

```pycon
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
```

### *class* ij.diagrams.state_machine.StateType(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Type of state.

### *class* ij.diagrams.state_machine.Transition(from_state, to_state, trigger, condition=None, action=None, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A transition between states.
