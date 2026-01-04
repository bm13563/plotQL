# Contributing to PlotQL

Thanks for your interest in contributing! This guide covers both the practical setup and the architectural principles that keep the codebase maintainable.

## Development Setup

### Requirements

- Python 3.10+
- Node.js (for tree-sitter grammar compilation)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### First-Time Setup

```bash
git clone https://github.com/your-username/plotql.git
cd plotql
./ctl.sh setup
source .venv/bin/activate
```

This will:
1. Create a Python 3.12 virtual environment
2. Install dependencies via `uv pip install -e .`
3. Build the tree-sitter grammar

### Control Script

The `ctl.sh` script handles common tasks:

```bash
./ctl.sh setup      # First-time setup
./ctl.sh compile    # Rebuild tree-sitter grammar
./ctl.sh test       # Quick smoke test
./ctl.sh run        # Launch the TUI
```

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Core only
python -m pytest tests/core/ -v

# UI only
python -m pytest tests/ui/ -v

# Specific test file
python -m pytest tests/core/test_parser.py -v
```

---

## Architecture

PlotQL has a strict separation between themes, core, and UI. Understanding this separation is essential for contributing.

### Module Structure

```
plotql/
├── themes/         # Centralized colors and fonts (standalone, no deps)
├── core/           # Language: parser, executor, AST
│   ├── connectors/ # Data source abstraction
│   └── engines/    # Rendering abstraction
└── ui/             # Textual TUI (one possible frontend)
```

### Dependency Graph

```
themes/  (standalone - no dependencies on core or ui)
   ↑
core/    (depends on themes for colors/fonts)
   ↑
ui/      (depends on core's public API and themes)
```

### Design Philosophy

#### Themes are Standalone

The `plotql/themes/` module defines all colors, fonts, and visual styling. It has no dependencies on core or UI. Both core (for rendering) and UI (for the interface) import from themes.

#### Core is UI-Agnostic

The `plotql/core/` module is a standalone library. It knows nothing about terminals, Textual, or any specific UI. It can be used by:

- Scripts
- Jupyter notebooks
- Web applications
- The TUI
- Any future interface

**Rule:** Core modules must never import from `plotql/ui/`.

#### UI Uses the Public API

The UI imports from `plotql.core` (the public API), not from internal submodules:

```python
# CORRECT - use public API
from plotql.core import parse, execute, get_engine, ParseError, ExecutionError

# WRONG - don't import internal modules
from plotql.core.parser import parse  # Avoid this
from plotql.core.executor import execute  # Avoid this
```

The public API is defined in `plotql/core/__init__.py` via `__all__`.

#### Interfaces, Not Implementations

Core defines abstract interfaces that implementations fulfill:

```
┌─────────────────────────────────────────────────────────┐
│                      plotql/core/                       │
│  ┌─────────┐   ┌──────────┐   ┌─────────┐   ┌───────┐  │
│  │ parser  │ → │ executor │ → │ engines │ → │ result│  │
│  └─────────┘   └──────────┘   └─────────┘   └───────┘  │
│                      ↑                                  │
│               ┌──────────────┐                         │
│               │  connectors  │                         │
│               └──────────────┘                         │
└─────────────────────────────────────────────────────────┘
                         ↑
                    Public API (plotql.core)
                         ↑
┌─────────────────────────────────────────────────────────┐
│                      plotql/ui/                         │
│              (consumes core like any user)              │
└─────────────────────────────────────────────────────────┘
```

#### Connectors

Connectors abstract data loading:

- `Connector` base class in `connectors/base.py`
- Implementations: `LiteralConnector`, `FileConnector`, `FolderConnector`, `ClickHouseConnector`
- Each returns a Polars DataFrame
- Connectors may support filter pushdown

**Adding a connector:**
1. Create `connectors/myconnector.py`
2. Extend `Connector` base class
3. Implement `validate_config()` and `load()`
4. Register in executor's connector routing logic

#### Engines

Engines abstract rendering:

- `Engine` base class in `engines/base.py`
- Implementations: `MatplotlibEngine`
- Each produces a `PlotResult`

**Adding an engine:**
1. Create `engines/myengine.py`
2. Extend `Engine` base class
3. Implement `COLORS`, `render()`, `get_color()`
4. Return a `PlotResult` wrapper

---

## Themes

**All colors and fonts are defined in `plotql/themes/`.** No colors should be hardcoded elsewhere.

### Theme Structure

```python
# themes/base.py - defines the PlotQLTheme dataclass
@dataclass(frozen=True)
class PlotQLTheme:
    name: str

    # Base colors
    background: str
    text: str
    # ... 20+ color properties

    # Chart palette
    chart_colors: Dict[str, str]
    gradient: List[str]
    color_map: Dict[str, str]

    # Fonts
    font_family: str
    font_stack: List[str]
```

```python
# themes/vaporwave.py - current theme implementation
THEME = PlotQLTheme(
    name="vaporwave",
    background="#1f1d2e",
    text="#e0def4",
    # ...
)
```

```python
# themes/__init__.py - exports active theme
from plotql.themes.vaporwave import THEME
```

### Using Theme Colors

```python
# In engines
from plotql.themes import THEME
bg_color = THEME.background

# In UI
from plotql.themes import THEME
style = Style(color=THEME.text, bgcolor=THEME.background)
```

### Adding a Theme

1. Create `themes/mytheme.py` with a `THEME = PlotQLTheme(...)` instance
2. Update `themes/__init__.py` to import your theme
3. All colors should be hex strings (`#rrggbb`)

---

## Tree-Sitter Grammar

PlotQL uses tree-sitter for syntax highlighting in the TUI.

### Files

```
plotql/grammar.json              # Source of truth for keywords, functions, operators
tree-sitter-plotql/
├── generate_grammar.py          # Generates grammar.js from grammar.json
├── grammar.js                   # Generated (don't edit directly)
├── queries/highlights.scm       # Syntax highlighting queries
└── src/
    ├── parser.c                 # Generated parser
    └── grammar.json             # Generated (by tree-sitter)
```

### Workflow

1. Edit `plotql/grammar.json` to add/modify keywords, functions, or operators
2. Run `./ctl.sh compile` to regenerate everything:
   - Runs `generate_grammar.py` to create `grammar.js`
   - Runs `npx tree-sitter generate` to create `parser.c`
   - Compiles the shared library

### Syntax Highlighting

Edit `tree-sitter-plotql/queries/highlights.scm` to change how tokens are highlighted:

```scheme
; Keywords get the @keyword capture
(with) @keyword
(plot) @keyword

; Functions get the @function capture
(aggregate_func) @function

; These map to theme colors in the TUI
```

The TUI maps captures to theme colors in `ui/tui.py`:

```python
syntax_styles={
    "keyword": Style(color=THEME.syntax_keyword),
    "function": Style(color=THEME.syntax_function),
    # ...
}
```

---

## Feature Checklist

When adding language features, ensure all of these are addressed:

### Core
- [ ] Parser handles new syntax (lexer tokens, grammar rules)
- [ ] AST types updated if needed (`core/ast.py`)
- [ ] Executor implements the behavior (`core/executor.py`)
- [ ] Tests in `tests/core/`

### Grammar
- [ ] Keywords/functions added to `plotql/grammar.json`
- [ ] Run `./ctl.sh compile`
- [ ] Highlighting queries updated (`tree-sitter-plotql/queries/highlights.scm`)

### UI
- [ ] Autocomplete updated (`ui/autocomplete.py`)
- [ ] Tests in `tests/ui/`

---

## Code Style

- **TDD:** Write tests first, then implement
- **No hardcoded colors:** Use theme values
- **Keep modules independent:** Core doesn't know about UI
- **Interface-based design:** Extend base classes for new connectors/engines
- **Polars for data:** All data manipulation uses Polars DataFrames

---

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes following the architecture principles
4. Add tests
5. Run `python -m pytest tests/ -v`
6. Submit a pull request

Please include:
- Clear description of what changed
- Which checklist items apply
- Any new dependencies
