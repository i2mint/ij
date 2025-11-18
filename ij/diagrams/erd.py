"""Entity-Relationship Diagram support.

Provides tools for creating and rendering ERDs.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class Cardinality(Enum):
    """Relationship cardinality."""

    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:N"
    MANY_TO_ONE = "N:1"
    MANY_TO_MANY = "N:N"


@dataclass
class Field:
    """A field in an entity."""

    name: str
    type: str
    primary_key: bool = False
    foreign_key: Optional[str] = None  # References entity.field
    nullable: bool = True
    unique: bool = False


@dataclass
class Entity:
    """An entity in an ERD."""

    name: str
    fields: List[Field] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def add_field(
        self,
        name: str,
        field_type: str,
        primary_key: bool = False,
        foreign_key: Optional[str] = None,
        nullable: bool = True,
        unique: bool = False,
    ):
        """Add a field to the entity."""
        self.fields.append(
            Field(
                name=name,
                type=field_type,
                primary_key=primary_key,
                foreign_key=foreign_key,
                nullable=nullable,
                unique=unique,
            )
        )


@dataclass
class Relationship:
    """A relationship between entities."""

    from_entity: str
    to_entity: str
    cardinality: Cardinality
    label: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class ERDiagram:
    """Entity-Relationship Diagram."""

    def __init__(self, title: Optional[str] = None):
        """Initialize ERD.

        Args:
            title: Diagram title
        """
        self.title = title
        self.entities: List[Entity] = []
        self.relationships: List[Relationship] = []

    def add_entity(self, entity: Entity):
        """Add an entity to the diagram."""
        self.entities.append(entity)

    def add_relationship(
        self,
        from_entity: str,
        to_entity: str,
        cardinality: Cardinality,
        label: Optional[str] = None,
    ):
        """Add a relationship between entities."""
        self.relationships.append(
            Relationship(
                from_entity=from_entity,
                to_entity=to_entity,
                cardinality=cardinality,
                label=label,
            )
        )

    def to_mermaid(self) -> str:
        """Render ERD as Mermaid ER diagram.

        Returns:
            Mermaid ER diagram syntax
        """
        lines = ["erDiagram"]

        if self.title:
            lines.append(f"    title {self.title}")

        # Add relationships
        for rel in self.relationships:
            # Mermaid ER cardinality syntax
            card_map = {
                Cardinality.ONE_TO_ONE: "||--||",
                Cardinality.ONE_TO_MANY: "||--o{",
                Cardinality.MANY_TO_ONE: "}o--||",
                Cardinality.MANY_TO_MANY: "}o--o{",
            }
            card_symbol = card_map.get(rel.cardinality, "||--||")
            label = f' : "{rel.label}"' if rel.label else ""
            lines.append(f"    {rel.from_entity} {card_symbol} {rel.to_entity}{label}")

        # Add entities with fields
        for entity in self.entities:
            lines.append(f"    {entity.name} {{")
            for field in entity.fields:
                field_line = f"        {field.type} {field.name}"

                # Add constraints
                constraints = []
                if field.primary_key:
                    constraints.append("PK")
                if field.foreign_key:
                    constraints.append("FK")
                if field.unique:
                    constraints.append("UK")
                if not field.nullable:
                    constraints.append("NOT NULL")

                if constraints:
                    field_line += f" \"{', '.join(constraints)}\""

                lines.append(field_line)
            lines.append("    }")

        return "\n".join(lines)

    def to_plantuml(self) -> str:
        """Render ERD as PlantUML class diagram.

        Returns:
            PlantUML syntax
        """
        lines = ["@startuml"]

        if self.title:
            lines.append(f"title {self.title}")

        # Add entities as classes
        for entity in self.entities:
            lines.append(f"class {entity.name} {{")
            for field in entity.fields:
                prefix = ""
                if field.primary_key:
                    prefix = "+ "
                elif field.foreign_key:
                    prefix = "# "
                else:
                    prefix = "- "

                lines.append(f"  {prefix}{field.name}: {field.type}")
            lines.append("}")

        # Add relationships
        for rel in self.relationships:
            # PlantUML cardinality
            card_map = {
                Cardinality.ONE_TO_ONE: '"1" -- "1"',
                Cardinality.ONE_TO_MANY: '"1" -- "N"',
                Cardinality.MANY_TO_ONE: '"N" -- "1"',
                Cardinality.MANY_TO_MANY: '"N" -- "N"',
            }
            card = card_map.get(rel.cardinality, '"1" -- "1"')
            label = f" : {rel.label}" if rel.label else ""
            lines.append(f"{rel.from_entity} {card} {rel.to_entity}{label}")

        lines.append("@enduml")
        return "\n".join(lines)

    def to_d2(self) -> str:
        """Render ERD as D2 diagram.

        Returns:
            D2 syntax
        """
        lines = []

        if self.title:
            lines.append(f"# {self.title}")
            lines.append("")

        # Add entities
        for entity in self.entities:
            lines.append(f"{entity.name}: {{")
            lines.append("  shape: sql_table")

            # Add fields
            for i, field in enumerate(entity.fields):
                constraints = []
                if field.primary_key:
                    constraints.append("PK")
                if field.foreign_key:
                    constraints.append("FK")
                if not field.nullable:
                    constraints.append("NOT NULL")

                constraint_str = f" ({', '.join(constraints)})" if constraints else ""
                lines.append(f"  {field.name}: {field.type}{constraint_str}")

            lines.append("}")

        # Add relationships
        for rel in self.relationships:
            label = rel.label if rel.label else rel.cardinality.value
            lines.append(f"{rel.from_entity} -> {rel.to_entity}: {label}")

        return "\n".join(lines)


class ERDBuilder:
    """Builder for creating ERDs from various sources."""

    @staticmethod
    def from_dict(schema: Dict) -> ERDiagram:
        """Create ERD from dictionary schema.

        Args:
            schema: Dictionary describing entities and relationships

        Returns:
            ERDiagram instance

        Example:
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
        """
        erd = ERDiagram(title=schema.get("title"))

        # Parse entities
        for entity_name, field_defs in schema.get("entities", {}).items():
            entity = Entity(name=entity_name)

            for field_def in field_defs:
                # Parse field definition: "name:type:constraints"
                parts = field_def.split(":")
                field_name = parts[0]
                field_type = parts[1] if len(parts) > 1 else "string"

                # Parse constraints
                is_pk = False
                is_fk = None
                is_unique = False
                is_nullable = True

                if len(parts) > 2:
                    constraints = parts[2:]
                    for constraint in constraints:
                        if constraint.upper() == "PK":
                            is_pk = True
                            is_nullable = False
                        elif constraint.upper().startswith("FK"):
                            # Extract FK reference
                            if "->" in constraint:
                                is_fk = constraint.split("->")[1]
                        elif constraint.upper() == "UNIQUE":
                            is_unique = True
                        elif constraint.upper() == "NOT NULL":
                            is_nullable = False

                entity.add_field(
                    field_name,
                    field_type,
                    primary_key=is_pk,
                    foreign_key=is_fk,
                    nullable=is_nullable,
                    unique=is_unique,
                )

            erd.add_entity(entity)

        # Parse relationships
        for rel_def in schema.get("relationships", []):
            card_str = rel_def.get("cardinality", "1:N")
            cardinality = Cardinality(card_str)

            erd.add_relationship(
                from_entity=rel_def["from"],
                to_entity=rel_def["to"],
                cardinality=cardinality,
                label=rel_def.get("label"),
            )

        return erd

    @staticmethod
    def from_sql_ddl(ddl: str) -> ERDiagram:
        """Create ERD from SQL DDL statements (basic support).

        Args:
            ddl: SQL CREATE TABLE statements

        Returns:
            ERDiagram instance
        """
        import re

        erd = ERDiagram()

        # Extract CREATE TABLE statements
        create_tables = re.findall(
            r"CREATE\s+TABLE\s+(\w+)\s*\((.*?)\);", ddl, re.IGNORECASE | re.DOTALL
        )

        for table_name, fields_sql in create_tables:
            entity = Entity(name=table_name)

            # Parse fields
            field_lines = [f.strip() for f in fields_sql.split(",")]

            for line in field_lines:
                # Skip constraints
                if line.upper().startswith(("PRIMARY KEY", "FOREIGN KEY", "CONSTRAINT")):
                    continue

                # Parse field: name type [constraints]
                match = re.match(r"(\w+)\s+(\w+)(.*)$", line, re.IGNORECASE)
                if match:
                    field_name = match.group(1)
                    field_type = match.group(2)
                    constraints = match.group(3).upper()

                    is_pk = "PRIMARY KEY" in constraints
                    is_nullable = "NOT NULL" not in constraints
                    is_unique = "UNIQUE" in constraints

                    entity.add_field(
                        field_name,
                        field_type,
                        primary_key=is_pk,
                        nullable=is_nullable,
                        unique=is_unique,
                    )

            erd.add_entity(entity)

        return erd
