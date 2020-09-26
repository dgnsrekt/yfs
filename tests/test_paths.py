from yfs import __version__
from yfs.paths import PROJECT_ROOT, SOURCE_ROOT
import toml


def test_sanity():
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    assert pyproject_path.exists()

    with open(pyproject_path, mode="r") as file:
        content = toml.loads(file.read())

    assert content["tool"]["poetry"].get("version") is not None
    assert content["tool"]["poetry"].get("version") == __version__


def test_sanity_two():
    assert SOURCE_ROOT.exists()
