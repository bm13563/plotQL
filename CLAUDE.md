# PlotQL

PlotQL is a SQL-like DSL for creating plots. Users write queries like:

```
WITH 'data.csv' PLOT price AGAINST time FILTER price > 100 FORMAT title = 'Price Chart'
```

## Architecture

**Core and UI are completely separate.** This separation is critical.

- `plotql/core/` - The language: parser, executor, rendering. This is a standalone library that can be used by any program (scripts, Jupyter, other packages).
- `plotql/ui/` - A Textual TUI that consumes core. Just one possible frontend.

Nothing should bleed between core and ui. Core knows nothing about the TUI. The UI imports and uses core's public API just like any other consumer would.

## Development

**Always use TDD.** Write tests first, then implement features.

```bash
python -m pytest tests/ -v
```

Tests mirror the architecture: `tests/core/` and `tests/ui/` are independent.

## Feature Checklist

When adding or modifying language features, ensure all of these are addressed:

### Core
- [ ] Parser handles new syntax (lexer tokens, grammar rules)
- [ ] AST types updated if needed
- [ ] Executor implements the behavior
- [ ] Grammar JSON updated and tree-sitter recompiled (`tree-sitter-plotql/`)
- [ ] Tests added to `tests/core/`

### UI
- [ ] Autocomplete updated (`plotql/ui/autocomplete.py`)
- [ ] Syntax highlighting queries updated (`tree-sitter-plotql/queries/highlights.scm`)
- [ ] Tests added to `tests/ui/`
