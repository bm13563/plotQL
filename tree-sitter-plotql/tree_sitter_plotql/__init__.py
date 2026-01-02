"""
Tree-sitter PlotQL language bindings.

Usage:
    import tree_sitter_plotql as tsplotql
    from tree_sitter import Language

    PLOTQL_LANGUAGE = Language(tsplotql.language())
"""
from pathlib import Path
from ctypes import cdll, c_void_p

_ROOT = Path(__file__).parent
_LIB_PATH = _ROOT / "plotql.so"

def language() -> int:
    """Return a pointer to the tree-sitter PlotQL language."""
    lib = cdll.LoadLibrary(str(_LIB_PATH))
    lib.tree_sitter_plotql.restype = c_void_p
    return lib.tree_sitter_plotql()
