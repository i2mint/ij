# ij.importers.database

Import diagrams from database schemas.

### Functions

| [`from_database`](#ij.importers.database.from_database)(connection_string[, schema])   | Import ERD from database schema.   |
|-----------------------------------------------------------------------------------------------|------------------------------------|
| [`from_sql_file`](#ij.importers.database.from_sql_file)(file_path)                     | Import ERD from SQL DDL file.      |

### ij.importers.database.from_database(connection_string, schema=None)

Import ERD from database schema.

* **Parameters:**
  * **connection_string** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Database connection string
  * **schema** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional schema name
* **Return type:**
  [`ERDiagram`](ij.diagrams.erd.html.md#ij.diagrams.erd.ERDiagram)
* **Returns:**
  ERDiagram representing database schema

### Example

```pycon
>>> erd = from_database('postgresql://user:pass@localhost/mydb')
>>> erd = from_database('sqlite:///path/to/db.sqlite')
```

#### NOTE
Requires sqlalchemy: pip install sqlalchemy

### ij.importers.database.from_sql_file(file_path)

Import ERD from SQL DDL file.

* **Parameters:**
  **file_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to SQL file
* **Return type:**
  [`ERDiagram`](ij.diagrams.erd.html.md#ij.diagrams.erd.ERDiagram)
* **Returns:**
  ERDiagram from SQL statements

### Example

```pycon
>>> erd = from_sql_file('schema.sql')
```
