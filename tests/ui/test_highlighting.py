"""
Tests for PlotQL syntax highlighting via tree-sitter.

These tests verify that the tree-sitter grammar correctly parses PlotQL
queries and produces the expected node types for syntax highlighting.
"""
import sys
from pathlib import Path

import pytest

# Add tree-sitter-plotql to path
_TS_DIR = Path(__file__).parent.parent.parent / "tree-sitter-plotql"
sys.path.insert(0, str(_TS_DIR))

try:
    import tree_sitter_plotql as tsplotql
    from tree_sitter import Language, Parser
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False


@pytest.fixture
def parser():
    """Create a tree-sitter parser for PlotQL."""
    if not TREE_SITTER_AVAILABLE:
        pytest.skip("tree-sitter not available")
    lang = Language(tsplotql.language())
    return Parser(lang)


def get_node_types(parser, query: bytes) -> dict:
    """Parse a query and return a dict of text -> node_type mappings."""
    tree = parser.parse(query)

    result = {}

    def walk(node):
        # Only capture leaf nodes (terminals)
        if node.child_count == 0:
            text = query[node.start_byte:node.end_byte].decode()
            result[text] = node.type
        for child in node.children:
            walk(child)

    walk(tree.root_node)
    return result


class TestTreeSitterParsing:
    """Tests for tree-sitter grammar parsing."""

    def test_basic_query_parses(self, parser):
        """Test that a basic query parses without errors."""
        query = b"WITH source('data.csv') PLOT y AGAINST x"
        tree = parser.parse(query)
        assert tree.root_node.type == "query"
        assert not tree.root_node.has_error

    def test_string_in_source_is_highlighted(self, parser):
        """Test that strings inside source() are recognized as string nodes."""
        query = b"WITH source('data.csv') PLOT y AGAINST x"
        nodes = get_node_types(parser, query)
        assert nodes.get("'data.csv'") == "string"

    def test_multiple_strings_in_source(self, parser):
        """Test that multiple strings in source() are all recognized."""
        query = b"WITH source('db', 'table') PLOT y AGAINST x"
        nodes = get_node_types(parser, query)
        assert nodes.get("'db'") == "string"
        assert nodes.get("'table'") == "string"

    def test_string_in_filter(self, parser):
        """Test that strings in FILTER are recognized."""
        query = b"WITH source('data.csv') PLOT y AGAINST x FILTER col = 'value'"
        nodes = get_node_types(parser, query)
        assert nodes.get("'value'") == "string"

    def test_string_in_format(self, parser):
        """Test that strings in FORMAT are recognized."""
        query = b"WITH source('data.csv') PLOT y AGAINST x FORMAT title = 'My Plot'"
        nodes = get_node_types(parser, query)
        assert nodes.get("'My Plot'") == "string"

    def test_string_in_plot_type(self, parser):
        """Test that plot type strings are recognized."""
        query = b"WITH source('data.csv') PLOT y AGAINST x AS 'line'"
        nodes = get_node_types(parser, query)
        assert nodes.get("'line'") == "string"

    def test_double_quoted_strings(self, parser):
        """Test that double-quoted strings work."""
        query = b'WITH source("data.csv") PLOT y AGAINST x'
        nodes = get_node_types(parser, query)
        assert nodes.get('"data.csv"') == "string"

    def test_source_keyword_case_insensitive(self, parser):
        """Test that 'source' is recognized in any case."""
        for variant in [b"source", b"SOURCE", b"Source", b"SoUrCe"]:
            query = variant + b"('data.csv') PLOT y AGAINST x"
            query = b"WITH " + query
            tree = parser.parse(query)
            assert not tree.root_node.has_error, f"Failed for: {variant}"

    def test_all_keywords_case_insensitive(self, parser):
        """Test that all keywords work in lowercase."""
        query = b"with source('data.csv') plot y against x filter a = 1 format title = 'T'"
        tree = parser.parse(query)
        assert not tree.root_node.has_error

    def test_aggregate_functions_recognized(self, parser):
        """Test that aggregate functions are recognized."""
        for func in [b"count", b"sum", b"avg", b"min", b"max", b"median"]:
            query = b"WITH source('data.csv') PLOT " + func + b"(y) AGAINST x"
            tree = parser.parse(query)
            assert not tree.root_node.has_error, f"Failed for: {func}"
            nodes = get_node_types(parser, query)
            assert func.decode() in [k.lower() for k in nodes.keys() if nodes[k] == "aggregate_func"]

    def test_complex_query(self, parser):
        """Test a complex query with all features."""
        query = b"""
WITH source('local', '2024', 'data.csv')
PLOT price AGAINST time AS 'line'
FILTER symbol = 'AAPL' AND volume > 1000
FORMAT title = 'Stock Price' AND color = 'blue'
"""
        tree = parser.parse(query)
        assert not tree.root_node.has_error

        nodes = get_node_types(parser, query)
        # Check all strings are recognized
        assert nodes.get("'local'") == "string"
        assert nodes.get("'2024'") == "string"
        assert nodes.get("'data.csv'") == "string"
        assert nodes.get("'line'") == "string"
        assert nodes.get("'AAPL'") == "string"
        assert nodes.get("'Stock Price'") == "string"
        assert nodes.get("'blue'") == "string"
