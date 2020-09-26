import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def tests(session):
    session.install("poetry")
    session.run("poetry", "install")
    session.run("poetry", "run", "pytest", "-vv")


lint_files = [
    "asset_types",
    "cleaner",
    "exchanges",
    "paths",
    "quote",
    "requestor",
    "summary",
    "symbol",
]


@nox.session
def lint(session):
    session.install("black", "flake8", "flake8-import-order", "flake8-bugbear")
    for file_name in lint_files:
        session.run("black", "--line-length", "99", "--check", f"yfs/{file_name}.py")
        session.run("flake8", "--import-order-style", "google", f"yfs/{file_name}.py")
