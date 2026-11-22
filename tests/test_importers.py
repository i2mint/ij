"""Tests for the OpenAPI and draw.io importers (files written to a temp dir)."""

import base64
import json
import zlib

import pytest

from ij.core import NodeType
from ij.importers.drawio import from_drawio, from_drawio_xml
from ij.importers.openapi import from_openapi

SPEC = {
    "info": {"title": "Pets", "version": "2.1"},
    "paths": {
        "/pets": {
            "get": {"operationId": "listPets", "tags": ["pets"]},
            "post": {"operationId": "addPet", "tags": ["pets"]},
        },
        "/health": {"get": {}},  # no operationId, no tags
        "/owners": {"delete": {"operationId": "dropOwner", "tags": ["owners"]}, "options": {}},
    },
}


def test_openapi_from_dict_groups_operations_by_tag():
    d = from_openapi(SPEC)
    assert d.metadata == {"title": "Pets", "type": "api"}
    root = d.get_node("api_root")
    assert root.label == "Pets v2.1" and root.node_type == NodeType.START
    tags = {n.id: n.label for n in d.nodes if n.id.startswith("tag_")}
    assert tags == {"tag_pets": "Pets", "tag_default": "Default", "tag_owners": "Owners"}
    assert d.get_node("listPets").label == "GET /pets"
    assert d.get_node("get_/health").label == "GET /health"  # synthesised id
    assert d.get_node("dropOwner").label == "DELETE /owners"
    edges = {(e.source, e.target) for e in d.edges}
    assert ("api_root", "tag_pets") in edges and ("tag_pets", "addPet") in edges
    assert d.get_node("options_/owners") is None  # unsupported method skipped
    assert d.validate()


def test_openapi_title_override_and_defaults():
    assert from_openapi(SPEC, title="Custom").metadata["title"] == "Custom"
    d = from_openapi({})
    assert d.metadata["title"] == "API" and d.get_node("api_root").label == "API v1.0"


def test_openapi_from_json_and_yaml_files(tmp_path):
    j = tmp_path / "spec.json"
    j.write_text(json.dumps(SPEC))
    assert from_openapi(str(j)).metadata["title"] == "Pets"
    yaml = pytest.importorskip("yaml")
    y = tmp_path / "spec.yaml"
    y.write_text(yaml.safe_dump(SPEC))
    assert from_openapi(str(y)).get_node("listPets") is not None


PLAIN = """<mxfile><diagram name="p1"><mxGraphModel><root>
<mxCell id="0"/><mxCell id="1" parent="0"/>
<mxCell id="a" value="Start here" style="ellipse;whiteSpace=wrap" vertex="1" parent="1"/>
<mxCell id="b" value="Is ok?" style="rhombus" vertex="1" parent="1"/>
<mxCell id="c" value="Stop" style="rounded=1" vertex="1" parent="1"/>
<mxCell id="d" value="Do work" style="" vertex="1" parent="1"/>
<mxCell id="e1" value="yes" edge="1" source="a" target="b" parent="1"/>
<mxCell id="e2" value="" edge="1" source="b" target="c" parent="1"/>
<mxCell id="e3" edge="1" source="b" target="zzz" parent="1"/>
</root></mxGraphModel></diagram></mxfile>""".replace("\n", "")


def _check_flow(d):
    assert [n.label for n in d.nodes] == ["Start here", "Is ok?", "Stop", "Do work"]
    assert [n.node_type for n in d.nodes] == [
        NodeType.START, NodeType.DECISION, NodeType.END, NodeType.PROCESS,
    ]
    assert [(e.source, e.target, e.label) for e in d.edges] == [
        ("n0", "n1", "yes"), ("n1", "n2", None),  # the edge to an unknown cell is dropped
    ]


def test_drawio_uncompressed(tmp_path):
    f = tmp_path / "flow.drawio"
    f.write_text(PLAIN)
    _check_flow(from_drawio(str(f)))
    _check_flow(from_drawio_xml(PLAIN))


def test_drawio_compressed_payload(tmp_path):
    inner = PLAIN[PLAIN.index("<mxGraphModel>") : PLAIN.index("</diagram>")]
    # draw.io: raw deflate, then base64
    deflated = zlib.compressobj(wbits=-zlib.MAX_WBITS)
    body = deflated.compress(inner.encode()) + deflated.flush()
    payload = base64.b64encode(body).decode()
    f = tmp_path / "compressed.drawio"
    f.write_text(f"<mxfile><diagram>{payload}</diagram></mxfile>")
    _check_flow(from_drawio(str(f)))


def test_drawio_without_a_diagram_is_an_error(tmp_path):
    f = tmp_path / "empty.drawio"
    f.write_text("<mxfile></mxfile>")
    with pytest.raises(ValueError, match="No diagram found"):
        from_drawio(str(f))
