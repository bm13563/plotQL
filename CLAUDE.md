# PlotQL

PlotQL is a SQL-like DSL for creating plots. Users write queries like:

```
WITH 'data.csv' PLOT price AGAINST time FILTER price > 100 FORMAT title = 'Price Chart'
```

Always start by reading the docs (README.md, CONTRIBUTING.md, /docs)

## Environment

Use the virtual environment in the project's root. Use uv. See ctl.sh for examples of how to work in the python environment.

## Development

**Always use TDD.** Write tests first, then implement features.

```bash
python -m pytest tests/ -v
```

Tests mirror the architecture: `tests/core/` and `tests/ui/` are independent. There are a lot of tests, so it's worth working out which ones are relevant to the feature being implemented and only running those.

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

## Docs
- [ ] Any relevant docs reviewed and updated
