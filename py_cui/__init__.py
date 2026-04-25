"""A python library for intuitively creating CUI/TUI interfaces with pre-built widgets.
"""

#
# Author:   Jakub Wlodek
# Created:  12-Aug-2019
# Docs:     https://jwlodek.github.io/py_cui-docs
# License:  BSD-3-Clause (New/Revised)
#

# Some python core library imports
import sys
import os
import time
import copy
import shutil  # We use shutil for getting the terminal dimensions
import threading  # Threading is used for loading icon popups
import logging  # Use logging library for debug purposes


# py_cui uses the curses library. On windows this does not exist, but
# there is a open source windows-curses module that adds curses support
# for python on windows
import curses
from typing import Any, Union, Callable, List, Dict, Optional, Tuple

# py_cui imports
import py_cui
import py_cui.keys
import py_cui.statusbar
import py_cui.widgets
import py_cui.controls
import py_cui.dialogs
import py_cui.widget_set
import py_cui.popups
import py_cui.renderer
import py_cui.debug
import py_cui.errors
from py_cui.colors import *

# Version number
__version__ = "0.1.6"


def fit_text(width: int, text: str, center: bool = False) -> str:
    """Fits text to screen size

    Helper function to fit text within a given width. Used to fix issue with status/title bar text
    being too long

    Parameters
    ----------
    width : int
        width of window in characters
    text : str
        input text
    center : Boolean
        flag to center text

    Returns
    -------
    fitted_text : str
        text fixed depending on width
    """
    pass


class PyCUI:
    """Base CUI class

    Main user interface class for py_cui. To create a user interface, you must
    first create an instance of this class, and then add cells + widgets to it.

    Attributes
    ----------
    cursor_x, cursor_y : int
        absolute position of the cursor in the CUI
    grid : py_cui.grid.Grid
        The main layout manager for the CUI
    widgets : dict of str - py_cui.widgets.Widget
        dict of widget in the grid
    title_bar : py_cui.statusbar.StatusBar
        a status bar object that gets drawn at the top of the CUI
    status_bar : py_cui.statusbar.StatusBar
        a status bar object that gets drawn at the bottom of the CUI
    keybindings : list of py_cui.keybinding.KeyBinding
        list of keybindings to check against in the main CUI loop
    height, width : int
        height of the terminal in characters, width of terminal in characters
    exit_key : key_code
        a key code for a key that exits the CUI
    simulated_terminal : List[int]
        Dimensions for an alternative simulated terminal (used for testing)
    """

    def __init__(
        self,
        num_rows: int,
        num_cols: int,
        auto_focus_buttons: bool = True,
        exit_key=py_cui.keys.KEY_Q_LOWER,
        simulated_terminal: List[int] = None,
    ):
        """Initializer for PyCUI class"""

        self._title = "PyCUI Window"

        # When this is not set, the escape character delay
        # is too long for exiting focus mode
        os.environ.setdefault("ESCDELAY", "25")

        # For unit testing purposes, we want to simulate terminal
        # dimensions so that we don't get errors
        self._simulated_terminal = simulated_terminal

        if self._simulated_terminal is None:
            term_size = shutil.get_terminal_size()
            height = term_size.lines
            width = term_size.columns
        else:
            height = self._simulated_terminal[0]
            width = self._simulated_terminal[1]

        # Curses supports up to 256 color pairs. Outside of the default color pairs (56 total combos)
        # Allow user to customize remaining 200
        self._num_color_pairs = 56
        self._available_color_pairs = 200
        self._color_map = py_cui.colors._COLOR_MAP

        # Data structure mapping color combos to pair code for faster lookup
        self._reverse_color_map = {}
        for i in range(56):
            self._reverse_color_map[self._color_map[i+1]] = i+1

        # Add status and title bar
        self.title_bar = py_cui.statusbar.StatusBar(
            self._title, BLACK_ON_WHITE, root=self, is_title_bar=True
        )
        exit_key_char = py_cui.keys.get_char_from_ascii(exit_key)

        if exit_key_char:
            self._init_status_bar_text = (
                f"Press - {exit_key_char} - to exit. Arrow "
                "Keys to move between widgets. Enter to "
                "enter focus mode."
            )
        else:
            self._init_status_bar_text = (
                "Press arrow Keys to move between widgets. " "Enter to enter focus mode."
            )
        self.status_bar = py_cui.statusbar.StatusBar(
            self._init_status_bar_text, BLACK_ON_WHITE, root=self
        )

        # Init terminal height width. Subtract 4 from height
        # for title/status bar and padding
        self._height = height
        self._width = width
        self._height = (
            self._height - self.title_bar.get_height() - self.status_bar.get_height() - 2
        )

        # Logging object initialization for py_cui
        self._logger = py_cui.debug._initialize_logger(self, name="py_cui")

        # Initialize grid, renderer, and widget dict
        self._grid = py_cui.grid.Grid(
            self, num_rows, num_cols, self._height, self._width, self._logger
        )
        self._stdscr: Any = None
        self._refresh_timeout = -1
        self._border_characters: Optional[Dict[str, str]] = None
        self._widgets: Dict[int, Optional["py_cui.widgets.Widget"]] = {}
        self._renderer: Optional["py_cui.renderer.Renderer"] = None

        # Variables for determining selected widget/focus mode
        self._selected_widget: Optional[int] = None
        self._in_focused_mode = False
        self._popup: Any = None
        self._auto_focus_buttons = auto_focus_buttons

        # CUI blocks when loading popup is open
        self._loading = False
        self._stopped = False
        self._post_loading_callback: Optional[Callable[[], Any]] = None
        self._on_draw_update_func: Optional[Callable[[], Any]] = None

        # Top level keybindings. Exit key is 'q' by default
        self._keybindings: Dict[int, Callable[[], Any]] = {}
        self._exit_key = exit_key
        self._forward_cycle_key = py_cui.keys.KEY_CTRL_LEFT
        self._reverse_cycle_key = py_cui.keys.KEY_CTRL_RIGHT
        self._toggle_live_debug_key: Optional[int] = None

        # Callback to fire when CUI is stopped.
        self._on_stop: Optional[Callable[[], Any]] = None

    def add_color_pair(self, foreground_color: int, bkgd_color: int):
        pass

    def get_color_code(self, foreground_color: int, bkgd_color: int) -> int:

        pass

    def set_refresh_timeout(self, timeout: int):
        """Sets the CUI auto-refresh timeout to a number of seconds.

        Parameters
        ----------
        timeout : int
            Number of seconds to wait before refreshing the CUI
        """
        pass

    def set_on_draw_update_func(self, update_function: Callable[[], Any]):
        """Adds a function that is fired during each draw call of the CUI

        Parameters
        ----------
        update_function : function
            A no-argument or lambda function that is fired at the start of each draw call
        """
        pass

    def set_widget_cycle_key(
        self, forward_cycle_key: int = None, reverse_cycle_key: int = None
    ) -> None:
        """Assigns a key for automatically cycling through widgets in both focus and overview modes

        Parameters
        ----------
        widget_cycle_key : py_cui.keys.KEY
            Key code for key to cycle through widgets
        """
        pass

    def set_toggle_live_debug_key(self, toggle_debug_key: int) -> None:
        """Sets the keybinding for opening/closing popup debug log.

        Parameters
        ----------
        toggle_debug_key : py_cui.keys.KEY
            Key code for debug log open/close toggle
        """
        pass

    def enable_logging(
        self,
        log_file_path: str = "py_cui.log",
        logging_level=logging.DEBUG,
        live_debug_key: int = py_cui.keys.KEY_CTRL_D,
    ) -> None:
        """Function enables logging for py_cui library

        Parameters
        ----------
        log_file_path : str
            The target log filepath. Default 'py_cui_log.txt
        logging_level : int
            Default logging level = logging.DEBUG
        """
        pass

    def apply_widget_set(self, new_widget_set: py_cui.widget_set.WidgetSet) -> None:
        """Function that replaces all widgets in a py_cui with those of a different widget set

        Parameters
        ----------
        new_widget_set : WidgetSet
            The new widget set to switch to

        Raises
        ------
        TypeError
            If input is not of type WidgetSet
        """
        pass

    def create_new_widget_set(
        self, num_rows: int, num_cols: int
    ) -> "py_cui.widget_set.WidgetSet":
        """Function that is used to create additional widget sets

        Use this function instead of directly creating widget set object instances, to allow
        for logging support.

        Parameters
        ----------
        num_rows : int
            row count for new widget set
        num_cols : int
            column count for new widget set

        Returns
        -------
        new_widget_set : py_cui.widget_set.WidgetSet
            The new widget set object instance
        """
        pass

    # ----------------------------------------------#
    # Initialization functions                      #
    # Used to initialzie CUI and its features       #
    # ----------------------------------------------#

    def start(self) -> None:
        """Function that starts the CUI"""
        pass

    def stop(self) -> None:
        """Function that stops the CUI, and fires the callback function.

        Callback must be a no arg method
        """
        pass

    def run_on_exit(self, command: Callable[[], Any]):
        """Sets callback function on CUI exit. Must be a no-argument function or lambda function

        Parameters
        ----------
        command : function
            A no-argument or lambda function to be fired on exit
        """
        pass

    def set_title(self, title: str) -> None:
        """Sets the title bar text

        Parameters
        ----------
        title : str
            New title for CUI
        """
        pass

    def set_status_bar_text(self, text: str) -> None:
        """Sets the status bar text when in overview mode

        Parameters
        ----------
        text : str
            Status bar text
        """
        pass

    def _initialize_colors(self) -> None:
        """Function for initialzing curses colors. Called when CUI is first created."""
        pass

    def _initialize_widget_renderer(self) -> None:
        """Function that creates the renderer object that will draw each widget"""
        pass

    def toggle_unicode_borders(self) -> None:
        """Function for toggling unicode based border rendering"""
        pass

    def set_widget_border_characters(
        self,
        upper_left_corner: str,
        upper_right_corner: str,
        lower_left_corner: str,
        lower_right_corner: str,
        horizontal: str,
        vertical: str,
    ) -> None:
        """Function that can be used to set arbitrary border characters for drawing widget borders by renderer.

        Parameters
        ----------
        upper_left_corner : char
            Upper left corner character
        upper_right_corner : char
            Upper right corner character
        lower_left_corner : char
            Upper left corner character
        lower_right_corner : char
            Lower right corner character
        horizontal : char
            Horizontal border character
        vertical : char
            Vertical border character
        """
        pass

    def get_widgets(self) -> Dict[int, Optional["py_cui.widgets.Widget"]]:
        """Function that gets current set of widgets

        Returns
        -------
        widgets : dict of int -> widget
            dictionary mapping widget IDs to object instances
        """
        pass

    # Widget add functions. Each of these adds a particular type of widget
    # to the grid in a specified location.

    def add_custom_widget(self, widget_class: type, title: str, row: int, column: int, row_span: int, column_span: int, padx: int, pady: int, *args, **kwargs) -> 'py_cui.widgets.Widget':
        """Function that allows for adding custom widget types to the CUI - specifically ones not included with py_cui by default

        Parameters
        ----------
        widget_class : type
            The class type of your custom widget. Note that it must be a subclass of the widget superclass
        title : str
            The title of the scroll menu
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction

        Raises
        ------
        TypeError
            If provided widget class is not a subclass of widget, a typeerror is raised.
        """
        pass



    def add_scroll_menu(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
        padx: int = 1,
        pady: int = 0,
    ) -> "py_cui.widgets.ScrollMenu":
        """Function that adds a new scroll menu to the CUI grid

        Parameters
        ----------
        title : str
            The title of the scroll menu
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction

        Returns
        -------
        new_scroll_menu : ScrollMenu
            A reference to the created scroll menu object.
        """
        pass

    def add_checkbox_menu(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
        padx: int = 1,
        pady: int = 0,
        checked_char: str = "X",
    ) -> "py_cui.widgets.CheckBoxMenu":
        """Function that adds a new checkbox menu to the CUI grid

        Parameters
        ----------
        title : str
            The title of the checkbox
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        checked_char='X' : char
            The character used to mark 'Checked' items

        Returns
        -------
        new_checkbox_menu : CheckBoxMenu
            A reference to the created checkbox object.
        """
        pass

    def add_text_box(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
        padx: int = 1,
        pady: int = 0,
        initial_text: str = "",
        password: bool = False,
    ) -> "py_cui.widgets.TextBox":
        """Function that adds a new text box to the CUI grid

        Parameters
        ----------
        title : str
            The title of the textbox
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        initial_text='' : str
            Initial text for the textbox
        password=False : bool
            Toggle to show '*' instead of characters.

        Returns
        -------
        new_text_box : TextBox
            A reference to the created textbox object.
        """
        pass

    def add_text_block(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
        padx: int = 1,
        pady: int = 0,
        initial_text: str = "",
    ) -> "py_cui.widgets.ScrollTextBlock":
        """Function that adds a new text block to the CUI grid

        Parameters
        ----------
        title : str
            The title of the text block
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        initial_text='' : str
            Initial text for the text block

        Returns
        -------
        new_text_block : ScrollTextBlock
            A reference to the created textblock object.
        """
        pass

    def add_label(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
        padx: int = 1,
        pady: int = 0,
    ) -> "py_cui.widgets.Label":
        """Function that adds a new label to the CUI grid

        Parameters
        ----------
        title : str
            The title of the label
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction

        Returns
        -------
        new_label : Label
            A reference to the created label object.
        """
        pass

    def add_block_label(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
        padx: int = 1,
        pady: int = 0,
        center: bool = True,
    ) -> "py_cui.widgets.BlockLabel":
        """Function that adds a new block label to the CUI grid

        Parameters
        ----------
        title : str
            The title of the block label
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        center : bool
            flag to tell label to be centered or left-aligned.

        Returns
        -------
        new_label : BlockLabel
            A reference to the created block label object.
        """
        pass

    def add_button(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
        padx: int = 1,
        pady: int = 0,
        command: Callable[[], Any] = None,
    ) -> "py_cui.widgets.Button":
        """Function that adds a new button to the CUI grid

        Parameters
        ----------
        title : str
            The title of the button
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        command=None : Function
            A no-argument or lambda function to fire on button press.

        Returns
        -------
        new_button : Button
            A reference to the created button object.
        """
        pass

    def add_slider(
        self,
        title: str,
        row: int,
        column: int,
        row_span: int = 1,
        column_span: int = 1,
        padx: int = 1,
        pady: int = 0,
        min_val: int = 0,
        max_val: int = 100,
        step: int = 1,
        init_val: int = 0,
    ) -> "py_cui.controls.slider.SliderWidget":
        """Function that adds a new label to the CUI grid

        Parameters
        ----------
        title : str
            The title of the label
        row : int
            The row value, from the top down
        column : int
            The column value from the top down
        row_span=1 : int
            The number of rows to span accross
        column_span=1 : int
            the number of columns to span accross
        padx=1 : int
            number of padding characters in the x direction
        pady=0 : int
            number of padding characters in the y direction
        min_val = 0 int
            min value of the slider
        max_val = 0 int
            max value of the slider
        step = 0 int
            step to incremento or decrement
        init_val = 0 int
            initial value of the slider

        Returns
        -------
        new_slider : Slider
            A reference to the created slider object.
        """
        pass

    def forget_widget(self, widget: "py_cui.widgets.Widget") -> None:
        """Function that is used to destroy or "forget" widgets. Forgotten widgets will no longer be drawn

        Parameters
        ----------
        widget : py_cui.widgets.Widget
            Widget to remove from the UI

        Raises
        ------
        TypeError
            If input parameter is not of the py_cui widget type
        KeyError
            If input widget does not exist in the current UI or has already been removed.
        """
        pass

    def get_element_at_position(self, x: int, y: int) -> Optional["py_cui.ui.UIElement"]:
        """Returns containing widget for character position

        Parameters
        ----------
        x : int
            Horizontal character position
        y : int
            Vertical character position, top down

        Returns
        -------
        in_widget : UIElement
            Widget or popup that is within the position None if nothing
        """
        pass

    def _get_horizontal_neighbors(
        self, widget: "py_cui.widgets.Widget", direction: int
    ) -> Optional[List[int]]:
        """Gets all horizontal (left, right) neighbor widgets

        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The currently selected widget
        direction : py_cui.keys.KEY*
            must be an arrow key value

        Returns
        -------
        id_list : list[]
            A list of the neighbor widget ids
        """
        pass

    def _get_vertical_neighbors(
        self, widget: "py_cui.widgets.Widget", direction: int
    ) -> Optional[List[int]]:
        """Gets all vertical (up, down) neighbor widgets

        Parameters
        ----------
        widget : py_cui.widgets.Widget
            The currently selected widget
        direction : py_cui.keys.KEY*
            must be an arrow key value

        Returns
        -------
        id_list : list[]
            A list of the neighbor widget ids
        """
        pass

    # CUI status functions. Used to switch between widgets, set the mode, and
    # identify neighbors for overview mode

    def _check_if_neighbor_exists(self, direction: int) -> Optional[int]:
        """Function that checks if widget has neighbor in specified cell.

        Used for navigating CUI, as arrow keys find the immediate neighbor

        Parameters
        ----------
        direction : py_cui.keys.KEY_*
            The direction in which to search

        Returns
        -------
        widget_id : int
            The widget neighbor ID if found, None otherwise
        """
        pass

    def get_selected_widget(self) -> Optional["py_cui.widgets.Widget"]:
        """Function that gets currently selected widget

        Returns
        -------
        selected_widget : py_cui.widgets.Widget
            Reference to currently selected widget object
        """
        pass

    def set_selected_widget(self, widget_id: int) -> None:
        """Function that sets the selected widget for the CUI

        Parameters
        ----------
        widget_id : int
            the id of the widget to select
        """
        pass

    def lose_focus(self) -> None:
        """Function that forces py_cui out of focus mode.

        After popup is called, focus is lost
        """
        pass

    def move_focus(
        self, widget: "py_cui.widgets.Widget", auto_press_buttons: bool = True
    ) -> None:
        """Moves focus mode to different widget

        Parameters
        ----------
        widget : Widget
            The widget object we want to move focus to.
        """
        pass

    def _cycle_widgets(self, reverse: bool = False) -> None:
        """Function that is fired if cycle key is pressed to move to next widget

        Parameters
        ----------
        reverse : bool
            Default false. If true, cycle widgets in reverse order.
        """
        pass

    def add_key_command(self, key: Union[int, List[int]], command: Callable[[], Any]) -> None:
        """Function that adds a keybinding to the CUI when in overview mode

        Parameters
        ----------
        key : py_cui.keys.KEY_*
            ascii keycode used to map the key
        command : Function
            A no-arg or lambda function to fire on keypress
        """
        pass

    # Popup functions. Used to display messages, warnings, and errors to the user.

    def show_message_popup(self, title: str, text: str, color: int = WHITE_ON_BLACK) -> None:
        """Shows a message popup

        Parameters
        ----------
        title : str
            Message title
        text : str
            Message text
        color: int
            Popup color with format FOREGOUND_ON_BACKGROUND. See colors module. Default: WHITE_ON_BLACK.
        """
        pass

    def show_warning_popup(self, title: str, text: str) -> None:
        """Shows a warning popup

        Parameters
        ----------
        title : str
            Warning title
        text : str
            Warning text
        """
        pass

    def show_error_popup(self, title: str, text: str) -> None:
        """Shows an error popup

        Parameters
        ----------
        title : str
            Error title
        text : str
            Error text
        """
        pass

    def show_yes_no_popup(self, title: str, command: Callable[[bool], Any]):
        """Shows a yes/no popup.

        The 'command' parameter must be a function with a single boolean parameter

        Parameters
        ----------
        title : str
            Message title
        command : function
            A function taking in a single boolean parameter. Will be fired with True if yes selected, false otherwise
        """
        pass

    def show_text_box_popup(
        self, title: str, command: Callable[[str], Any], initial_text = '', password: bool = False
    ):
        """Shows a textbox popup.

        The 'command' parameter must be a function with a single string parameter

        Parameters
        ----------
        title : str
            Message title
        command : Function
            A function with a single string parameter, fired with contents of textbox when enter key pressed
        password=False : bool
            If true, write characters as '*'
        """
        pass

    def show_menu_popup(
        self,
        title: str,
        menu_items: List[str],
        command: Callable[[str], Any],
        run_command_if_none: bool = False,
    ):
        """Shows a menu popup.

        The 'command' parameter must be a function with a single string parameter

        Parameters
        ----------
        title : str
            menu title
        menu_items : list of str
            A list of menu items
        command : Function
            A function taking in a single string argument. Fired with selected menu item when ENTER pressed.
        run_command_if_none=False : bool
            If True, will run command passing in None if no menu item selected.
        """
        pass

    def show_loading_icon_popup(
        self, title: str, message: str, callback: Callable[[], Any] = None
    ):
        """Shows a loading icon popup

        Parameters
        ----------
        title : str
            Message title
        message : str
            Message text. Will show as '$message...'
        callback=None : Function
            If not none, fired after loading is completed. Must be a no-arg function
        """
        pass

    def show_loading_bar_popup(
        self, title: str, num_items: List[int], callback: Callable[[], Any] = None
    ) -> None:
        """Shows loading bar popup.

        Use 'increment_loading_bar' to show progress

        Parameters
        ----------
        title : str
            Message title
        num_items : int
            Number of items to iterate through for loading
        callback=None : Function
            If not none, fired after loading is completed. Must be a no-arg function
        """
        pass

    def show_form_popup(
        self,
        title: str,
        fields: List[str],
        passwd_fields: List[str] = [],
        required: List[str] = [],
        callback: Callable[[], Any] = None,
    ) -> None:
        """Shows form popup.

        Used for inputting several fields worth of values

        Parameters
        ---------
        title : str
            Message title
        fields : List[str]
            Names of each individual field
        passwd_fields : List[str]
            Field names that should have characters hidden
        required : List[str]
            Fields that are required before submission
        callback=None : Function
            If not none, fired after loading is completed. Must be a no-arg function
        """
        pass

    def show_filedialog_popup(
        self,
        popup_type: str = "openfile",
        initial_dir: str = ".",
        callback: Callable[[], Any] = None,
        ascii_icons: bool = True,
        limit_extensions: List[str] = [],
    ) -> None:
        """Shows form popup.

        Used for inputting several fields worth of values

        Parameters
        ---------
        popup_type : str
            Type of filedialog popup - either openfile, opendir, or saveas
        initial_dir : os.PathLike
            Path to directory in which to open the file dialog, default "."
        callback=None : Callable
            If not none, fired after loading is completed. Must be a no-arg function, default=None
        ascii_icons : bool
            Compatibility option - use ascii icons instead of unicode file/folder icons, default True
        limit_extensions : List[str]
            Only show files with extensions in this list if not empty. Default, []
        """
        pass

    def increment_loading_bar(self) -> None:
        """Increments progress bar if loading bar popup is open"""
        pass

    def stop_loading_popup(self) -> None:
        """Leaves loading state, and closes popup.

        Must be called by user to escape loading.
        """
        pass

    def close_popup(self) -> None:
        """Closes the popup, and resets focus"""
        pass

    def _refresh_height_width(self) -> None:
        """Function that updates the height and width of the CUI based on terminal window size."""
        pass

    def get_absolute_size(self) -> Tuple[int, int]:
        """Returns dimensions of CUI

        Returns
        -------
        height, width : int
            The dimensions of drawable CUI space in characters
        """
        pass

    # Draw Functions. Function for drawing widgets, status bars, and popups

    def _draw_widgets(self) -> None:
        """Function that draws all of the widgets to the screen"""
        pass

    def _draw_status_bars(self, stdscr, height: int, width: int) -> None:
        """Draws status bar and title bar

        Parameters
        ----------
        stdscr : curses Standard cursor
            The cursor used to draw the status bar
        height : int
            Window height in terminal characters
        width : int
            Window width in terminal characters
        """
        pass

    def _display_window_warning(self, stdscr, error_info: str) -> None:
        """Function that prints some basic error info if there is an error with the CUI

        Parameters
        ----------
        stdscr : curses Standard cursor
            The cursor used to draw the warning
        error_info : str
            The information regarding the error.
        """
        pass

    def _handle_key_presses(self, key_pressed: int) -> None:
        """Function that handles all main loop key presses.

        Parameters
        ----------
        key_pressed : py_cui.keys.KEY_*
            The key being pressed
        """
        pass

    def _draw(self, stdscr) -> None:
        """Main CUI draw loop called by start()

        Parameters
        --------
        stdscr : curses Standard screen
            The screen buffer used for drawing CUI elements
        """
        pass

    def __format__(self, fmt):
        """Override of base format function. Prints list of current widgets.

        Parameters
        ----------
        fmt : Format
            The format to override
        """

        out = ""
        for widget_id in self.get_widgets().keys():
            if self.get_widgets()[widget_id] is not None:
                out += f"{self.get_widgets()[widget_id].get_title()}\n"
        return out
