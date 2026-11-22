"""Tests for ERD and state machine builders, exporters, validation and simulation."""

import pytest

from ij.diagrams.erd import Cardinality, ERDBuilder
from ij.diagrams.state_machine import StateMachineBuilder, StateType

SCHEMA = {
    "title": "Blog",
    "entities": {
        "User": ["id:int:PK", "name:string", "email:string:unique"],
        "Post": ["id:int:PK", "user_id:int:FK->User", "title"],
    },
    "relationships": [
        {"from": "User", "to": "Post", "cardinality": "1:N", "label": "writes"}
    ],
}


def _fields(entity):
    return {f.name: f for f in entity.fields}


def test_erd_from_dict_parses_field_constraints():
    erd = ERDBuilder.from_dict(SCHEMA)
    user, post = erd.entities if isinstance(erd.entities, list) else list(erd.entities.values())
    uf, pf = _fields(user), _fields(post)
    assert uf["id"].primary_key and not uf["id"].nullable
    assert uf["email"].unique and uf["name"].type == "string"
    assert pf["user_id"].foreign_key == "User"
    assert pf["title"].type == "string"  # type defaults to string
    rel = erd.relationships[0]
    assert rel.cardinality == Cardinality.ONE_TO_MANY and rel.label == "writes"


def test_erd_exports_mention_entities_fields_and_relationship():
    erd = ERDBuilder.from_dict(SCHEMA)
    mermaid = erd.to_mermaid()
    assert mermaid.startswith("erDiagram") and 'User ||--o{ Post : "writes"' in mermaid
    assert 'int id "PK, NOT NULL"' in mermaid and 'string email "UK"' in mermaid
    assert 'int user_id "FK"' in mermaid
    puml = erd.to_plantuml()
    assert puml.startswith("@startuml") and puml.rstrip().endswith("@enduml")
    assert "class User {" in puml and 'User "1" -- "N" Post : writes' in puml
    d2 = erd.to_d2()
    assert "shape: sql_table" in d2 and "User -> Post: writes" in d2


def test_erd_from_sql_ddl():
    ddl = """
    CREATE TABLE accounts (
        id INT PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        note TEXT,
        PRIMARY KEY (id)
    );
    CREATE TABLE logs (id INT, msg TEXT);
    """
    erd = ERDBuilder.from_sql_ddl(ddl)
    entities = erd.entities if isinstance(erd.entities, list) else list(erd.entities.values())
    assert [e.name for e in entities] == ["accounts", "logs"]
    f = _fields(entities[0])
    assert set(f) == {"id", "name", "note"}  # the table-level PRIMARY KEY line is skipped
    assert f["id"].primary_key and f["name"].unique and not f["name"].nullable
    assert f["note"].nullable


DOOR = {
    "name": "Door",
    "initial": "locked",
    "states": {"locked": {"type": "initial"}, "unlocked": {}, "gone": {"type": "final"}},
    "transitions": [
        {"from": "locked", "trigger": "unlock", "to": "unlocked",
         "condition": "has_key", "action": "click"},
        {"from": "unlocked", "trigger": "lock", "to": "locked"},
    ],
}


def test_state_machine_from_dict_and_exports():
    sm = StateMachineBuilder.from_dict(DOOR)
    assert sm.initial_state == "locked"
    assert {s.name: s.state_type for s in sm.states}["gone"] == StateType.FINAL
    mermaid = sm.to_mermaid()
    assert mermaid.startswith("stateDiagram-v2") and "[*] --> locked" in mermaid
    assert "locked --> unlocked: unlock [has_key] / click" in mermaid
    assert "gone --> [*]" in mermaid
    puml = sm.to_plantuml()
    assert "title Door" in puml and "locked --> unlocked : unlock [has_key] / click" in puml
    d2 = sm.to_d2()
    assert "shape: oval" in d2 and 'locked -> unlocked: "unlock [has_key] / click"' in d2


def test_state_machine_validate_and_reachability():
    sm = StateMachineBuilder.from_dict(DOOR)
    assert sm.validate() == ["Unreachable states: gone"]
    assert sm.get_triggers_from_state("locked") == ["unlock"]
    assert sm.get_triggers_from_state("gone") == []
    bad = StateMachineBuilder.from_dict(
        {"states": {"a": {}}, "transitions": [
            {"from": "a", "trigger": "x", "to": "ghost"},
            {"from": "a", "trigger": "x", "to": "ghost"},
        ]}
    )
    issues = bad.validate()
    assert "No initial state defined" in issues
    assert "Transition to undefined state: ghost" in issues
    assert any(i.startswith("Duplicate transition") for i in issues)


def test_state_machine_simulate():
    sm = StateMachineBuilder.from_dict(DOOR)
    assert sm.simulate("locked", ["unlock", "lock"]) == ["locked", "unlocked", "locked"]
    path = sm.simulate("locked", ["unlock", "boom", "lock"])
    assert path[:2] == ["locked", "unlocked"]
    assert path[-1] == "<error: no transition for boom from unlocked>"  # stops at the first error


def test_state_machine_from_code_dsl():
    sm = StateMachineBuilder.from_code(
        "INITIAL a\nSTATE b\nSTATE c FINAL\na --go--> b\nb --go--> c"
    )
    assert sm.initial_state == "a"
    assert [(s.name, s.state_type.value) for s in sm.states] == [
        ("a", "initial"), ("b", "normal"), ("c", "final"),
    ]
    assert [(t.from_state, t.trigger, t.to_state) for t in sm.transitions] == [
        ("a", "go", "b"), ("b", "go", "c"),
    ]
    assert sm.validate() == []
