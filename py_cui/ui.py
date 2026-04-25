"""Module containing classes for generic UI elements.

Contains base UI element class, along with UI implementation agnostic UI element classes.
"""

# Author:    Jakub Wlodek
# Created:   19-Mar-2020


import py_cui
import py_cui.errors
import py_cui.colors

import inspect
from typing import Any, List, Optional, Tuple, Callable


class UIElement:
    """Base class for all UI elements. Extended by base widget and popup classes.

    Interfaces between UIImplementation subclasses and CUI engine. For example,
    a widget is a subclass of a UIElement. Then a TextBox widget would be a subclass
    of the base widget class, and the TextBoxImplementation. The TextBoxImplementation
    superclass contains logic for all textbox required operations, while the widget base
    class contains all links to the CUI engine.

    Attributes
    ----------
    _id : str
        Internal UI element unique ID
    _title : str
        UI element title
    _padx, pady : int, int
        padding in terminal characters
    _start_x, _start_y: int, int
        Coords in terminal characters for top-left corner of element
    _stop_x, _stop_y : int, int
        Coords in terminal characters for bottom-right corner of element
    _height, width : int, int
        absolute dimensions of ui element in terminal characters
    _color : int
        Default color for which to draw element
    _border_color: int
        Color used to draw the border of the element when not focused
    _focus_border_color: int
        Color used to draw the border of the element when focused
    _selected : bool
        toggle for marking an element as selected
    _renderer : py_cui.renderer.Renderer
        The default ui renderer
    _logger   : py_cui.debug.PyCUILogger
        The default logger inherited from the parent
    _help_text: str
        Text to diplay when selected in status bar
    """

    def __init__(self, id, title, renderer, logger):
        """Initializer for UIElement base class
        """

        self._id                        = id
        self._title                     = title
        self._padx                      = 1
        self._pady                      = 0
        self._start_x,  self._stop_y    = 0, 0
        self._stop_x,   self._start_y   = 0, 0
        self._height,   self._width     = 0, 0
        # Default UI Element color is white on black.
        self._color                     = py_cui.WHITE_ON_BLACK
        self._border_color              = self._color
        self._focus_border_color        = self._color
        self._selected_color            = self._color
        self._selected                  = False
        self._renderer                  = renderer
        self._logger                    = logger
        self._help_text                 = ''


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Must be implemented by subclass, computes the absolute coords of upper-left corner
        """

        raise NotImplementedError


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Must be implemented by subclass, computes the absolute coords of bottom-right corner
        """

        raise NotImplementedError


    def get_absolute_dimensions(self) -> Tuple[int,int]:
        """Gets dimensions of element in terminal characters

        Returns
        -------
        height, width : int, int
            Dimensions of element in terminal characters
        """
        pass


    def update_height_width(self) -> None:
        """Function that refreshes position and dimensons on resize.

        If necessary, make sure required widget attributes updated here as well.
        """
        pass


    def get_viewport_height(self) -> int:
        """Gets the height of the element viewport (height minus padding and borders)

        Returns
        -------
        viewport_height : int
            Height of element viewport in terminal characters
        """
        pass


    def get_id(self) -> int:
        """Gets the element ID

        Returns
        -------
        id : int
            The ui element id
        """
        pass


    def get_title(self) -> str:
        """Getter for ui element title

        Returns
        -------
        title : str
            UI element title
        """
        pass


    def get_padding(self) -> Tuple[int,int]:
        """Gets ui element padding on in characters

        Returns
        -------
        padx, pady : int, int
            Padding on either axis in characters
        """
        pass


    def get_start_position(self) -> Tuple[int,int]:
        """Gets coords of upper left corner

        Returns
        -------
        start_x, start_y : int, int
            Coords of upper right corner
        """
        pass


    def get_stop_position(self) -> Tuple[int,int]:
        """Gets coords of lower right corner

        Returns
        -------
        stop_x, stop_y : int, int
            Coords of lower right corner
        """
        pass


    def get_color(self) -> int:
        """Gets current element color

        Returns
        -------
        color : int
            color code for combination
        """
        pass


    def get_border_color(self) -> int:
        """Gets current element border color

        Returns
        -------
        color : int
            color code for combination
        """
        pass


    def get_selected_color(self) -> int:
        """Gets current selected item color

        Returns
        -------
        color : int
            color code for combination
        """
        pass


    def is_selected(self) -> bool:
        """Get selected status

        Returns
        -------
        selected : bool
            True if selected, False otherwise
        """
        pass


    def get_renderer(self) -> 'py_cui.renderer.Renderer':
        """Gets reference to renderer object

        Returns
        -------
        renderer : py_cui.renderer.Render
            renderer object used for drawing element
        """
        pass


    def get_help_text(self) -> str:
        """Returns current help text

        Returns
        -------
        help_text : str
            Current element status bar help message
        """
        pass


    def set_title(self, title: str):
        """Function that sets the widget title.

        Parameters
        ----------
        title : str
            New widget title
        """
        pass


    def set_color(self, color: int) -> None:
        """Sets element default color

        Parameters
        ----------
        color : int
            New color pair key code
        """
        pass


    def set_border_color(self, color: int) -> None:
        """Sets element border color

        Parameters
        ----------
        color : int
            New color pair key code
        """
        pass


    def set_focus_border_color(self, color: int) -> None:
        """Sets element border color if the current element
        is focused

        Parameters
        ----------
        color : int
            New color pair key code
        """
        pass


    def set_selected_color(self, color: int) -> None:
        """Sets element sected color

        Parameters
        ----------
        color : int
            New color pair key code
        """
        pass


    def set_selected(self, selected: bool) -> None:
        """Marks the UI element as selected or not selected

        Parameters
        ----------
        selected : bool
            The new selected state of the element
        """
        pass


    def set_help_text(self, help_text: str) -> None:
        """Sets status bar help text

        Parameters
        ----------
        help_text : str
            New statusbar help text
        """
        pass


    def set_focus_text(self, focus_text: str) -> None:
        """Sets status bar focus text. Legacy function, overridden by set_focus_text

        Parameters
        ----------
        focus_text : str
            New statusbar help text
        """
        pass


    def _handle_key_press(self, key_pressed):
        """Must be implemented by subclass. Used to handle keypresses
        """

        raise NotImplementedError


    def _handle_mouse_press(self, x, y, mouse_event):
        """Can be implemented by subclass. Used to handle mouse presses

        Parameters
        ----------
        x, y : int, int
            Coordinates of the mouse press event.
        """

        pass


    def _draw(self):
        """Must be implemented by subclasses. Uses renderer to draw element to terminal
        """

        raise NotImplementedError


    def _assign_renderer(self, renderer: 'py_cui.renderer.Renderer', quiet: bool=False) :
        """Function that assigns a renderer object to the element

        (Meant for internal usage only)

        Parameters
        ----------
        renderer : py_cui.renderer.Renderer
            Renderer for drawing element

        Raises
        ------
        error : PyCUIError
            If parameter is not an initialized renderer.
        """
        pass


    def _contains_position(self, x: int, y: int) -> bool:
        """Checks if character position is within element.

        Parameters
        ----------
        x : int
            X coordinate to check
        y : int
            Y coordinate to check

        Returns
        -------
        contains : bool
            True if (x,y) is within the element, false otherwise
        """
        pass


class UIImplementation:
    """Base class for ui implementations.

    Should be extended for creating logic common accross ui elements.
    For example, a textbox needs the same logic for a widget or popup.
    This base class is only used to initialize the logger

    Attributes
    ----------
    _logger : py_cui.debug.PyCUILogger
        parent logger object reference.
    """

    def __init__(self, logger):
        self._logger = logger


class TextBoxImplementation(UIImplementation):
    """UI implementation for a single-row textbox input

    Attributes
    ----------
    _text : str
        The text in the text box
    _initial_cursor : int
        Initial position of the cursor
    _cursor_x, _cursor_y : int
        The absolute positions of the cursor in the terminal window
    _cursor_text_pos : int
        the cursor position relative to the text
    _cursor_max_left, cursor_max_right : int
        The cursor bounds of the text box
    _viewport_width : int
        The width of the textbox viewport
    _password : bool
        Toggle to display password characters or text
    """

    def __init__(self, initial_text: str, password: bool , logger):
        """Initializer for the TextBoxImplementation base class
        """

        super().__init__(logger)
        self._text             = initial_text
        self._password         = password
        self._initial_cursor   = 0
        self._cursor_text_pos  = 0
        self._cursor_max_left  = 0
        self._cursor_x         = 0
        self._cursor_max_right = 0
        self._cursor_y         = 0
        self._viewport_width   = 0

    # Variable getter + setter functions

    def get_initial_cursor_pos(self) -> int:
        """Gets initial cursor position

        Returns
        -------
        initial_cursor : int
            Initial position of the cursor
        """
        pass


    def get_cursor_text_pos(self) -> int:
        """Gets current position of cursor relative to text

        Returns
        -------
        cursor_text_pos : int
            the cursor position relative to the text
        """
        pass


    def get_cursor_limits(self) -> Tuple[int,int]:
        """Gets cursor extreme points in terminal position

        Returns
        -------
        cursor_max_left, cursor_max_right : int
            The cursor bounds of the text box
        """
        pass


    def get_cursor_position(self) -> Tuple[int,int]:
        """Returns current cursor poition

        Returns
        -------
        cursor_x, cursor_y : int
            The absolute positions of the cursor in the terminal window
        """
        pass


    def get_viewport_width(self) -> int:
        """Gets the width of the textbox viewport

        Returns
        -------
        viewport_width : int
            The width of the textbox viewport
        """
        pass


    def set_text(self, text: str):
        """Sets the value of the text. Overwrites existing text

        Parameters
        ----------
        text : str
            The text to write to the textbox
        """
        pass


    def get(self) -> str:
        """Gets value of the text in the textbox

        Returns
        -------
        text : str
            The current textbox test
        """
        pass


    def clear(self) -> None:
        """Clears the text in the textbox
        """
        pass


    def _move_left(self) -> None:
        """Shifts the cursor the the left. Internal use only
        """
        pass


    def _move_right(self) -> None:
        """Shifts the cursor the the right. Internal use only
        """
        pass


    def _insert_char(self, key_pressed: int) -> None:
        """Inserts char at cursor position. Internal use only

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        pass


    def _jump_to_start(self) -> None:
        """Jumps to the start of the textbox. Internal use only
        """
        pass


    def _jump_to_end(self) -> None:
        """Jumps to the end to the textbox. Internal use only
        """
        pass


    def _erase_char(self) -> None:
        """Erases character at textbox cursor. Internal Use only
        """
        pass


    def _delete_char(self) -> None:
        """Deletes character to right of texbox cursor. Internal use only
        """
        pass


class MenuImplementation(UIImplementation):
    """A scrollable menu UI element

    Allows for creating a scrollable list of items of which one is selectable.
    Analogous to a RadioButton

    Attributes
    ----------
    _top_view : int
        the uppermost menu element in view
    _selected_item : int
        the currently highlighted menu item
    _view_items : list of str
        list of menu items
    """

    def __init__(self, logger):
        """Initializer for MenuImplementation base class
        """

        super().__init__(logger)
        self._top_view         = 0
        self._selected_item    = 0
        self._page_scroll_len  = 5
        self._view_items       = []
        self._on_selection_change: Optional[Callable[[Any],Any]] = None
        self._stick_to_bottom = False

    
    def toggle_stick_to_bottom(self):
        """Toggle option for keeping the viewport at the bottom of the items
        """
        pass


    def clear(self) -> None:
        """Clears all items from the Scroll Menu
        """
        pass


    def set_on_selection_change_event(self, on_selection_change_event: Callable[[Any],Any]):
        """Function that sets the function fired when menu selection changes.

        Event function must take 0 or 1 parameters. If 1 parameter, the new selcted item will be passed in.

        Parameters
        ----------
        on_selection_change_event : Callable
            Callable function that takes in as an argument the newly selected element

        Raises
        ------
        TypeError
            Raises a type error if event function is not callable
        """
        pass


    def _process_selection_change_event(self):
        """Function that executes on-selection change event either with the current menu item, or with no-args"""
        pass


    def get_selected_item_index(self) -> int:
        """Gets the currently selected item

        Returns
        -------
        selected_item : int
            the currently highlighted menu item
        """
        pass


    def set_selected_item_index(self, selected_item_index: int) -> None:
        """Sets the currently selected item

        Parameters
        ----------
        selected_item : int
            The new selected item index
        """
        pass


    def _scroll_up(self) -> None:
        """Function that scrolls the view up in the scroll menu
        """
        pass


    def _scroll_down(self, viewport_height: int) -> None:
        """Function that scrolls the view down in the scroll menu

        TODO: Viewport height should be calculated internally, and not rely on a parameter.

        Parameters
        ----------
        viewport_height : int
            The number of visible viewport items
        """
        pass


    def _jump_up(self) -> None:
        """Function for jumping up menu several spots at a time
        """
        pass


    def _jump_down(self, viewport_height: int) -> None:
        """Function for jumping down the menu several spots at a time

        Parameters
        ----------
        viewport_height : int
            The number of visible viewport items
        """
        pass


    def _jump_to_top(self) -> None:
        """Function that jumps to the top of the menu
        """
        pass


    def _jump_to_bottom(self, viewport_height: int) -> None:
        """Function that jumps to the bottom of the menu

        Parameters
        ----------
        viewport_height : int
            The number of visible viewport items
        """
        pass


    def add_item(self, item: Any) -> None: 
        """Adds an item to the menu.

        Parameters
        ----------
        item : Object
            Object to add to the menu. Must have implemented __str__ function
        """
        pass


    def add_item_list(self, item_list: List[Any]) -> None:

        """Adds a list of items to the scroll menu.

        Parameters
        ----------
        item_list : List[Object]
            list of objects to add as items to the scrollmenu
        """
        pass


    def remove_selected_item(self) -> None:
        """Function that removes the selected item from the scroll menu.
        """
        pass


    def remove_item(self, item: Any) -> None:
        """Function that removes a specific item from the menu

        Parameters
        ----------
        item : Object
            Reference of item to remove
        """
        pass


    def get_item_list(self) -> List[Any]:
        """Function that gets list of items in a scroll menu

        Returns
        -------
        item_list : List[Object]
            list of items in the scrollmenu
        """
        pass


    def get(self) -> Optional[Any]:
        """Function that gets the selected item from the scroll menu

        Returns
        -------
        item : Object
            selected item, or None if there are no items in the menu
        """
        pass


    def is_empty(self) -> bool:
        """Function that returns true if menu has no items within it, false otherwise

        Returns
        -------
        bool
            True if menu has no items, False otherwise. Identical to len(self._view_items) == 0
        """
        pass


    def set_selected_item(self, selected_item: Any):
        """Function that replaces the currently selected item with a new item

        Parameters
        ----------
        item : Object
            A new selected item to replace the current one
        """
        pass


    def get_item_index(self, index: int):
        """Function that returns reference to item at given index

        Paramters
        ---------
        index : int
            Index of object

        Returns
        -------
        item : Any
            Item at specified index in the list, or None if index is invalid.
        """
        pass


    def set_item_index(self, item: Any, index: int):
        """Function that sets the item at the specified index of the menu

        Parameters
        ----------
        item: Any
            Item to put in menu at given index
        index: int
            Index at which to put the specified item.
        """
        pass


class CheckBoxMenuImplementation(MenuImplementation):
    """Class representing checkbox menu ui implementation

    Attributes
    ----------
    _selected_item_dict : dict of object -> bool
        stores each object and maps to its current selected status
    _checked_char : char
        Character to mark checked items
    """

    def __init__(self, logger, checked_char):
        """Initializer for the checkbox menu implementation
        """

        super().__init__(logger)
        self._selected_item_dict = {}
        self._checked_char       = checked_char


    def add_item(self, item: Any) -> None:
        """Extends base class function, item is added and marked as unchecked to start

        Parameters
        ----------
        item : object
            The item being added
        """
        pass


    def remove_selected_item(self) -> None:
        """Removes selected item from item list and selected item dictionary
        """
        pass


    def remove_item(self, item) -> None:
        """Removes item from item list and selected item dict

        Parameters
        ----------
        item : object
            Item to remove from menu
        """
        pass


    def toggle_item_checked(self, item: Any):
        """Function that marks an item as selected

        Parameters
        ----------
        item : object
            Toggle item checked state
        """
        pass


    def mark_item_as_checked(self, item: Any) -> None:
        """Function that marks an item as selected

        Parameters
        ----------
        item : object
            Toggle item checked state
        """
        pass


    def mark_item_as_not_checked(self, item) -> None:
        """Function that marks an item as selected

        Parameters
        ----------
        item : object
            Item to uncheck
        """
        pass


class DropdownMenuImplementation(MenuImplementation):

    def __init__(self, logger, max_height):

        super().__init__(logger)
        self.max_height = max_height
        self.opened = False


class TextBlockImplementation(UIImplementation):
    """Base class for TextBlockImplementation

    Contains all logic required for a textblock ui element to function.
    Currently only implemented in widget form, though popup form is possible.

    Attributes
    ----------
    _text_lines : List[str]
        the lines of text in the texbox
    _viewport_x_start, _viewport_y_start : int
        Initial location of viewport relative to text
    _cursor_text_pos_x, _cursor_text_pos_y : int
        Cursor position relative to text
    _cursor_x, _cursor_y : int
        Absolute cursor position in characters
    _cursor_max_up, _cursor_max_down : int
        cursor limits in vertical space
    _cursor_max_left, _cursor_max_right : int
        Cursor limits in horizontal space
    _viewport_height, _viewport_width : int
        The dimensions of the viewport in characters
    """

    def __init__(self, initial_text: str, logger):
        """Initializer for TextBlockImplementation base class

        Zeros attributes, and parses initial text
        """

        super().__init__(logger)
        self._text_lines = initial_text.splitlines()
        if len(self._text_lines) == 0:
            self._text_lines.append('')

        self._viewport_y_start   = 0
        self._viewport_x_start   = 0
        self._cursor_text_pos_x  = 0
        self._cursor_text_pos_y  = 0
        self._cursor_y           = 0
        self._cursor_x           = 0
        self._cursor_max_up      = 0
        self._cursor_max_down    = 0
        self._cursor_max_left    = 0
        self._cursor_max_right   = 0
        self._viewport_width     = 0
        self._viewport_height    = 0


    # Getters and setters

    def get_viewport_start_pos(self) -> Tuple[int,int]:
        """Gets upper left corner position of viewport

        Returns
        -------
        viewport_x_start, viewport_y_start : int
            Initial location of viewport relative to text
        """
        pass


    def get_viewport_dims(self) -> Tuple[int,int]:
        """Gets viewport dimensions in characters

        Returns
        -------
        viewport_height, viewport_width : int
            The dimensions of the viewport in characters
        """
        pass


    def get_cursor_text_pos(self) -> Tuple[int,int]:
        """Gets cursor postion relative to text

        Returns
        -------
        cursor_text_pos_x, cursor_text_pos_y : int
            Cursor position relative to text
        """
        pass


    def get_abs_cursor_position(self) -> Tuple[int,int]:
        """Gets absolute cursor position in terminal characters

        Returns
        -------
        cursor_x, cursor_y : int
            Absolute cursor position in characters
        """
        pass


    def get_cursor_limits_vertical(self) -> Tuple[int,int]:
        """Gets limits for cursor in vertical direction

        Returns
        -------
        cursor_max_up, cursor_max_down : int
            cursor limits in vertical space
        """
        pass


    def get_cursor_limits_horizontal(self) -> Tuple[int,int]:
        """Gets limits for cursor in horizontal direction

        Returns
        -------
        cursor_max_left, cursor_max_right : int
            Cursor limits in horizontal space
        """
        pass


    def get(self) -> str:
        """Gets all of the text in the textblock and returns it

        Returns
        -------
        text : str
            The current text in the text block
        """
        pass


    def write(self, text: str) -> None:
        """Function used for writing text to the text block

        Parameters
        ----------
        text : str
            Text to write to the text block
        """
        pass


    def clear(self) -> None:
        """Function that clears the text block
        """
        pass


    def get_current_line(self) -> str:
        """Returns the line on which the cursor currently resides

        Returns
        -------
        current_line : str
            The current line of text that the cursor is on
        """
        pass


    def set_text(self, text: str) -> None:
        """Function that sets the text for the textblock.

        Note that this will overwrite any existing text

        Parameters
        ----------
        text : str
            text to write into text block
        """
        pass


    def set_text_line(self, text: str) -> None:
        """Function that sets the current line's text.

        Meant only for internal use

        Parameters
        ----------
        text : str
            text line to write into text block
        """
        pass


    def _move_left(self) -> None:
        """Function that moves the cursor/text position one location to the left
        """
        pass


    def _move_right(self) -> None:
        """Function that moves the cursor/text position one location to the right
        """
        pass


    def _move_up(self) -> None:
        """Function that moves the cursor/text position one location up
        """
        pass


    def _move_down(self) -> None:
        """Function that moves the cursor/text position one location down
        """
        pass



    def _handle_newline(self) -> None:
        """Function that handles recieving newline characters in the text
        """
        pass


    def _handle_backspace(self) -> None:
        """Function that handles recieving backspace characters in the text
        """
        pass


    def _handle_home(self) -> None:
        """Function that handles recieving a home keypress
        """
        pass


    def _handle_end(self) -> None:
        """Function that handles recieving an end keypress
        """
        pass


    def _handle_delete(self) -> None:
        """Function that handles recieving a delete keypress
        """
        pass


    def _insert_char(self, key_pressed: int) -> None:
        """Function that handles recieving a character

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        pass
