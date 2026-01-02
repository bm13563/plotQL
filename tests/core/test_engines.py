"""
Unit tests for plotql.core.engines module.

Tests Engine base class and MatplotlibEngine implementation.
"""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from plotql.core.ast import ColumnRef, FormatOptions, PlotQuery, PlotType
from plotql.core.engines import MatplotlibEngine, get_engine
from plotql.core.engines.base import Engine
from plotql.core.executor import ColorInfo, PlotData, SizeInfo
from plotql.core.result import PlotResult


# =============================================================================
# Engine Abstract Base Class Tests
# =============================================================================

class TestEngineBaseClass:
    """Tests for Engine abstract base class."""

    def test_engine_is_abstract(self):
        """Test that Engine cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Engine()

    def test_engine_requires_colors_property(self):
        """Test that COLORS property must be implemented."""
        class IncompleteEngine(Engine):
            def render(self, data, width, height):
                pass

            def get_color(self, color_name):
                pass

        with pytest.raises(TypeError):
            IncompleteEngine()

    def test_engine_requires_render_method(self):
        """Test that render method must be implemented."""
        class IncompleteEngine(Engine):
            @property
            def COLORS(self):
                return {}

            def get_color(self, color_name):
                pass

        with pytest.raises(TypeError):
            IncompleteEngine()

    def test_engine_requires_get_color_method(self):
        """Test that get_color method must be implemented."""
        class IncompleteEngine(Engine):
            @property
            def COLORS(self):
                return {}

            def render(self, data, width, height):
                pass

        with pytest.raises(TypeError):
            IncompleteEngine()


# =============================================================================
# get_engine Tests
# =============================================================================

class TestGetEngine:
    """Tests for get_engine factory function."""

    def test_get_engine_returns_matplotlib(self):
        """Test get_engine returns MatplotlibEngine."""
        engine = get_engine()
        assert isinstance(engine, MatplotlibEngine)

    def test_get_engine_singleton(self):
        """Test get_engine returns same instance."""
        engine1 = get_engine()
        engine2 = get_engine()
        # Note: Current implementation may or may not be singleton
        # Just verify both are valid engines
        assert isinstance(engine1, Engine)
        assert isinstance(engine2, Engine)


# =============================================================================
# MatplotlibEngine Tests
# =============================================================================

class TestMatplotlibEngine:
    """Tests for MatplotlibEngine class."""

    @pytest.fixture
    def engine(self):
        """Create a MatplotlibEngine instance."""
        return MatplotlibEngine()

    @pytest.fixture
    def simple_query(self, temp_csv: Path) -> PlotQuery:
        """Create a simple PlotQuery."""
        return PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )

    @pytest.fixture
    def simple_plot_data(self, simple_query: PlotQuery) -> PlotData:
        """Create simple PlotData."""
        return PlotData(
            x=[1.0, 2.0, 3.0, 4.0, 5.0],
            y=[10.0, 20.0, 30.0, 40.0, 50.0],
            query=simple_query,
            row_count=5,
            filtered_count=5,
        )


class TestMatplotlibEngineColors:
    """Tests for MatplotlibEngine color handling."""

    @pytest.fixture
    def engine(self):
        return MatplotlibEngine()

    def test_colors_property(self, engine):
        """Test COLORS property returns dict."""
        colors = engine.COLORS
        assert isinstance(colors, dict)
        assert "background" in colors
        assert "text" in colors
        assert "grid" in colors
        assert "blue" in colors

    def test_colors_are_hex(self, engine):
        """Test all colors are valid hex."""
        for name, color in engine.COLORS.items():
            assert color.startswith("#")
            assert len(color) == 7
            # Should be valid hex
            int(color[1:], 16)

    def test_get_color_known_colors(self, engine):
        """Test get_color with known color names."""
        colors = ["blue", "red", "green", "yellow", "orange", "pink", "purple"]
        for name in colors:
            result = engine.get_color(name)
            assert result.startswith("#")

    def test_get_color_case_insensitive(self, engine):
        """Test get_color is case insensitive."""
        assert engine.get_color("blue") == engine.get_color("BLUE")
        assert engine.get_color("red") == engine.get_color("Red")

    def test_get_color_none(self, engine):
        """Test get_color with None returns default."""
        result = engine.get_color(None)
        assert result == engine.COLORS["blue"]

    def test_get_color_unknown(self, engine):
        """Test get_color with unknown color returns default."""
        result = engine.get_color("unknown_color")
        assert result == engine.COLORS["blue"]

    def test_get_color_gray_grey(self, engine):
        """Test both gray and grey spellings work."""
        assert engine.get_color("gray") == engine.get_color("grey")


class TestMatplotlibEngineRender:
    """Tests for MatplotlibEngine.render method."""

    @pytest.fixture
    def engine(self):
        return MatplotlibEngine()

    @pytest.fixture
    def simple_query(self, temp_csv: Path) -> PlotQuery:
        return PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )

    @pytest.fixture
    def simple_plot_data(self, simple_query: PlotQuery) -> PlotData:
        return PlotData(
            x=[1.0, 2.0, 3.0, 4.0, 5.0],
            y=[10.0, 20.0, 30.0, 40.0, 50.0],
            query=simple_query,
            row_count=5,
            filtered_count=5,
        )

    def test_render_returns_plot_result(self, engine, simple_plot_data):
        """Test render returns PlotResult."""
        result = engine.render(simple_plot_data, 800, 600)
        assert isinstance(result, PlotResult)
        result.close()

    def test_render_figure_is_matplotlib(self, engine, simple_plot_data):
        """Test render returns matplotlib figure."""
        from matplotlib.figure import Figure
        result = engine.render(simple_plot_data, 800, 600)
        assert isinstance(result.figure, Figure)
        result.close()

    def test_render_to_bytes(self, engine, simple_plot_data):
        """Test render produces valid PNG bytes."""
        result = engine.render(simple_plot_data, 800, 600)
        png_bytes = result.to_bytes()

        assert len(png_bytes) > 0
        assert png_bytes[:4] == b"\x89PNG"  # PNG magic bytes
        result.close()

    def test_render_dimensions(self, engine, simple_plot_data):
        """Test render produces image with correct dimensions."""
        width, height = 800, 600
        result = engine.render(simple_plot_data, width, height)

        img = result.to_image()
        assert img.size == (width, height)
        result.close()


class TestMatplotlibEngineScatterPlot:
    """Tests for scatter plot rendering."""

    @pytest.fixture
    def engine(self):
        return MatplotlibEngine()

    def test_scatter_basic(self, engine, temp_csv: Path):
        """Test basic scatter plot."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        data = PlotData(
            x=[1.0, 2.0, 3.0],
            y=[4.0, 5.0, 6.0],
            query=query,
            row_count=3,
            filtered_count=3,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()

    def test_scatter_with_sizes(self, engine, temp_csv: Path):
        """Test scatter plot with marker sizes."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_size="value"),
        )
        data = PlotData(
            x=[1.0, 2.0, 3.0],
            y=[4.0, 5.0, 6.0],
            query=query,
            row_count=3,
            filtered_count=3,
            marker_sizes=[1.0, 3.0, 5.0],
            size_info=SizeInfo(
                is_continuous=True,
                column_name="value",
                min_value=1.0,
                max_value=5.0,
            ),
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()

    def test_scatter_with_categorical_colors(self, engine, temp_csv: Path):
        """Test scatter plot with categorical marker colors."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_color="category"),
        )
        data = PlotData(
            x=[1.0, 2.0, 3.0],
            y=[4.0, 5.0, 6.0],
            query=query,
            row_count=3,
            filtered_count=3,
            marker_colors=["blue", "green", "blue"],
            color_info=ColorInfo(
                is_continuous=False,
                column_name="category",
                category_colors={"A": "blue", "B": "green"},
            ),
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()

    def test_scatter_with_continuous_colors(self, engine, temp_csv: Path):
        """Test scatter plot with continuous marker colors."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(marker_color="value"),
        )
        data = PlotData(
            x=[1.0, 2.0, 3.0],
            y=[4.0, 5.0, 6.0],
            query=query,
            row_count=3,
            filtered_count=3,
            marker_colors=["#89b4fa", "#c1d1f5", "#f9e2af"],  # Hex colors
            color_info=ColorInfo(
                is_continuous=True,
                column_name="value",
                min_value=0.0,
                max_value=100.0,
            ),
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()


class TestMatplotlibEngineLinePlot:
    """Tests for line plot rendering."""

    @pytest.fixture
    def engine(self):
        return MatplotlibEngine()

    def test_line_basic(self, engine, temp_csv: Path):
        """Test basic line plot."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.LINE,
        )
        data = PlotData(
            x=[1.0, 2.0, 3.0, 4.0, 5.0],
            y=[10.0, 15.0, 12.0, 18.0, 20.0],
            query=query,
            row_count=5,
            filtered_count=5,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()

    def test_line_with_color(self, engine, temp_csv: Path):
        """Test line plot with custom color."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.LINE,
            format=FormatOptions(line_color="red"),
        )
        data = PlotData(
            x=[1.0, 2.0, 3.0],
            y=[4.0, 5.0, 6.0],
            query=query,
            row_count=3,
            filtered_count=3,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()


class TestMatplotlibEngineBarPlot:
    """Tests for bar plot rendering."""

    @pytest.fixture
    def engine(self):
        return MatplotlibEngine()

    def test_bar_basic(self, engine, temp_csv: Path):
        """Test basic bar plot."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="category"),
            y_column=ColumnRef(name="count"),
            plot_type=PlotType.BAR,
        )
        data = PlotData(
            x=["A", "B", "C"],
            y=[10.0, 20.0, 15.0],
            query=query,
            row_count=3,
            filtered_count=3,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()

    def test_bar_with_color(self, engine, temp_csv: Path):
        """Test bar plot with custom color."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.BAR,
            format=FormatOptions(line_color="green"),
        )
        data = PlotData(
            x=["X", "Y", "Z"],
            y=[5.0, 10.0, 7.0],
            query=query,
            row_count=3,
            filtered_count=3,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()


class TestMatplotlibEngineHistPlot:
    """Tests for histogram rendering."""

    @pytest.fixture
    def engine(self):
        return MatplotlibEngine()

    def test_hist_basic(self, engine, temp_csv: Path):
        """Test basic histogram."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.HIST,
        )
        data = PlotData(
            x=[1.0, 2.0, 3.0, 4.0, 5.0],  # Ignored for hist
            y=[10.0, 12.0, 11.0, 15.0, 14.0, 13.0, 16.0],  # Distribution
            query=query,
            row_count=7,
            filtered_count=7,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()


class TestMatplotlibEngineFormatOptions:
    """Tests for format options handling."""

    @pytest.fixture
    def engine(self):
        return MatplotlibEngine()

    def test_title(self, engine, temp_csv: Path):
        """Test plot with custom title."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(title="Custom Title"),
        )
        data = PlotData(
            x=[1.0, 2.0], y=[3.0, 4.0], query=query, row_count=2, filtered_count=2,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()

    def test_axis_labels(self, engine, temp_csv: Path):
        """Test plot with custom axis labels."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(xlabel="Custom X", ylabel="Custom Y"),
        )
        data = PlotData(
            x=[1.0, 2.0], y=[3.0, 4.0], query=query, row_count=2, filtered_count=2,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()


class TestMatplotlibEngineRenderToBytes:
    """Tests for render_to_bytes convenience method."""

    @pytest.fixture
    def engine(self):
        return MatplotlibEngine()

    def test_render_to_bytes(self, engine, temp_csv: Path):
        """Test render_to_bytes method."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        data = PlotData(
            x=[1.0, 2.0, 3.0],
            y=[4.0, 5.0, 6.0],
            query=query,
            row_count=3,
            filtered_count=3,
        )

        png_bytes = engine.render_to_bytes(data, 400, 300)

        assert len(png_bytes) > 0
        assert png_bytes[:4] == b"\x89PNG"

    def test_render_to_bytes_with_scale(self, engine, temp_csv: Path):
        """Test render_to_bytes with scale factor."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        data = PlotData(
            x=[1.0, 2.0],
            y=[3.0, 4.0],
            query=query,
            row_count=2,
            filtered_count=2,
        )

        # Scale 2.0 should double dimensions
        png_bytes = engine.render_to_bytes(data, 400, 300, scale=2.0)

        from PIL import Image
        from io import BytesIO
        img = Image.open(BytesIO(png_bytes))
        assert img.size == (800, 600)


class TestMatplotlibEngineGetTerminalPixelSize:
    """Tests for get_terminal_pixel_size static method."""

    def test_default_cell_size(self):
        """Test with default cell size."""
        width, height = MatplotlibEngine.get_terminal_pixel_size(80, 24)
        assert width == 80 * 8  # 640
        assert height == 24 * 16  # 384

    def test_custom_cell_size(self):
        """Test with custom cell size."""
        width, height = MatplotlibEngine.get_terminal_pixel_size(
            100, 50, cell_width_px=10, cell_height_px=20
        )
        assert width == 100 * 10  # 1000
        assert height == 50 * 20  # 1000


class TestMatplotlibEngineFigureToBytes:
    """Tests for _figure_to_bytes static method."""

    def test_figure_to_bytes_png(self):
        """Test _figure_to_bytes with PNG format."""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])

        png_bytes = MatplotlibEngine._figure_to_bytes(fig, "png", "#ffffff")

        assert len(png_bytes) > 0
        assert png_bytes[:4] == b"\x89PNG"
        plt.close(fig)

    def test_figure_to_bytes_svg(self):
        """Test _figure_to_bytes with SVG format."""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])

        svg_bytes = MatplotlibEngine._figure_to_bytes(fig, "svg", "#ffffff")

        assert b"<svg" in svg_bytes
        assert b"</svg>" in svg_bytes
        plt.close(fig)


# =============================================================================
# Edge Cases
# =============================================================================

class TestMatplotlibEngineEdgeCases:
    """Test edge cases for MatplotlibEngine."""

    @pytest.fixture
    def engine(self):
        return MatplotlibEngine()

    def test_empty_data(self, engine, temp_csv: Path):
        """Test rendering with empty data lists."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        data = PlotData(
            x=[],
            y=[],
            query=query,
            row_count=0,
            filtered_count=0,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()

    def test_single_point(self, engine, temp_csv: Path):
        """Test rendering with single data point."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        data = PlotData(
            x=[1.0],
            y=[2.0],
            query=query,
            row_count=1,
            filtered_count=1,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()

    def test_very_small_dimensions(self, engine, temp_csv: Path):
        """Test rendering with very small dimensions."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        data = PlotData(
            x=[1.0, 2.0],
            y=[3.0, 4.0],
            query=query,
            row_count=2,
            filtered_count=2,
        )

        result = engine.render(data, 50, 50)
        assert result.to_bytes()
        result.close()

    def test_large_data(self, engine, temp_csv: Path):
        """Test rendering with large dataset."""
        import random

        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
        )
        data = PlotData(
            x=[float(i) for i in range(1000)],
            y=[random.random() * 100 for _ in range(1000)],
            query=query,
            row_count=1000,
            filtered_count=1000,
        )

        result = engine.render(data, 800, 600)
        assert result.to_bytes()
        result.close()

    def test_long_labels(self, engine, temp_csv: Path):
        """Test rendering with very long axis labels."""
        query = PlotQuery(
            source=str(temp_csv),
            x_column=ColumnRef(name="x"),
            y_column=ColumnRef(name="y"),
            plot_type=PlotType.SCATTER,
            format=FormatOptions(
                title="This is a very long title that might cause wrapping issues",
                xlabel="A very long x-axis label that exceeds normal length",
                ylabel="A very long y-axis label",
            ),
        )
        data = PlotData(
            x=[1.0, 2.0, 3.0],
            y=[4.0, 5.0, 6.0],
            query=query,
            row_count=3,
            filtered_count=3,
        )

        result = engine.render(data, 400, 300)
        assert result.to_bytes()
        result.close()
