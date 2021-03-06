from pythonit_toolkit import __version__
from ward import test


@test("test")
def _():
    assert __version__ == "0.1.0"
