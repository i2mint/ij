# ij.diagrams

Advanced diagram types.

### Classes

| [`ERDiagram`](#ij.diagrams.ERDiagram)([title])                                | Entity-Relationship Diagram.                    |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------|
| [`Entity`](#ij.diagrams.Entity)(name[, fields, metadata])                  | An entity in an ERD.                            |
| [`Field`](#ij.diagrams.Field)(name, type[, primary_key, ...])             | A field in an entity.                           |
| [`Relationship`](#ij.diagrams.Relationship)(from_entity, to_entity, cardinality) | A relationship between entities.                |
| [`Cardinality`](#ij.diagrams.Cardinality)(\*values)                             | Relationship cardinality.                       |
| [`ERDBuilder`](#ij.diagrams.ERDBuilder)()                                      | Builder for creating ERDs from various sources. |
| [`StateMachine`](#ij.diagrams.StateMachine)([name, initial_state])               | Finite State Machine diagram.                   |
| [`State`](#ij.diagrams.State)(name[, state_type, on_enter, on_exit, ...]) | A state in a state machine.                     |
| [`Transition`](#ij.diagrams.Transition)(from_state, to_state, trigger[, ...])  | A transition between states.                    |

### *class* ij.diagrams.Cardinality(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Relationship cardinality.

### *class* ij.diagrams.ERDBuilder

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Builder for creating ERDs from various sources.

#### *static* from_dict(schema)

Create ERD from dictionary schema.

* **Parameters:**
  **schema** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)) – Dictionary describing entities and relationships
* **Return type:**
  [`ERDiagram`](ij.diagrams.erd.html.md#ij.diagrams.erd.ERDiagram)
* **Returns:**
  ERDiagram instance

### Example

```pycon
>>> schema = {
...     "entities": {
...         "User": ["id:int:PK", "name:string", "email:string:unique"],
...         "Post": ["id:int:PK", "user_id:int:FK->User", "title:string"]
...     },
...     "relationships": [
...         {"from": "User", "to": "Post", "cardinality": "1:N"}
...     ]
... }
>>> erd = ERDBuilder.from_dict(schema)
```

#### *static* from_sql_ddl(ddl)

Create ERD from SQL DDL statements (basic support).

* **Parameters:**
  **ddl** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – SQL CREATE TABLE statements
* **Return type:**
  [`ERDiagram`](ij.diagrams.erd.html.md#ij.diagrams.erd.ERDiagram)
* **Returns:**
  ERDiagram instance

### *class* ij.diagrams.ERDiagram(title=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Entity-Relationship Diagram.

#### add_entity(entity)

Add an entity to the diagram.

#### add_relationship(from_entity, to_entity, cardinality, label=None)

Add a relationship between entities.

#### to_d2()

Render ERD as D2 diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  D2 syntax

#### to_mermaid()

Render ERD as Mermaid ER diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Mermaid ER diagram syntax

#### to_plantuml()

Render ERD as PlantUML class diagram.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  PlantUML syntax

### *class* ij.diagrams.Entity(name, fields=<factory>, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An entity in an ERD.

#### add_field(name, field_type, primary_key=False, foreign_key=None, nullable=True, unique=False)

Add a field to the entity.

### *class* ij.diagrams.Field(name, type, primary_key=False, foreign_key=None, nullable=True, unique=False)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A field in an entity.

### *class* ij.diagrams.Relationship(from_entity, to_entity, cardinality, label=None, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A relationship between entities.

### *class* ij.diagrams.State(name, state_type=StateType.NORMAL, on_enter=None, on_exit=None, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A state in a state machine.

### *class* ij.diagrams.StateMachine(name='StateMachine', initial_state=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Finite State Machine diagram.

#### add_state(name, state_type=StateType.NORMAL, on_enter=None, on_exit=None)

Add a state to the machine.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – State name
  * **state_type** ([`StateType`](ij.diagrams.state_machine.html.md#ij.diagrams.state_machine.StateType)) – Type of state (NORMAL, INITIAL, FINAL)
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

### *class* ij.diagrams.Transition(from_state, to_state, trigger, condition=None, action=None, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A transition between states.

### Modules

| [`erd`](ij.diagrams.erd.html.md#module-ij.diagrams.erd)                     | Entity-Relationship Diagram support.   |
|-------------------------------------------------------------------------------------------------|----------------------------------------|
| [`state_machine`](ij.diagrams.state_machine.html.md#module-ij.diagrams.state_machine) | State Machine diagram support.         |
