"""CLI interface for DataCheck."""

from pathlib import Path

import typer
from rich.console import Console

from datacheck import __version__
from datacheck.engine import ValidationEngine
from datacheck.exceptions import ConfigurationError, DataCheckError, DataLoadError, ValidationError
from datacheck.output import JSONExporter, OutputFormatter

app = typer.Typer(
    name="datacheck",
    help="Lightweight data quality validation CLI tool",
    add_completion=False,
)

console = Console()


@app.command()
def validate(
    file_path: str,
    config: str | None = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to validation config file (auto-discovered if not provided)",
    ),
    output_format: str = typer.Option(
        "terminal",
        "--format",
        "-f",
        help="Output format: 'terminal' or 'json'",
    ),
    json_output: str | None = typer.Option(
        None,
        "--json-output",
        "-o",
        help="Path to write JSON output (only with --format json)",
    ),
) -> None:
    """Validate data file against configured quality rules.

    Exit codes:
      0 - All validation rules passed
      1 - Some validation rules failed
      2 - Configuration error
      3 - Data loading error
      4 - Unexpected error
    """
    try:
        # Validate arguments
        if output_format not in ["terminal", "json"]:
            console.print(
                f"[red]Error:[/red] Invalid output format '{output_format}'. "
                f"Must be 'terminal' or 'json'.",
                style="red",
            )
            raise typer.Exit(code=2)

        if json_output and output_format != "json":
            console.print(
                "[yellow]Warning:[/yellow] --json-output specified but --format is not 'json'. "
                "Setting format to 'json'.",
                style="yellow",
            )
            output_format = "json"

        # Initialize validation engine
        try:
            if config:
                config_path = Path(config)
                engine = ValidationEngine(config_path=config_path)
            else:
                engine = ValidationEngine()
        except ConfigurationError as e:
            console.print(f"[red]Configuration Error:[/red] {e}", style="red")
            raise typer.Exit(code=2) from e

        # Load and validate data
        try:
            summary = engine.validate_file(file_path)
        except DataLoadError as e:
            console.print(f"[red]Data Load Error:[/red] {e}", style="red")
            raise typer.Exit(code=3) from e

        # Output results
        if output_format == "terminal":
            formatter = OutputFormatter(console=console)
            formatter.print_summary(summary)
        elif output_format == "json":
            json_str = JSONExporter.export_summary(summary, output_path=json_output, pretty=True)
            if not json_output:
                # Print to stdout if no output file specified
                console.print(json_str)

        # Determine exit code
        if summary.has_errors:
            # Validation errors occurred (configuration/execution issues)
            raise typer.Exit(code=4)
        elif not summary.all_passed:
            # Validation rules failed
            raise typer.Exit(code=1)
        else:
            # All rules passed
            raise typer.Exit(code=0)

    except typer.Exit:
        # Re-raise typer Exit exceptions (for proper exit codes)
        raise
    except (ConfigurationError, DataLoadError, ValidationError) as e:
        # These should have been handled above, but catch just in case
        console.print(f"[red]Error:[/red] {e}", style="red")
        raise typer.Exit(code=4) from e
    except DataCheckError as e:
        # Generic DataCheck error
        console.print(f"[red]DataCheck Error:[/red] {e}", style="red")
        raise typer.Exit(code=4) from e
    except Exception as e:
        # Unexpected error
        console.print(f"[red]Unexpected Error:[/red] {e}", style="red")
        raise typer.Exit(code=4) from e


@app.command()
def version() -> None:
    """Display version information."""
    console.print(f"DataCheck v{__version__}")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """DataCheck - Lightweight data quality validation CLI tool.

    Run 'datacheck validate <file>' to validate a data file.
    Run 'datacheck --help' for more information.
    """
    if ctx.invoked_subcommand is None:
        console.print("[bold]DataCheck[/bold] - Data Quality Validation")
        console.print(f"Version: {__version__}")
        console.print()
        console.print("Usage: datacheck [COMMAND] [OPTIONS]")
        console.print()
        console.print("Commands:")
        console.print("  validate  Validate data file against configured rules")
        console.print("  version   Display version information")
        console.print()
        console.print("Run 'datacheck [COMMAND] --help' for more information on a command.")


if __name__ == "__main__":
    app()
