from pathlib import Path

import pytest

# tomllib is 3.11+; the guard only needs to run on one interpreter.
tomllib = pytest.importorskip("tomllib")


def test_pypi_summary_fits():
    """PyPI rejects an upload whose summary (project.description) is over 512 characters.

    0.33.0 never reached PyPI because of it: the upload failed with 400 after tests passed.
    """
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    project = tomllib.loads(pyproject.read_text())["project"]
    assert len(project["description"]) <= 512
    assert "\n" not in project["description"]
