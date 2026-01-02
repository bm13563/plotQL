#!/bin/bash
# PlotQL control script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TS_DIR="$SCRIPT_DIR/tree-sitter-plotql"

case "${1:-help}" in
    compile|build)
        echo "Compiling PlotQL tree-sitter grammar..."

        # Generate grammar.js from grammar.json
        python3 "$TS_DIR/generate_grammar.py"

        # Generate parser with tree-sitter-cli
        cd "$TS_DIR"
        npx tree-sitter generate

        # Compile shared library
        mkdir -p tree_sitter_plotql
        gcc -shared -fPIC -o tree_sitter_plotql/plotql.so src/parser.c -I src/

        echo "Done! PlotQL language compiled successfully."
        ;;

    test)
        echo "Testing PlotQL..."
        cd "$SCRIPT_DIR"
        source .venv/bin/activate
        python -c "
from plotql.parser import parse
q = parse(\"WITH 'test.csv' PLOT price AGAINST time\")
print(f'Parse OK: {q.source}')

from plotql.tui import PLOTQL_LANGUAGE, PLOTQL_HIGHLIGHTS
print(f'Highlighting: {\"enabled\" if PLOTQL_LANGUAGE else \"disabled\"}')
"
        ;;

    run|tui)
        cd "$SCRIPT_DIR"
        source .venv/bin/activate
        python -m plotql.tui "${@:2}"
        ;;

    setup)
        echo "Setting up PlotQL development environment..."
        cd "$SCRIPT_DIR"

        # Check for uv
        if ! command -v uv &> /dev/null; then
            echo "Error: uv not found. Install it from https://docs.astral.sh/uv/getting-started/installation/"
            exit 1
        fi

        # Create virtual environment with Python 3.12 and install dependencies
        echo "Creating virtual environment with Python 3.12 and installing dependencies..."
        uv venv --python 3.12
        uv pip install -e .

        # Check for tree-sitter CLI
        if ! command -v npx &> /dev/null; then
            echo "Warning: npx not found. Install Node.js for tree-sitter grammar compilation."
        else
            echo "Building tree-sitter grammar..."
            "$SCRIPT_DIR/ctl.sh" compile
        fi

        echo ""
        echo "Setup complete! To get started:"
        echo "  source .venv/bin/activate"
        echo "  ./ctl.sh run"
        ;;

    help|*)
        echo "PlotQL Control Script"
        echo ""
        echo "Usage: ./ctl.sh <command>"
        echo ""
        echo "Commands:"
        echo "  setup             First-time development setup"
        echo "  compile, build    Recompile the tree-sitter grammar"
        echo "  test              Run basic tests"
        echo "  run, tui          Launch the TUI"
        echo "  help              Show this help"
        ;;
esac
