"""
Unit tests for plotql.core.result module.

Tests PlotResult wrapper for rendered plot output.
"""
from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest


from plotql.core.result import PlotResult


# =============================================================================
# PlotResult Creation Tests
# =============================================================================

class TestPlotResultCreation:
    """Tests for PlotResult initialization."""

    @pytest.fixture
    def mock_figure(self):
        """Create a mock figure object."""
        return MagicMock(name="MockFigure")

    @pytest.fixture
    def mock_callbacks(self):
        """Create mock callback functions."""
        return {
            "save_func": MagicMock(),
            "to_bytes_func": MagicMock(return_value=b"PNG_DATA"),
            "show_func": MagicMock(),
            "close_func": MagicMock(),
        }

    def test_init(self, mock_figure, mock_callbacks):
        """Test PlotResult initialization."""
        result = PlotResult(
            figure=mock_figure,
            **mock_callbacks,
        )

        assert result._figure == mock_figure
        assert result._save_func == mock_callbacks["save_func"]
        assert result._to_bytes_func == mock_callbacks["to_bytes_func"]
        assert result._show_func == mock_callbacks["show_func"]
        assert result._close_func == mock_callbacks["close_func"]


# =============================================================================
# PlotResult.figure Tests
# =============================================================================

class TestPlotResultFigure:
    """Tests for PlotResult.figure property."""

    def test_figure_property(self):
        """Test accessing figure property."""
        mock_figure = MagicMock()
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=MagicMock(),
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        assert result.figure == mock_figure

    def test_figure_is_readonly(self):
        """Test that figure property has no setter."""
        mock_figure = MagicMock()
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=MagicMock(),
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        with pytest.raises(AttributeError):
            result.figure = MagicMock()


# =============================================================================
# PlotResult.to_bytes Tests
# =============================================================================

class TestPlotResultToBytes:
    """Tests for PlotResult.to_bytes method."""

    def test_to_bytes_default_format(self):
        """Test to_bytes with default format (png)."""
        mock_figure = MagicMock()
        to_bytes_func = MagicMock(return_value=b"PNG_DATA")
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=to_bytes_func,
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        data = result.to_bytes()

        to_bytes_func.assert_called_once_with(mock_figure, "png")
        assert data == b"PNG_DATA"

    def test_to_bytes_svg_format(self):
        """Test to_bytes with SVG format."""
        mock_figure = MagicMock()
        to_bytes_func = MagicMock(return_value=b"<svg></svg>")
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=to_bytes_func,
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        data = result.to_bytes(format="svg")

        to_bytes_func.assert_called_once_with(mock_figure, "svg")
        assert data == b"<svg></svg>"

    def test_to_bytes_pdf_format(self):
        """Test to_bytes with PDF format."""
        mock_figure = MagicMock()
        to_bytes_func = MagicMock(return_value=b"%PDF-1.4")
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=to_bytes_func,
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        data = result.to_bytes(format="pdf")

        to_bytes_func.assert_called_once_with(mock_figure, "pdf")


# =============================================================================
# PlotResult.to_image Tests
# =============================================================================

class TestPlotResultToImage:
    """Tests for PlotResult.to_image method."""

    def test_to_image_returns_pil_image(self):
        """Test to_image returns PIL Image."""
        # Create actual PNG bytes for a minimal 1x1 image
        from PIL import Image
        import io

        # Create a minimal valid PNG
        img = Image.new("RGB", (1, 1), color="red")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png_bytes = buf.getvalue()

        mock_figure = MagicMock()
        to_bytes_func = MagicMock(return_value=png_bytes)
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=to_bytes_func,
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        img_result = result.to_image()

        assert isinstance(img_result, Image.Image)
        to_bytes_func.assert_called_once_with(mock_figure, "png")


# =============================================================================
# PlotResult.save Tests
# =============================================================================

class TestPlotResultSave:
    """Tests for PlotResult.save method."""

    def test_save_calls_save_func(self):
        """Test save calls the save function."""
        mock_figure = MagicMock()
        save_func = MagicMock()
        result = PlotResult(
            figure=mock_figure,
            save_func=save_func,
            to_bytes_func=MagicMock(),
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        result.save("/path/to/plot.png")

        save_func.assert_called_once_with(mock_figure, "/path/to/plot.png", None)

    def test_save_with_format(self):
        """Test save with explicit format."""
        mock_figure = MagicMock()
        save_func = MagicMock()
        result = PlotResult(
            figure=mock_figure,
            save_func=save_func,
            to_bytes_func=MagicMock(),
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        result.save("/path/to/plot.svg", format="svg")

        save_func.assert_called_once_with(mock_figure, "/path/to/plot.svg", "svg")


# =============================================================================
# PlotResult.show Tests
# =============================================================================

class TestPlotResultShow:
    """Tests for PlotResult.show method."""

    def test_show_calls_show_func(self):
        """Test show calls the show function."""
        mock_figure = MagicMock()
        show_func = MagicMock()
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=MagicMock(),
            show_func=show_func,
            close_func=MagicMock(),
        )

        result.show()

        show_func.assert_called_once_with(mock_figure)


# =============================================================================
# PlotResult.close Tests
# =============================================================================

class TestPlotResultClose:
    """Tests for PlotResult.close method."""

    def test_close_calls_close_func(self):
        """Test close calls the close function."""
        mock_figure = MagicMock()
        close_func = MagicMock()
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=MagicMock(),
            show_func=MagicMock(),
            close_func=close_func,
        )

        result.close()

        close_func.assert_called_once_with(mock_figure)


# =============================================================================
# PlotResult Jupyter Support Tests
# =============================================================================

class TestPlotResultJupyter:
    """Tests for Jupyter notebook display support."""

    def test_repr_png(self):
        """Test _repr_png_ for Jupyter PNG display."""
        mock_figure = MagicMock()
        to_bytes_func = MagicMock(return_value=b"PNG_DATA")
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=to_bytes_func,
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        png_data = result._repr_png_()

        to_bytes_func.assert_called_once_with(mock_figure, "png")
        assert png_data == b"PNG_DATA"

    def test_repr_svg(self):
        """Test _repr_svg_ for Jupyter SVG display."""
        mock_figure = MagicMock()
        svg_bytes = b"<svg>test</svg>"
        to_bytes_func = MagicMock(return_value=svg_bytes)
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=to_bytes_func,
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        svg_str = result._repr_svg_()

        to_bytes_func.assert_called_once_with(mock_figure, "svg")
        assert svg_str == "<svg>test</svg>"


# =============================================================================
# PlotResult __repr__ Tests
# =============================================================================

class TestPlotResultRepr:
    """Tests for PlotResult string representation."""

    def test_repr(self):
        """Test __repr__ includes figure type."""
        mock_figure = MagicMock()
        mock_figure.__class__.__name__ = "Figure"
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=MagicMock(),
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        repr_str = repr(result)

        assert "PlotResult" in repr_str
        assert "MagicMock" in repr_str or "Figure" in repr_str


# =============================================================================
# Integration with Matplotlib Tests
# =============================================================================

class TestPlotResultWithMatplotlib:
    """Integration tests with actual matplotlib figures."""

    @pytest.fixture
    def matplotlib_figure(self):
        """Create a real matplotlib figure."""
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        return fig

    def test_with_real_figure(self, matplotlib_figure):
        """Test PlotResult with real matplotlib figure."""
        import matplotlib.pyplot as plt
        from io import BytesIO

        def save_func(fig, path, fmt):
            fig.savefig(path, format=fmt)

        def to_bytes_func(fig, fmt):
            buf = BytesIO()
            fig.savefig(buf, format=fmt)
            buf.seek(0)
            return buf.read()

        def show_func(fig):
            pass  # Don't actually show in tests

        def close_func(fig):
            plt.close(fig)

        result = PlotResult(
            figure=matplotlib_figure,
            save_func=save_func,
            to_bytes_func=to_bytes_func,
            show_func=show_func,
            close_func=close_func,
        )

        # Test to_bytes
        png_data = result.to_bytes()
        assert len(png_data) > 0
        assert png_data[:4] == b"\x89PNG"  # PNG magic bytes

        # Test to_image
        img = result.to_image()
        assert img.size[0] > 0
        assert img.size[1] > 0

        # Cleanup
        result.close()

    def test_svg_output_with_real_figure(self, matplotlib_figure):
        """Test SVG output with real matplotlib figure."""
        import matplotlib.pyplot as plt
        from io import BytesIO

        def to_bytes_func(fig, fmt):
            buf = BytesIO()
            fig.savefig(buf, format=fmt)
            buf.seek(0)
            return buf.read()

        result = PlotResult(
            figure=matplotlib_figure,
            save_func=MagicMock(),
            to_bytes_func=to_bytes_func,
            show_func=MagicMock(),
            close_func=lambda f: plt.close(f),
        )

        svg_data = result.to_bytes(format="svg")
        assert b"<svg" in svg_data
        assert b"</svg>" in svg_data

        result.close()


# =============================================================================
# Edge Cases
# =============================================================================

class TestPlotResultEdgeCases:
    """Test edge cases and error conditions."""

    def test_to_bytes_with_failing_function(self):
        """Test error handling when to_bytes_func fails."""
        mock_figure = MagicMock()
        to_bytes_func = MagicMock(side_effect=Exception("Render error"))
        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=to_bytes_func,
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        with pytest.raises(Exception) as exc_info:
            result.to_bytes()
        assert "Render error" in str(exc_info.value)

    def test_save_with_failing_function(self):
        """Test error handling when save_func fails."""
        mock_figure = MagicMock()
        save_func = MagicMock(side_effect=IOError("Cannot write file"))
        result = PlotResult(
            figure=mock_figure,
            save_func=save_func,
            to_bytes_func=MagicMock(),
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        with pytest.raises(IOError) as exc_info:
            result.save("/invalid/path/plot.png")
        assert "Cannot write file" in str(exc_info.value)

    def test_multiple_to_bytes_calls(self):
        """Test multiple to_bytes calls work correctly."""
        mock_figure = MagicMock()
        call_count = 0

        def to_bytes_func(fig, fmt):
            nonlocal call_count
            call_count += 1
            return f"DATA_{fmt}_{call_count}".encode()

        result = PlotResult(
            figure=mock_figure,
            save_func=MagicMock(),
            to_bytes_func=to_bytes_func,
            show_func=MagicMock(),
            close_func=MagicMock(),
        )

        data1 = result.to_bytes("png")
        data2 = result.to_bytes("svg")
        data3 = result.to_bytes("png")

        assert data1 == b"DATA_png_1"
        assert data2 == b"DATA_svg_2"
        assert data3 == b"DATA_png_3"
