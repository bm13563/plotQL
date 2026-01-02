"""
Autocomplete provider for PlotQL queries.

Provides context-aware completions for keywords, functions, columns,
and file paths.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import polars as pl


@dataclass
class Completion:
    """A single autocomplete suggestion."""
    text: str
    display: str
    kind: str  # "keyword", "function", "column", "type"

    def __str__(self) -> str:
        return self.text


# PlotQL keywords
KEYWORDS = [
    "WITH", "PLOT", "AGAINST", "AS", "FILTER", "FORMAT", "AND", "OR", "NOT",
]

# Aggregate functions
FUNCTIONS = [
    "count", "sum", "avg", "min", "max", "median",
]

# Connector functions
CONNECTORS = [
    "file", "clickhouse",
]

# Plot types
PLOT_TYPES = [
    "'scatter'", "'line'", "'bar'", "'hist'",
]

# Format options
FORMAT_OPTIONS = [
    "title", "xlabel", "ylabel", "color", "line_color", "marker_color", "marker_size", "marker",
]

# Color options for plotext
COLOR_OPTIONS = [
    "red", "green", "blue", "yellow", "cyan", "magenta", "white", "black",
    "orange", "gray", "grey",
]


def get_context(text: str, cursor_pos: int) -> Tuple[str, str, Optional[str]]:
    """
    Determine the completion context based on cursor position.

    Returns:
        A tuple of (context_type, partial_word, plot_type)
        Context types reflect valid next tokens in the grammar.
        plot_type is extracted if present in the query.
    """
    # Get text before cursor
    before = text[:cursor_pos]

    # Get the partial word being typed (include path chars for file completion)
    word_match = re.search(r"[a-zA-Z0-9_./'-]*$", before)
    partial = word_match.group(0) if word_match else ""

    # Determine context by analyzing what's been typed
    before_upper = before.upper()
    before_stripped = before.rstrip()

    # Extract plot type if present (for filtering format options)
    # For multi-series, get the plot type from the LAST/current series
    plot_type_matches = list(re.finditer(r"\bAS\s+['\"](\w+)['\"]", before, re.IGNORECASE))
    detected_plot_type = plot_type_matches[-1].group(1).lower() if plot_type_matches else None

    # Check if we're inside an aggregate function (e.g., count(|) )
    agg_match = re.search(r"\b(count|sum|avg|min|max|median)\(\s*([a-zA-Z_]*)?$", before, re.IGNORECASE)
    if agg_match:
        partial_col = agg_match.group(2) or ""
        return ("agg_column", partial_col, detected_plot_type)

    # Check if we're inside a connector function (e.g., file(|) or clickhouse(|) )
    connector_match = re.search(r"\b(file|clickhouse)\(\s*([a-zA-Z_]*)?$", before, re.IGNORECASE)
    if connector_match:
        connector_type = connector_match.group(1).lower()
        partial_alias = connector_match.group(2) or ""
        return ("connector_alias", partial_alias, detected_plot_type, connector_type)

    # Check if we're inside a string after WITH (file path context)
    with_match = re.search(r"WITH\s+['\"]([^'\"]*?)$", before, re.IGNORECASE)
    if with_match:
        return ("file_path", with_match.group(1), detected_plot_type)

    # For multi-series support, find the last PLOT keyword and work from there
    # This isolates context to the current series being typed
    last_plot_match = None
    for m in re.finditer(r"\bPLOT\b", before_upper):
        last_plot_match = m

    # Determine text context for current series (after last PLOT, or full text if no PLOT yet)
    if last_plot_match:
        current_series_start = last_plot_match.start()
        current_series = before[current_series_start:]
        current_series_upper = current_series.upper()
    else:
        current_series = before
        current_series_upper = before_upper

    # Check for FORMAT context - only within the current series
    if "FORMAT" in current_series_upper:
        last_format = current_series_upper.rfind("FORMAT")
        after_format = current_series[last_format:]

        # Check if we're typing a new word after a complete FORMAT value on a new line
        # This handles: FORMAT color = 'peach'\nPL (typing PLOT for new series)
        format_value_then_newword = re.search(
            r"FORMAT\s+\w+\s*=\s*(?:'[^']*'|\"[^\"]*\"|\w+)(?:\s+AND\s+\w+\s*=\s*(?:'[^']*'|\"[^\"]*\"|\w+))*\s*[\n\r]+\s*[a-zA-Z]+$",
            current_series, re.IGNORECASE
        )
        if format_value_then_newword:
            # User is typing a new keyword after FORMAT on a new line - treat as after_format
            return ("after_format", partial, detected_plot_type)

        # Check if FORMAT clause looks complete (has key = value and ends with space/newline)
        # Pattern: FORMAT key = value (with possible AND key = value chains)
        format_complete = re.search(
            r"FORMAT\s+(\w+\s*=\s*(?:'[^']*'|\"[^\"]*\"|\w+)(?:\s+AND\s+\w+\s*=\s*(?:'[^']*'|\"[^\"]*\"|\w+))*)\s+$",
            current_series, re.IGNORECASE
        )
        if format_complete:
            # FORMAT clause is complete - suggest PLOT for new series, AND for more format options
            return ("after_format", partial, detected_plot_type)

        # After = sign, check what kind of value is expected
        eq_match = re.search(r"(\w+)\s*=\s*[^=]*$", after_format)
        if eq_match:
            key = eq_match.group(1).lower()
            # Check if we just finished a value (after AND)
            if re.search(r"AND\s*$", after_format.upper()):
                return ("format_key", partial, detected_plot_type)
            # For color options, suggest color literals
            if key in ("color", "colour", "line_color", "line_colour", "marker_color", "marker_colour"):
                return ("format_color", partial, detected_plot_type)
            # For marker_size, suggest column names (for dynamic sizing)
            if key in ("marker_size", "size"):
                return ("format_size", partial, detected_plot_type)
            # For title/labels, don't autocomplete - user types their own string
            # Return none so no popup appears
            return ("none", partial, detected_plot_type)
        return ("format_key", partial, detected_plot_type)

    # Check for AS context (plot type)
    if re.search(r"\bAS\s+$", before_upper) or re.search(r"\bAS\s+['\"]?[a-z]*$", before, re.IGNORECASE):
        # After AS, only plot types are valid
        return ("plot_type", partial, detected_plot_type)

    # Check for FILTER context
    if "FILTER" in before_upper:
        last_filter = before_upper.rfind("FILTER")
        after_filter = before[last_filter:]
        # After operator, suggest values
        if re.search(r"[<>=!]+\s*[^<>=!]*$", after_filter) and not re.search(r"\b(AND|OR)\s*$", after_filter.upper()):
            return ("filter_value", partial, detected_plot_type)
        # After AND/OR in filter, suggest columns
        if re.search(r"\b(AND|OR)\s*$", after_filter.upper()):
            return ("filter_column", partial, detected_plot_type)
        # After column name, suggest operators
        if re.search(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*$", after_filter) and not re.search(r"FILTER\s*$", after_filter.upper()):
            return ("filter_op", partial, detected_plot_type)
        return ("filter_column", partial, detected_plot_type)

    # After AS + plot type (complete), suggest FILTER or FORMAT
    if re.search(r"\bAS\s+['\"][a-z]+['\"]\s*$", before, re.IGNORECASE):
        return ("after_plot_type", partial, detected_plot_type)

    # After AGAINST + column, suggest AS or FILTER or FORMAT
    if re.search(r"AGAINST\s+[a-zA-Z_][a-zA-Z0-9_()]*\s+$", before_upper):
        return ("after_against_col", partial, detected_plot_type)

    # After AGAINST, suggest columns
    if re.search(r"AGAINST\s*$", before_upper):
        return ("column", partial, detected_plot_type)

    # After PLOT + column, suggest AGAINST
    if re.search(r"PLOT\s+[a-zA-Z_][a-zA-Z0-9_()]*\s+$", before_upper):
        return ("after_plot_col", partial, detected_plot_type)

    # After PLOT, suggest columns/aggregates
    if re.search(r"PLOT\s*$", before_upper):
        return ("column", partial, detected_plot_type)

    # After WITH + quoted string, suggest PLOT
    if re.search(r"WITH\s+['\"][^'\"]+['\"]\s*$", before, re.IGNORECASE):
        return ("after_with", partial, detected_plot_type)

    # After WITH + connector call (e.g., "WITH file(trades) "), suggest PLOT
    if re.search(r"WITH\s+(file|clickhouse)\([a-zA-Z_][a-zA-Z0-9_]*\)\s*$", before, re.IGNORECASE):
        return ("after_with", partial, detected_plot_type)

    # After WITH, can type quote for file path OR connector function
    if re.search(r"WITH\s*$", before_upper):
        return ("after_with_source", partial, detected_plot_type)

    # Typing a connector name after WITH (e.g., "WITH fi")
    if re.search(r"WITH\s+[a-zA-Z]+$", before, re.IGNORECASE) and not re.search(r"WITH\s+['\"]", before):
        return ("after_with_source", partial, detected_plot_type)

    # Empty or start - also handle newlines after complete statements
    if not before_stripped or before_stripped.upper() == partial.upper():
        return ("start", partial, detected_plot_type)

    # Check if we're at start of a new line/section after a complete clause
    # This handles typing at start of new lines (e.g., typing "FOR" on a new line)
    # Remove the partial word from the end to see what's before it
    if partial:
        # Strip the partial word we're typing from the end
        text_before_partial = before[:-len(partial)].rstrip()
    else:
        text_before_partial = before_stripped

    text_before_partial_upper = text_before_partial.upper()

    # After a complete plot type declaration, suggest FILTER or FORMAT
    if re.search(r"AS\s+['\"][a-z]+['\"]$", text_before_partial, re.IGNORECASE):
        return ("after_plot_type", partial, detected_plot_type)

    # After complete AGAINST column, suggest AS/FILTER/FORMAT
    if re.search(r"AGAINST\s+[a-zA-Z_][a-zA-Z0-9_()]*$", text_before_partial_upper):
        return ("after_against_col", partial, detected_plot_type)

    # After PLOT + column, suggest AGAINST
    if re.search(r"PLOT\s+[a-zA-Z_][a-zA-Z0-9_()]*$", text_before_partial_upper):
        return ("after_plot_col", partial, detected_plot_type)

    # After PLOT (no column yet), suggest columns
    if re.search(r"PLOT$", text_before_partial_upper):
        return ("column", partial, detected_plot_type)

    # After AGAINST (no column yet), suggest columns
    if re.search(r"AGAINST$", text_before_partial_upper):
        return ("column", partial, detected_plot_type)

    # After complete WITH 'file', suggest PLOT
    if re.search(r"WITH\s+['\"][^'\"]+['\"]$", text_before_partial, re.IGNORECASE):
        return ("after_with", partial, detected_plot_type)

    return ("none", partial, detected_plot_type)


def get_file_completions(partial_path: str, limit: int = 10) -> List[Completion]:
    """
    Get file path completions.

    Args:
        partial_path: The partial path typed so far
        limit: Maximum number of suggestions

    Returns:
        List of file path completions
    """
    completions = []

    # Determine the directory to search and the prefix to match
    if not partial_path:
        search_dir = Path(".")
        prefix = ""
    elif partial_path.endswith("/"):
        search_dir = Path(partial_path)
        prefix = ""
    else:
        search_dir = Path(partial_path).parent
        prefix = Path(partial_path).name
        if str(search_dir) == ".":
            search_dir = Path(".")

    # Supported file extensions
    data_extensions = {".csv", ".parquet", ".json", ".ndjson"}

    try:
        if not search_dir.exists():
            return completions

        for entry in sorted(search_dir.iterdir()):
            name = entry.name

            # Skip hidden files
            if name.startswith("."):
                continue

            # Match prefix
            if prefix and not name.lower().startswith(prefix.lower()):
                continue

            # Build the completion path
            if str(search_dir) == ".":
                completion_path = name
            else:
                completion_path = str(search_dir / name)

            if entry.is_dir():
                # Add trailing slash for directories
                completions.append(Completion(
                    text=completion_path + "/",
                    display=name + "/",
                    kind="directory"
                ))
            elif entry.suffix.lower() in data_extensions:
                completions.append(Completion(
                    text=completion_path + "'",
                    display=name,
                    kind="file"
                ))

            if len(completions) >= limit:
                break

    except PermissionError:
        pass

    return completions


def extract_file_path(text: str) -> Optional[str]:
    """Extract the file path from a WITH clause."""
    match = re.search(r"WITH\s+['\"]([^'\"]+)['\"]", text, re.IGNORECASE)
    return match.group(1) if match else None


def get_columns_from_file(file_path: str) -> List[str]:
    """Load column names from a data file."""
    try:
        # Try to infer file type and load just the schema
        if file_path.endswith(".csv"):
            df = pl.read_csv(file_path, n_rows=0)
        elif file_path.endswith(".parquet"):
            df = pl.read_parquet(file_path, n_rows=0)
        elif file_path.endswith(".json"):
            df = pl.read_json(file_path)
        elif file_path.endswith(".ndjson"):
            df = pl.read_ndjson(file_path, n_rows=1)
        else:
            # Default to CSV
            df = pl.read_csv(file_path, n_rows=0)
        return df.columns
    except Exception:
        return []


class AutoCompleter:
    """
    Context-aware autocomplete provider for PlotQL.

    Caches column names from the data file for performance.
    """

    def __init__(self):
        self._cached_path: Optional[str] = None
        self._cached_columns: List[str] = []

    def get_completions(
        self,
        text: str,
        cursor_pos: int,
        limit: int = 10
    ) -> List[Completion]:
        """
        Get autocomplete suggestions for the current cursor position.

        Args:
            text: The full query text
            cursor_pos: The cursor position (character offset)
            limit: Maximum number of suggestions

        Returns:
            List of Completion objects
        """
        context_result = get_context(text, cursor_pos)

        # get_context returns 3-tuple normally, 4-tuple for connector_alias
        if len(context_result) == 4:
            context, partial, detected_plot_type, connector_type = context_result
        else:
            context, partial, detected_plot_type = context_result
            connector_type = None

        partial_upper = partial.upper()
        partial_lower = partial.lower()

        completions: List[Completion] = []

        # Update column cache if file changed
        file_path = extract_file_path(text)
        if file_path and file_path != self._cached_path:
            self._cached_path = file_path
            self._cached_columns = get_columns_from_file(file_path)

        if context == "start":
            # Only WITH is valid at start
            if "WITH".startswith(partial_upper) or not partial:
                completions.append(Completion("WITH", "WITH", "keyword"))

        elif context == "need_quote":
            # After WITH, need to type a quote (backward compat)
            completions.append(Completion("'", "' (open quote)", "syntax"))

        elif context == "after_with_source":
            # After WITH, suggest connectors or quote for literal path
            for conn in CONNECTORS:
                if conn.startswith(partial_lower) or not partial:
                    completions.append(Completion(f"{conn}(", conn, "connector"))
            if not partial or "'".startswith(partial):
                completions.append(Completion("'", "' (file path)", "syntax"))

        elif context == "file_path":
            # File path completions (no quotes needed, they're already there)
            return get_file_completions(partial, limit)

        elif context == "after_with":
            # After file path, only PLOT is valid
            if "PLOT".startswith(partial_upper) or not partial:
                completions.append(Completion("PLOT", "PLOT", "keyword"))

        elif context == "column":
            # Suggest columns and aggregate functions
            for col in self._cached_columns:
                if col.lower().startswith(partial_lower) or not partial:
                    completions.append(Completion(col, col, "column"))

            for func in FUNCTIONS:
                if func.startswith(partial_lower) or not partial:
                    completions.append(Completion(f"{func}(", func, "function"))

        elif context == "agg_column":
            # Inside aggregate function - suggest columns only
            for col in self._cached_columns:
                if col.lower().startswith(partial_lower) or not partial:
                    completions.append(Completion(col + ")", col, "column"))

        elif context == "connector_alias":
            # Inside connector function - suggest aliases from config
            try:
                from plotql.core.config import list_aliases
                if connector_type:
                    aliases = list_aliases(connector_type)
                    for alias in aliases:
                        if alias.lower().startswith(partial_lower) or not partial:
                            completions.append(Completion(alias + ")", alias, "alias"))
            except Exception:
                # Config not available or error - no completions
                pass

        elif context == "after_plot_col":
            # After PLOT column, only AGAINST is valid
            if "AGAINST".startswith(partial_upper) or not partial:
                completions.append(Completion("AGAINST", "AGAINST", "keyword"))

        elif context == "after_against_col":
            # After AGAINST column, AS/FILTER/FORMAT/PLOT are valid
            # PLOT starts a new series
            for kw in ["AS", "FILTER", "FORMAT", "PLOT"]:
                if kw.startswith(partial_upper) or not partial:
                    completions.append(Completion(kw, kw, "keyword"))

        elif context == "after_plot_type":
            # After AS 'type', FILTER/FORMAT/PLOT are valid
            # PLOT starts a new series
            for kw in ["FILTER", "FORMAT", "PLOT"]:
                if kw.startswith(partial_upper) or not partial:
                    completions.append(Completion(kw, kw, "keyword"))

        elif context == "plot_type":
            # After AS, only plot types are valid
            for ptype in PLOT_TYPES:
                inner = ptype.strip("'")
                if inner.startswith(partial_lower.strip("'")) or not partial:
                    completions.append(Completion(ptype, ptype, "type"))

        elif context == "filter_column":
            # Suggest columns for filter conditions
            for col in self._cached_columns:
                if col.lower().startswith(partial_lower) or not partial:
                    completions.append(Completion(col, col, "column"))

        elif context == "filter_op":
            # Suggest comparison operators
            for op in ["=", "!=", "<", "<=", ">", ">="]:
                completions.append(Completion(op, op, "operator"))

        elif context == "filter_value":
            # Suggest columns or common values
            for col in self._cached_columns:
                if col.lower().startswith(partial_lower) or not partial:
                    completions.append(Completion(col, col, "column"))
            # Also suggest AND/OR/FORMAT/PLOT to continue
            for kw in ["AND", "OR", "FORMAT", "PLOT"]:
                if kw.startswith(partial_upper) or not partial:
                    completions.append(Completion(kw, kw, "keyword"))

        elif context == "format_key":
            # Suggest format options - filtered by plot type
            valid_options = self._get_valid_format_options(detected_plot_type)
            for opt in valid_options:
                if opt.lower().startswith(partial_lower) or not partial:
                    completions.append(Completion(opt, opt, "keyword"))

        elif context == "format_color":
            # Suggest color literals
            for color in COLOR_OPTIONS:
                if color.startswith(partial_lower) or not partial:
                    completions.append(Completion(f"'{color}'", color, "value"))
            # Also suggest column names for dynamic colors
            for col in self._cached_columns:
                if col.lower().startswith(partial_lower) or not partial:
                    completions.append(Completion(col, col, "column"))

        elif context == "format_size":
            # Suggest column names for dynamic sizing
            for col in self._cached_columns:
                if col.lower().startswith(partial_lower) or not partial:
                    completions.append(Completion(col, col, "column"))

        elif context == "after_format":
            # After FORMAT value, can add more options with AND or start new series with PLOT
            for kw in ["AND", "PLOT"]:
                if kw.startswith(partial_upper) or not partial:
                    completions.append(Completion(kw, kw, "keyword"))

        # Filter and sort completions
        seen = set()
        unique = []
        for c in completions:
            if c.text not in seen:
                seen.add(c.text)
                unique.append(c)

        # Sort: prioritize by context, then by prefix match, then alphabetically
        def sort_key(c: Completion) -> Tuple[int, int, str]:
            # In column context, prioritize columns and functions over keywords
            if context == "column":
                kind_order = {"column": 0, "function": 1, "keyword": 2, "type": 3}
            else:
                kind_order = {"keyword": 0, "function": 1, "column": 2, "type": 3}
            is_prefix = 0 if c.text.lower().startswith(partial_lower) else 1
            return (is_prefix, kind_order.get(c.kind, 99), c.text.lower())

        unique.sort(key=sort_key)

        return unique[:limit]

    def _get_valid_format_options(self, plot_type: Optional[str]) -> List[str]:
        """
        Get format options valid for the given plot type.

        Args:
            plot_type: The detected plot type (scatter, line, bar, hist) or None

        Returns:
            List of valid format option names
        """
        # Universal options (valid for all plot types)
        universal = ["title", "xlabel", "ylabel"]

        # Scatter-only options
        scatter_only = ["marker_color", "marker_size"]

        # Line/bar options
        line_bar_options = ["line_color", "color"]

        if plot_type == "scatter":
            return universal + scatter_only + ["color"]
        elif plot_type in ("line", "bar"):
            return universal + line_bar_options
        elif plot_type == "hist":
            return universal + ["color", "line_color"]
        else:
            # Unknown or no plot type - show all options
            return FORMAT_OPTIONS

    def invalidate_cache(self) -> None:
        """Clear the column cache."""
        self._cached_path = None
        self._cached_columns = []
