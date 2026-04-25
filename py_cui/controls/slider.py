import py_cui.ui
import py_cui.widgets
import py_cui.popups
import py_cui.errors
import py_cui.keys


class SliderImplementation(py_cui.ui.UIImplementation):

    def __init__(self, min_val: int, max_val: int, init_val: int, step: int, logger):
        pass


    def set_bar_char(self, char: str) -> None:
        """
        Updates the character used to represent the slider bar.

        Parameters
        ----------
        char : str
            Character to represent progressive bar.
        """
        pass


    def update_slider_value(self, offset: int) -> float:
        """
        Steps up or down the value in offset fashion.

        Parameters
        ----------
        offset : int
            Number of steps to increase or decrease the slider value.

        Returns
        -------
        self._cur_val: float
            Current slider value.
        """
        pass


    def get_slider_value(self) -> float:
        """
        Returns current slider value.

        Returns
        -------
        self._cur_val: float
            Current slider value.
        """
        pass


    def set_slider_step(self, step: int) -> None:
        """
        Changes the step value.

        Parameters
        ----------
        step : int
            Step size of the slider.
        """
        pass


class SliderWidget(py_cui.widgets.Widget, SliderImplementation):
    """
    Widget for a Slider

    Parameters
    ----------
    min_val : int
        Lowest value of the slider
    max_val: int
        Highest value of the slider
    step : int
        Increment from low to high value
    init_val:
        Initial value of the slider
    """

    def __init__(self, id, title, grid, row, column, row_span, column_span,
                 padx, pady, logger, min_val, max_val, step, init_val):

        SliderImplementation.__init__(self, min_val, max_val, init_val, step, logger)

        py_cui.widgets.Widget.__init__(self, id, title, grid, row, column,
                                       row_span, column_span, padx,
                                       pady, logger, selectable=True)

        self._title_enabled = True
        self._border_enabled = True
        self._display_value = True
        self._alignment = "mid"
        self.set_help_text("Focus mode on Slider. Use left/right to adjust value. Esc to exit.")


    def toggle_title(self) -> None:
        """Toggles visibility of the widget's name.
        """
        pass


    def toggle_border(self) -> None:
        """Toggles visibility of the widget's border.
        """
        pass


    def toggle_value(self) -> None:
        """Toggles visibility of the widget's current value in integer.
        """
        pass


    def align_to_top(self) -> None:
        """Aligns widget height to top.
        """
        pass


    def align_to_middle(self) -> None:
        """Aligns widget height to middle. default configuration.
        """
        pass


    def align_to_bottom(self) -> None:
        """Aligns widget height to bottom.
        """
        pass


    def _custom_draw_with_border(self, start_y: int, content: str) -> None:
        """
        Custom method made from renderer.draw_border to support alignment for bordered variants.

        Parameters
        ----------
        start_y : int
            border's Y-axis starting coordination
        content: str
            string to be drawn inside the border
        """
        pass


    def _generate_bar(self, width: int) -> str:
        """
        Internal implementation to generate progression bar.

        Parameters
        ----------
        width : int
            Width of bar in character length.

        Returns
        -------
        progress: str
            progressive bar string  with length of width.
        """
        pass


    def _draw(self) -> None:
        """Override of base class draw function.
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """
        LEFT_ARROW decreases value, RIGHT_ARROW increases.

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """
        pass


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int):
        """Override of base class handle mouse press function

        Parameters
        ----------
        x : int
            x-position of the mouse event in the terminal
        y : int
            y position of the mouse event in the terminal
        mouse_event : int
            Mouse event type code
        """
        pass


class SliderPopup(py_cui.popups.Popup, SliderImplementation):
    pass
