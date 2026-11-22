"""Tests for importing an ERD from a real (temporary sqlite) database and from a SQL file."""

import pytest

from ij.importers.database import from_database, from_sql_file


def _entities(erd):
    return {e.name: e for e in (erd.entities if isinstance(erd.entities, list) else erd.entities.values())}


def test_from_database_reads_tables_columns_and_foreign_keys(tmp_path):
    sa = pytest.importorskip("sqlalchemy")
    db = tmp_path / "shop.sqlite"
    engine = sa.create_engine(f"sqlite:///{db}")
    with engine.begin() as con:
        con.exec_driver_sql("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        con.exec_driver_sql(
            "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, "
            "FOREIGN KEY (customer_id) REFERENCES customers(id))"
        )
    erd = from_database(f"sqlite:///{db}")
    assert erd.title == "Database Schema: " + str(db)
    ents = _entities(erd)
    assert set(ents) == {"customers", "orders"}
    cust = {f.name: f for f in ents["customers"].fields}
    assert cust["id"].primary_key and not cust["name"].nullable
    rel = erd.relationships[0]
    assert (rel.from_entity, rel.to_entity) == ("customers", "orders")  # parent -> child, 1:N
    assert rel.cardinality.value == "1:N"
    assert "customers" in erd.to_mermaid()


def test_from_sql_file(tmp_path):
    f = tmp_path / "schema.sql"
    f.write_text("CREATE TABLE t (id INT PRIMARY KEY, label TEXT);")
    ents = _entities(from_sql_file(str(f)))
    assert list(ents) == ["t"] and {x.name for x in ents["t"].fields} == {"id", "label"}
