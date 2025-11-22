"""Import diagrams from database schemas."""

from typing import Optional

from ..diagrams.erd import Entity, ERDiagram, Cardinality


def from_database(connection_string: str, schema: Optional[str] = None) -> ERDiagram:
    """Import ERD from database schema.

    Args:
        connection_string: Database connection string
        schema: Optional schema name

    Returns:
        ERDiagram representing database schema

    Example:
        >>> erd = from_database('postgresql://user:pass@localhost/mydb')
        >>> erd = from_database('sqlite:///path/to/db.sqlite')

    Note:
        Requires sqlalchemy: pip install sqlalchemy
    """
    try:
        from sqlalchemy import create_engine, inspect
    except ImportError:
        raise ImportError(
            "SQLAlchemy required for database import. Install with: pip install sqlalchemy"
        )

    # Create engine and inspector
    engine = create_engine(connection_string)
    inspector = inspect(engine)

    erd = ERDiagram(title=f"Database Schema: {engine.url.database}")

    # Get schema name
    schema_name = schema or inspector.default_schema_name

    # Get all tables
    table_names = inspector.get_table_names(schema=schema_name)

    # Create entities for each table
    for table_name in table_names:
        entity = Entity(name=table_name)

        # Get columns
        columns = inspector.get_columns(table_name, schema=schema_name)
        pk_constraint = inspector.get_pk_constraint(table_name, schema=schema_name)
        pk_columns = set(pk_constraint.get("constrained_columns", []))

        for column in columns:
            col_name = column["name"]
            col_type = str(column["type"])

            entity.add_field(
                name=col_name,
                field_type=col_type,
                primary_key=col_name in pk_columns,
                nullable=column.get("nullable", True),
            )

        erd.add_entity(entity)

    # Get foreign key relationships
    for table_name in table_names:
        fks = inspector.get_foreign_keys(table_name, schema=schema_name)

        for fk in fks:
            referred_table = fk["referred_table"]

            # Infer cardinality (simplified - assumes 1:N for FKs)
            cardinality = Cardinality.ONE_TO_MANY

            erd.add_relationship(
                from_entity=referred_table,
                to_entity=table_name,
                cardinality=cardinality,
                label=fk.get("name"),
            )

    return erd


def from_sql_file(file_path: str) -> ERDiagram:
    """Import ERD from SQL DDL file.

    Args:
        file_path: Path to SQL file

    Returns:
        ERDiagram from SQL statements

    Example:
        >>> erd = from_sql_file('schema.sql')
    """
    from pathlib import Path
    from ..diagrams.erd import ERDBuilder

    sql_content = Path(file_path).read_text()
    return ERDBuilder.from_sql_ddl(sql_content)
