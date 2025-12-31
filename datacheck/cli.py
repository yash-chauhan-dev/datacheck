"""CLI interface for DataCheck (placeholder for Phase 9)."""

import typer

app = typer.Typer(
    name="datacheck",
    help="Lightweight data quality validation CLI tool",
    add_completion=False,
)


@app.command()
def validate() -> None:
    """Validate data against rules (to be implemented)."""
    typer.echo("DataCheck CLI - Coming soon in Phase 9")


@app.command()
def version() -> None:
    """Display version information."""
    typer.echo("DataCheck v0.1.0")


if __name__ == "__main__":
    app()
