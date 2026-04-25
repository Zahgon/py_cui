"""Module containing all core widget classes for py_cui.

Widgets are the basic building blocks of a user interface made with py_cui.
This module contains classes for:

* Base Widget class
* Label
* Block Label
* Scroll Menu
* Checkbox Menu
* Button
* TextBox
* Text Block
* Slider

Additional widgets should be added in appropriate sub-modules, importing this
file and extending the base Widget class, or if appropriate one of the other core widgets.
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019


import curses
import inspect
import py_cui
import py_cui.ui
import py_cui.colors
import py_cui.errors
import py_cui.debug

from typing import Union, Callable, List, Dict, Tuple, Any, Optional


class Widget(py_cui.ui.UIElement):
    """Top Level Widget Base Class

    Extended by all widgets. Contains base classes for handling key presses, drawing,
    and setting status bar text.

    Attributes
    ----------
    _grid : py_cui.grid.Grid
        The parent grid object of the widget
    _row, _column : int
        row and column position of the widget
    _row_span, _column_span : int
        number of rows or columns spanned by the widget
    _selectable : bool
        Flag that says if a widget can be selected
    _key_commands : dict
        Dictionary mapping key codes to functions
    _text_color_rules : List[py_cui.ColorRule]
        color rules to load into renderer when drawing widget
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, selectable: bool = True):
        """Initializer for base widget class

        Class UIElement superclass initializer, and then assigns widget to grid, along with row/column info
        and color rules and key commands
        """

        super().__init__(id, title, None, logger)
        if grid is None:
            raise py_cui.errors.PyCUIMissingParentError("Cannot add widget to NoneType")

        self._grid = grid
        grid_rows, grid_cols = self._grid.get_dimensions()
        if (grid_cols < column + column_span) or (grid_rows < row + row_span):
            raise py_cui.errors.PyCUIOutOfBoundsError(f"Target grid too small for widget {title}")

        self._row          = row
        self._column       = column
        self._row_span     = row_span
        self._column_span  = column_span
        self._padx         = padx
        self._pady         = pady
        self._selectable       = selectable
        self._key_commands: Dict[int,Callable[[],Any]]     = {}
        self._mouse_commands: Dict[int,Callable[[],Any]]   = {}
        self._text_color_rules: List['py_cui.ColorRule'] = []
        self._default_color = py_cui.WHITE_ON_BLACK
        self._border_color = self._default_color
        self.update_height_width()

        self._move_focus_map = {}
        for mouse_event in py_cui.keys.MOUSE_EVENTS:
            self._move_focus_map[mouse_event] = False

        self._context_menu = None


    def _get_parent_ui(self):
        """Function used to get reference to parent UI instance for interfacing with popups and context menus
        """
        pass


    def add_key_command(self, key: Union[int, List[int]], command: Callable[[],Any]) -> None:
        """Maps a keycode to a function that will be executed when in focus mode

        Parameters
        ----------
        key : py_cui.keys.KEY_*
            ascii keycode used to map the key
        command : function without args
            a non-argument function or lambda function to execute if in focus mode and key is pressed
        """
        pass


    def add_mouse_command(self, mouse_event: int, command: Callable[[],Any], move_focus = False) -> None:
        """Maps a keycode to a function that will be executed when in focus mode

        Parameters
        ----------
        key : py_cui.keys.MOUSE_EVENT
            Mouse event code from py_cui.keys
        command : Callable
            a non-argument function or lambda function to execute if in focus mode and key is pressed

        Raises
        ------
        PyCUIError
            If input mouse event code is not valid
        """
        pass


    def update_key_command(self, key: Union[int, List[int]], command: Callable[[],Any]) -> Any:
        """Maps a keycode to a function that will be executed when in focus mode, if key is already mapped

        Parameters
        ----------
        key : py_cui.keys.KEY_*
            ascii keycode used to map the key
        command : function without args
            a non-argument function or lambda function to execute if in focus mode and key is pressed
        """
        pass


    def add_text_color_rule(self, regex: str, color: int, rule_type: str, match_type: str='line', region: List[int]=[0,1], include_whitespace: bool=False, selected_color=None) -> None:
        """Forces renderer to draw text using given color if text_condition_function returns True

        Parameters
        ----------
        regex : str
            A string to check against the line for a given rule type
        color : int
            a supported py_cui color value
        rule_type : string
            A supported color rule type
        match_type='line' : str
            sets match type. Can be 'line', 'regex', or 'region'
        region=[0,1] : [int, int]
            A specified region to color if using match_type='region'
        include_whitespace : bool
            if false, strip string before checking for match
        """
        pass


    def clear_color_rules(self):
        """Removes all configured color rules for the widget
        """
        pass


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Gets the absolute position of the widget in characters. Override of base class function

        Returns
        -------
        x_pos, y_pos : int
            position of widget in terminal
        """
        pass


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Gets the absolute dimensions of the widget in characters. Override of base class function

        Returns
        -------
        width, height : int
            dimensions of widget in terminal
        """
        pass


    def get_grid_cell(self) -> Tuple[int,int]:
        """Gets widget row, column in grid

        Returns
        -------
        row, column : int
            Initial row and column placement for widget in grid
        """
        pass


    def get_grid_cell_spans(self) -> Tuple[int,int]:
        """Gets widget row span, column span in grid

        Returns
        -------
        row_span, column_span : int
            Initial row span and column span placement for widget in grid
        """
        pass


    def set_selectable(self, selectable: bool) -> None:
        """Setter for widget selectablility

        Paramters
        ---------
        selectable : bool
            Widget selectable if true, otherwise not
        """
        pass


    def is_selectable(self) -> bool:
        """Checks if the widget is selectable

        Returns
        -------
        selectable : bool
            True if selectable, false otherwise
        """
        pass


    def _is_row_col_inside(self, row: int, col: int) -> bool:
        """Checks if a particular row + column is inside the widget area

        Parameters
        ----------
        row, col : int
            row and column position to check

        Returns
        -------
        is_inside : bool
            True if row, col is within widget bounds, false otherwise
        """
        pass


    # BELOW FUNCTIONS SHOULD BE OVERWRITTEN BY SUB-CLASSES


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int):
        """Base class function that handles all assigned mouse presses.

        When overwriting this function, make sure to add a super()._handle_mouse_press(x, y, mouse_event) call,
        as this is required for user defined key command support

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Base class function that handles all assigned key presses.

        When overwriting this function, make sure to add a super()._handle_key_press(key_pressed) call,
        as this is required for user defined key command support

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        pass


    def _draw(self) -> None:
        """Base class draw class that checks if renderer is valid.

        Should be called with super()._draw() in overrides.
        Also intializes color rules, so if not called color rules will not be applied
        """
        pass


class Label(Widget):
    """The most basic subclass of Widget.

    Simply displays one centered row of text. Has no unique attributes or methods

    Attributes
    ----------
    draw_border : bool
        Toggle for drawing label border
    """

    def __init__(self, id, title: str,  grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger):
        """Initalizer for Label widget
        """

        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger, selectable=False)
        self._draw_border = False


    def toggle_border(self) -> None:
        """Function that gives option to draw border around label
        """
        pass


    def _draw(self) -> None:
        """Override base draw class.

        Center text and draw it
        """
        pass


class BlockLabel(Widget):
    """A Variation of the label widget that renders a block of text.

    Attributes
    ----------
    lines : list of str
        list of lines that make up block text
    center : bool
        Decides whether or not label should be centered
    """

    def __init__(self, id, title: str,  grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger: py_cui.debug.PyCUILogger, center: bool):
        """Initializer for blocklabel widget
        """

        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger, selectable=False)
        self._lines        = title.splitlines()
        self._center       = center
        self._draw_border  = False


    def set_title(self, title: str) -> None:
        """Override of base class, splits title into lines for rendering line by line.

        Parameters
        ----------
        title : str
            The new title for the block label object.
        """
        pass


    def toggle_border(self) -> None:
        """Function that gives option to draw border around label
        """
        pass


    def _draw(self) -> None:
        """Override base draw class.

        Center text and draw it
        """
        pass


class ScrollMenu(Widget, py_cui.ui.MenuImplementation):
    """A scroll menu widget.
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger: 'py_cui.debug.PyCUILogger'):
        """Initializer for scroll menu. calls superclass initializers and sets help text
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.MenuImplementation.__init__(self, logger)
        self.set_help_text('Focus mode on ScrollMenu. Use Up/Down/PgUp/PgDown/Home/End to scroll, Esc to exit.')


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int):
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """
        pass



    def _handle_key_press(self, key_pressed: int) -> None:
        """Override base class function.

        UP_ARROW scrolls up, DOWN_ARROW scrolls down.

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        pass


    def add_item(self, item):
        """Override of add_item function, allows for sticking to bottom

        Parameters
        ----------
        item : Object
            Object to add to the menu. Must have implemented __str__ function
        """
        pass


    def _draw(self) -> None:
        """Overrides base class draw function
        """
        pass


class CheckBoxMenu(Widget, py_cui.ui.CheckBoxMenuImplementation):
    """Extension of ScrollMenu that allows for multiple items to be selected at once.

    Attributes
    ----------
    selected_item_list : list of str
        List of checked items
    checked_char : char
        Character to represent a checked item
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, checked_char: str):
        """Initializer for CheckBoxMenu Widget
        """

        Widget.__init__(self,id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.CheckBoxMenuImplementation.__init__(self, logger, checked_char)
        self.set_help_text('Focus mode on CheckBoxMenu. Use up/down to scroll, Enter to toggle set, unset, Esc to exit.')


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of key presses.

        First, run the superclass function, scrolling should still work.
        Adds Enter command to toggle selection

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """
        pass


    def _draw(self) -> None:
        """Overrides base class draw function
        """
        pass


class RadioMenu(CheckBoxMenu):

    def __init__(self, *args):
        super.__init__(args)

    def toggle_item_checked(self, item: Any):

        pass

    def mark_item_as_checked(self, item: Any) -> None:
        pass


    def mark_item_as_not_checked(self, item) -> None:
        pass


class DropdownMenu(Widget, py_cui.ui.DropdownMenuImplementation):


    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, max_height: int):
        """Initializer for CheckBoxMenu Widget
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.DropdownMenuImplementation.__init__(self, logger, max_height)
        self.set_help_text('Focus mode on Dropdown. Use up/down to scroll. Use Enter to open, Backspace to close, arrows to navigate.')

        self._selected_from_dropdown = None

        # Shift focus to dropdown in event of click or double click.
        self._move_focus_map[py_cui.keys.LEFT_MOUSE_CLICK] = True
        self._move_focus_map[py_cui.keys.LEFT_MOUSE_DBL_CLICK] = True


    def update_height_width(self) -> None:
        pass


    def set_selected_dropdown_option(self, item):
        pass


    def get_selected_dropdown_option(self):
        pass


    def _get_actual_max_height(self):

        pass


    def _get_render_text(self):
        pass


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of key presses.

        First, run the superclass function, scrolling should still work.
        Adds Enter command to toggle selection

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """
        pass


    def _draw(self) -> None:
        """Overrides base class draw function
        """
        pass


class Button(Widget):
    """Basic button widget.

    Allows for running a command function on Enter

    Attributes
    ----------
    command : function
        A no-args function to run when the button is pressed.
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, command: Optional[Callable[[],Any]]):
        """Initializer for Button Widget
        """

        super().__init__(id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        self.command = command
        self.set_color(py_cui.MAGENTA_ON_BLACK)
        self.set_help_text('Focus mode on Button. Press Enter to press button, Esc to exit focus mode.')

        # By default we will process command on click or double click
        if self.command is not None:
            self.add_mouse_command(py_cui.keys.LEFT_MOUSE_CLICK, self.command)
            self.add_mouse_command(py_cui.keys.LEFT_MOUSE_DBL_CLICK, self.command)


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class, adds ENTER listener that runs the button's command

        Parameters
        ----------
        key_pressed : int
            Key code of pressed key
        """
        pass


    def _draw(self) -> None:
        """Override of base class draw function
        """
        pass



class TextBox(Widget, py_cui.ui.TextBoxImplementation):
    """Widget for entering small single lines of text
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, initial_text: str, password: bool):
        """Initializer for TextBox widget. Uses TextBoxImplementation as base
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.TextBoxImplementation.__init__(self, initial_text, password, logger)
        self.update_height_width()
        self.set_help_text('Focus mode on TextBox. Press Esc to exit focus mode.')

        # Shift focus to textbox in event of click or double click.
        self._move_focus_map[py_cui.keys.LEFT_MOUSE_CLICK] = True
        self._move_focus_map[py_cui.keys.LEFT_MOUSE_DBL_CLICK] = True


    def update_height_width(self) -> None:
        """Need to update all cursor positions on resize
        """
        pass


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base handle key press function

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        pass


    def _draw(self) -> None:
        """Override of base draw function
        """
        pass


class ScrollTextBlock(Widget, py_cui.ui.TextBlockImplementation):
    """Widget for editing large multi-line blocks of text
    """

    def __init__(self, id, title: str, grid: 'py_cui.grid.Grid', row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, logger, initial_text: str):
        """Initializer for TextBlock Widget. Uses TextBlockImplementation as base
        """

        Widget.__init__(self, id, title, grid, row, column, row_span, column_span, padx, pady, logger)
        py_cui.ui.TextBlockImplementation.__init__(self, initial_text, logger)
        self.update_height_width()
        self.set_help_text('Focus mode on TextBlock. Press Esc to exit focus mode.')

        # Shift focus to text block in event of click or double click.
        self._move_focus_map[py_cui.keys.LEFT_MOUSE_CLICK] = True
        self._move_focus_map[py_cui.keys.LEFT_MOUSE_DBL_CLICK] = True


    def update_height_width(self) -> None:
        """Function that updates the position of the text and cursor on resize
        """
        pass


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class handle key press function

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        pass


    def _draw(self) -> None:
        """Override of base class draw function
        """
        pass


