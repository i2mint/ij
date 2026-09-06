"""Tests that ``ij.__version__`` stays in step with the installed distribution.

The single source of truth for the version is ``pyproject.toml`` (which the wads
CI bumps on every release). ``ij.__version__`` must be derived from installed
metadata rather than a hand-edited literal, which silently drifts.
"""

from importlib.metadata import PackageNotFoundError, version

import pytest

import ij


def test_version_matches_installed_metadata():
    """``ij.__version__`` equals the version of the installed ``ij`` distribution."""
    try:
        installed = version("ij")
    except PackageNotFoundError:  # pragma: no cover - only in an uninstalled tree
        pytest.skip("ij is not installed; no distribution metadata to compare against")
    assert ij.__version__ == installed


def test_version_is_a_string():
    """The attribute keeps its public shape: a module-level, non-empty ``str``."""
    assert isinstance(ij.__version__, str)
    assert ij.__version__
