import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["tests", "cover", "lint"]


@nox.session
def tests(session):
    session.install("poetry")
    session.install("pytest-cov")
    session.run("poetry", "install")
    session.run("poetry", "check")
    session.run("poetry", "run", "pytest", "-vv", "--cov=yfs")
    session.notify("cover")


@nox.session
def cover(session):
    session.install("coverage")
    session.run("coverage", "report", "--show-missing", "--fail-under=70")
    session.run("coverage", "erase")


lint_files = [
    "asset_types",
    "cleaner",
    "exchanges",
    "lookup",
    "options",
    "paths",
    "quote",
    "requestor",
    "statistics",
    "summary",
]


@nox.session
def lint(session):
    session.install(
        "black",
        "flake8",
        "flake8-import-order",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-annotations",
        "pylint",
    )
    for file_name in lint_files:
        session.run("black", "--line-length", "99", "--check", f"yfs/{file_name}.py")
        session.run("flake8", "--import-order-style", "google", f"yfs/{file_name}.py")
        session.run("pylint", "--disable=E0401,R0903,W0511", f"yfs/{file_name}.py")


@nox.session
def docs(session):
    session.install("pydoc-markdown", "mkdocs-material")
    session.run("pydoc-markdown", "pydoc-markdown.yml", "--server", "--open")
