"""
CLI entry point for PlotQL.

Usage:
    plotql                    # Launch interactive TUI
    plotql -q "WITH ..."      # Execute query and show in TUI
    plotql script.pql         # Run queries from file
"""

import argparse
import sys
from typing import Optional


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="plotql",
        description="SQL-like DSL for terminal plotting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  plotql                              Launch interactive TUI
  plotql -q "WITH 'data.csv' PLOT y AGAINST x"
  plotql script.pql                   Run from file

Query Syntax:
  WITH 'file.csv'
  PLOT y_column AGAINST x_column AS 'line'
  FILTER column = 'value' AND column > 10
  FORMAT line_color = 'red' AND title = 'My Plot'

Keybindings:
  F5            Execute query
  Ctrl+Q        Quit
        """,
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="Query file to execute (.pql)",
    )
    parser.add_argument(
        "-q", "--query",
        help="Query string to execute",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    # Get query from file or argument
    query: Optional[str] = None
    if args.file:
        try:
            with open(args.file) as f:
                query = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
    elif args.query:
        query = args.query

    # Launch TUI
    from plotql.ui import run_tui
    run_tui(query)
    return 0


if __name__ == "__main__":
    sys.exit(main())
