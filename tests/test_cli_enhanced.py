"""End-to-end tests of the `ij` and `ij2` command lines through their main() functions."""

import sys

import pytest

from ij import cli, cli_enhanced

A = "graph TD\n    A[Start] --> B[Work]\n    B --> C[End]\n    A --> D[Side]\n"
B = "graph TD\n    A[Start] --> B[Work]\n    B --> E[More]\n"


@pytest.fixture
def files(tmp_path):
    (tmp_path / "a.mmd").write_text(A)
    (tmp_path / "b.mmd").write_text(B)
    return tmp_path


def run2(monkeypatch, capsys, *argv, exit_code=None):
    monkeypatch.setattr(sys, "argv", ["ij2", *map(str, argv)])
    if exit_code is None:
        cli_enhanced.main()
    else:
        with pytest.raises(SystemExit) as e:
            cli_enhanced.main()
        assert e.value.code == exit_code
    return capsys.readouterr()


def test_stats(files, monkeypatch, capsys):
    out = run2(monkeypatch, capsys, "stats", files / "a.mmd").out
    assert "Nodes: 4" in out and "Edges: 3" in out and "Has cycles: False" in out


def test_convert_to_stdout_and_file(files, monkeypatch, capsys):
    out = run2(monkeypatch, capsys, "convert", files / "a.mmd", "--to", "d2").out
    assert 'A: "Start"' in out and "shape: rectangle" in out
    target = files / "out.d2"
    out = run2(monkeypatch, capsys, "convert", files / "a.mmd", "-o", target).out
    assert "mermaid → d2" in out and "A -> B" in target.read_text()


def test_validate_valid_and_missing(files, monkeypatch, capsys):
    assert "Valid" in run2(monkeypatch, capsys, "validate", files / "a.mmd").out
    err = run2(monkeypatch, capsys, "validate", files / "nope.mmd", exit_code=1).err
    assert "No files found" in err


def test_validate_reports_issues_with_severity_names(files, monkeypatch, capsys):
    out = run2(monkeypatch, capsys, "validate", files / "a.mmd", "--max-nodes", "2", exit_code=1).out
    assert "1 issue(s)" in out and "ERROR:" in out  # severity prints as its value, upper-cased


def test_validate_glob_and_unparseable(files, monkeypatch, capsys):
    monkeypatch.chdir(files)
    out = run2(monkeypatch, capsys, "validate", "*.mmd").out
    assert out.count("Valid") == 2


def test_diff(files, monkeypatch, capsys):
    out = run2(monkeypatch, capsys, "diff", files / "a.mmd", files / "b.mmd").out
    assert "Added nodes: 1" in out and "Removed nodes: 2" in out


def test_extract_and_simplify(files, monkeypatch, capsys):
    out = run2(monkeypatch, capsys, "extract", files / "a.mmd", "B").out
    assert "B[Work]" in out and "C[End]" in out and "A[Start]" not in out
    out = run2(monkeypatch, capsys, "simplify", files / "a.mmd").out
    assert out.startswith("flowchart TD") and "A --> B" in out


def test_no_command_prints_help(monkeypatch, capsys):
    out = run2(monkeypatch, capsys, exit_code=1).out
    assert "usage: ij2" in out


def test_detect_format_and_parser_lookup():
    assert cli_enhanced.detect_format("x.mmd") == "mermaid"
    assert cli_enhanced.detect_format("x.d2") == "d2"
    assert cli_enhanced.get_parser_for_format("mermaid") is not None


def test_plain_ij_command(files, monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(sys, "argv", ["ij", "Start -> Do work -> End", "-d", "LR"])
    cli.main()
    out = capsys.readouterr().out
    assert out.startswith("flowchart LR") and "Do work" in out
    target = tmp_path / "o.mmd"
    monkeypatch.setattr(sys, "argv", ["ij", "A -> B", "-o", str(target), "-t", "T"])
    cli.main()
    assert "A" in target.read_text()
    src = tmp_path / "in.txt"
    src.write_text("X -> Y")
    monkeypatch.setattr(sys, "argv", ["ij", "-f", str(src)])
    cli.main()
    assert "X" in capsys.readouterr().out


def test_plain_ij_errors(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["ij", "-f", "/definitely/missing.txt"])
    with pytest.raises(SystemExit) as e:
        cli.main()
    assert e.value.code == 1 and "not found" in capsys.readouterr().err
    monkeypatch.setattr(sys, "argv", ["ij"])
    with pytest.raises(SystemExit) as e:
        cli.main()
    assert e.value.code == 1


def test_convert_of_a_txt_file_reads_it_as_plain_text(tmp_path, capsys):
    """A .txt input goes through the plain-text converter, not the mermaid parser (empty diagram)."""
    from types import SimpleNamespace

    from ij.cli_enhanced import cmd_convert

    src = tmp_path / "steps.txt"
    src.write_text("Start\nProcess data\nEnd\n")
    args = SimpleNamespace(
        input=str(src), from_format=None, to_format=None, output=None, direction=None
    )
    cmd_convert(args)
    out = capsys.readouterr().out
    assert "Process data" in out and "-->" in out


def test_convert_to_a_txt_file_writes_mermaid(files, monkeypatch, capsys):
    """A .txt output has no renderer of its own: it gets mermaid, the default output."""
    target = files / "out.txt"
    out = run2(monkeypatch, capsys, "convert", files / "a.mmd", "-o", target).out
    assert "mermaid → mermaid" in out
    assert target.read_text().startswith("flowchart TD") and "A --> B" in target.read_text()
