# ij.diagrams.erd

Entity-Relationship Diagram support.

Provides tools for creating and rendering ERDs.

### Classes

| [`Cardinality`](#ij.diagrams.erd.Cardinality)(\*values)                             | Relationship cardinality.                       |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------|
| [`ERDBuilder`](#ij.diagrams.erd.ERDBuilder)()                                      | Builder for creating ERDs from various sources. |
| [`ERDiagram`](#ij.diagrams.erd.ERDiagram)([title])                                | Entity-Relationship Diagram.                    |
| [`Entity`](#ij.diagrams.erd.Entity)(name[, fields, metadata])                  | An entity in an ERD.                            |
| [`Field`](#ij.diagrams.erd.Field)(name, type[, primary_key, ...])             | A field in an entity.                           |
| [`Relationship`](#ij.diagrams.erd.Relationship)(from_entity, to_entity, cardinality) | A relationship between entities.                |

### *class* ij.diagrams.erd.Cardinality(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Relationship cardinality.

### *class* ij.diagrams.erd.ERDBuilder

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Builder for creating ERDs from various sources.

#### *static* from_dict(schema)

Create ERD from dictionary schema.

* **Parameters:**
  **schema** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)) – Dictionary describing entities and relationships
* **Return type:**
  [`ERDiagram`](#ij.diagrams.erd.ERDiagram)
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
  [`ERDiagram`](#ij.diagrams.erd.ERDiagram)
* **Returns:**
  ERDiagram instance

### *class* ij.diagrams.erd.ERDiagram(title=None)

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

### *class* ij.diagrams.erd.Entity(name, fields=<factory>, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An entity in an ERD.

#### add_field(name, field_type, primary_key=False, foreign_key=None, nullable=True, unique=False)

Add a field to the entity.

### *class* ij.diagrams.erd.Field(name, type, primary_key=False, foreign_key=None, nullable=True, unique=False)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A field in an entity.

### *class* ij.diagrams.erd.Relationship(from_entity, to_entity, cardinality, label=None, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A relationship between entities.
