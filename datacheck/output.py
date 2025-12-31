"""Output formatting and display."""

import json
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from datacheck.results import RuleResult, ValidationSummary


class OutputFormatter:
    """Formatter for Rich terminal output.

    Provides colored, formatted output for validation results with:
    - Color-coded pass/fail status (green/red/yellow)
    - Detailed failure information tables
    - Summary statistics panels
    - Progress indicators
    """

    def __init__(self, console: Console | None = None) -> None:
        """Initialize output formatter.

        Args:
            console: Rich Console instance (creates new one if None)
        """
        self.console = console or Console()

    def print_summary(self, summary: ValidationSummary) -> None:
        """Print validation summary with color-coded results.

        Args:
            summary: ValidationSummary to display
        """
        # Print header
        self.console.print()
        self.console.print(
            Panel.fit(
                "[bold]DataCheck Validation Results[/bold]",
                border_style="blue",
            )
        )
        self.console.print()

        # Print overall status
        if summary.all_passed:
            status_text = Text("✓ ALL CHECKS PASSED", style="bold green")
        elif summary.error_rules > 0:
            status_text = Text("✗ VALIDATION ERRORS", style="bold yellow")
        else:
            status_text = Text("✗ VALIDATION FAILED", style="bold red")

        self.console.print(status_text)
        self.console.print()

        # Print statistics
        self._print_statistics(summary)

        # Print detailed results
        if not summary.all_passed:
            self.console.print()
            self._print_failed_rules(summary)

        if summary.error_rules > 0:
            self.console.print()
            self._print_error_rules(summary)

    def _print_statistics(self, summary: ValidationSummary) -> None:
        """Print summary statistics.

        Args:
            summary: ValidationSummary containing statistics
        """
        table = Table(show_header=True, header_style="bold cyan", box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")

        table.add_row("Total Rules", str(summary.total_rules))
        table.add_row(
            "Passed",
            f"[green]{summary.passed_rules}[/green]",
        )
        table.add_row(
            "Failed",
            f"[red]{summary.failed_rules}[/red]" if summary.failed_rules > 0 else "0",
        )
        table.add_row(
            "Errors",
            f"[yellow]{summary.error_rules}[/yellow]" if summary.error_rules > 0 else "0",
        )

        self.console.print(table)

    def _print_failed_rules(self, summary: ValidationSummary) -> None:
        """Print detailed information about failed rules.

        Args:
            summary: ValidationSummary containing failed rules
        """
        failed_results = summary.get_failed_results()
        if not failed_results:
            return

        self.console.print("[bold red]Failed Rules:[/bold red]")
        self.console.print()

        for result in failed_results:
            self._print_rule_result(result)

    def _print_error_rules(self, summary: ValidationSummary) -> None:
        """Print detailed information about rules with errors.

        Args:
            summary: ValidationSummary containing error rules
        """
        error_results = summary.get_error_results()
        if not error_results:
            return

        self.console.print("[bold yellow]Rules with Errors:[/bold yellow]")
        self.console.print()

        for result in error_results:
            self._print_rule_result(result)

    def _print_rule_result(self, result: RuleResult) -> None:
        """Print detailed information for a single rule result.

        Args:
            result: RuleResult to display
        """
        # Print rule header
        if result.has_error:
            status_icon = "⚠"
            status_color = "yellow"
        else:
            status_icon = "✗"
            status_color = "red"

        self.console.print(
            f"{status_icon} [bold]{result.rule_name}[/bold] "
            f"(column: [cyan]{result.column}[/cyan])",
            style=status_color,
        )

        # Print error message if present
        if result.error:
            self.console.print(f"  Error: {result.error}", style="yellow")
            self.console.print()
            return

        # Print failure statistics
        failure_rate = (result.failed_rows / result.total_rows * 100) if result.total_rows > 0 else 0.0
        self.console.print(
            f"  Failed rows: {result.failed_rows:,} / {result.total_rows:,} "
            f"({failure_rate:.2f}%)"
        )

        # Print failure details if available
        if result.failure_details:
            details = result.failure_details

            # Create failure samples table
            if details.sample_failures:
                table = Table(
                    show_header=True,
                    header_style="bold",
                    box=None,
                    padding=(0, 2),
                )
                table.add_column("Row Index", justify="right", style="dim")

                # Limit to first 10 samples for display
                display_samples = details.sample_failures[:10]
                for idx in display_samples:
                    table.add_row(str(idx))

                self.console.print("  Sample failure row indices:", style="dim")
                self.console.print(table)

                # Indicate if more failures exist
                total_samples = len(details.sample_failures)
                if total_samples > 10:
                    self.console.print(
                        f"  ... and {total_samples - 10} more samples "
                        f"(showing 10/{total_samples})",
                        style="dim",
                    )

        self.console.print()

    def print_rule_result(self, result: RuleResult) -> None:
        """Print a single rule result.

        Args:
            result: RuleResult to display
        """
        if result.passed:
            status = "[green]✓ PASS[/green]"
        elif result.has_error:
            status = "[yellow]⚠ ERROR[/yellow]"
        else:
            status = "[red]✗ FAIL[/red]"

        self.console.print(
            f"{status} {result.rule_name} (column: [cyan]{result.column}[/cyan])"
        )

        if result.has_error:
            self.console.print(f"  Error: {result.error}", style="yellow")
        elif not result.passed:
            failure_rate = (result.failed_rows / result.total_rows * 100) if result.total_rows > 0 else 0.0
            self.console.print(
                f"  Failed: {result.failed_rows:,} / {result.total_rows:,} rows "
                f"({failure_rate:.2f}%)"
            )


class JSONExporter:
    """Exporter for JSON output format.

    Provides JSON export functionality for CI/CD integration:
    - Structured JSON output
    - Pretty-print and compact modes
    - Full failure detail export
    """

    @staticmethod
    def export_summary(
        summary: ValidationSummary,
        output_path: str | Path | None = None,
        pretty: bool = True,
    ) -> str:
        """Export ValidationSummary to JSON format.

        Args:
            summary: ValidationSummary to export
            output_path: Optional file path to write JSON (writes to file if provided)
            pretty: Whether to pretty-print JSON (default: True)

        Returns:
            JSON string representation of the summary
        """
        json_data = summary.to_dict()

        # Serialize to JSON
        if pretty:
            json_str = json.dumps(json_data, indent=2)
        else:
            json_str = json.dumps(json_data)

        # Write to file if path provided
        if output_path:
            path = Path(output_path)
            path.write_text(json_str, encoding="utf-8")

        return json_str

    @staticmethod
    def export_result(
        result: RuleResult,
        output_path: str | Path | None = None,
        pretty: bool = True,
    ) -> str:
        """Export single RuleResult to JSON format.

        Args:
            result: RuleResult to export
            output_path: Optional file path to write JSON
            pretty: Whether to pretty-print JSON (default: True)

        Returns:
            JSON string representation of the result
        """
        json_data = result.to_dict()

        # Serialize to JSON
        if pretty:
            json_str = json.dumps(json_data, indent=2)
        else:
            json_str = json.dumps(json_data)

        # Write to file if path provided
        if output_path:
            path = Path(output_path)
            path.write_text(json_str, encoding="utf-8")

        return json_str

    @staticmethod
    def load_summary(json_path: str | Path) -> dict[str, Any]:
        """Load ValidationSummary from JSON file.

        Args:
            json_path: Path to JSON file

        Returns:
            Dictionary containing the validation summary data
        """
        path = Path(json_path)
        json_str = path.read_text(encoding="utf-8")
        data: dict[str, Any] = json.loads(json_str)
        return data


__all__ = [
    "OutputFormatter",
    "JSONExporter",
]
