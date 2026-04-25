"""File containing classes for all popups used by py_cui
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019


# required library imports
import curses
import py_cui
import py_cui.ui
import py_cui.errors
from typing import Tuple


class Popup(py_cui.ui.UIElement):
    """Base CUI popup class.

    Contains constructor and initial definitions for key_press and draw
    Unlike widgets, they do not have a set grid cell, they are simply centered in the view
    frame

    Attributes
    ----------
    _root : py_cui.PyCUI
        Root CUI window
    _text : str
        Popup message text
    _selected : bool
        Always true. Used by the renderer to highlight popup
    _close_keys : List[int]
        List of keycodes used to close popup
    """


    def __init__(self, root: 'py_cui.PyCUI', title: str, text: str, color: int, renderer: 'py_cui.renderer.Renderer', logger):
        """Initializer for main popup class. Calls UIElement intialier, and sets some initial values
        """

        super().__init__(0, title, renderer, logger)
        self._root         = root
        self._text         = text
        self._selected     = True
        self._close_keys   = [py_cui.keys.KEY_ESCAPE]
        # Default to use the selected color for all aspects of ui element
        self._color                 = color
        self._border_color          = color
        self._focus_border_color    = color
        self._selected_color        = color
        self.update_height_width()


    def _increment_counter(self):
        """Function that increments an internal counter
        """

        pass


    def set_text(self, text: str) -> None :
        """Sets popup text (message)

        Parameters
        ----------
        text : str
            The new popup text
        """
        pass


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base class, computes position based on root dimensions

        Returns
        -------
        start_x, start_y : int
            The coords of the upper-left corner of the popup
        """
        pass


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base class, computes position based on root dimensions

        Returns
        -------
        stop_x, stop_y : int
            The coords of the lower-right corner of the popup
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Handles key presses when popup is open

        By default, only closes popup when Escape is pressed

        Parameters
        ----------
        key_pressed : int
            The ascii code for the key that was pressed
        """
        pass


    def _draw(self) -> None:
        """Function that uses renderer to draw the popup

        Can be implemented by subclass. Base draw function will draw the title and text in a bordered box
        """
        pass



class MessagePopup(Popup):
    """Class representing a simple message popup
    """

    def __init__(self, root, title, text, color, renderer, logger):
        """Initializer for MessagePopup
        """

        super().__init__(root, title, text, color, renderer, logger)
        self._close_keys = [ py_cui.keys.KEY_ENTER,
                            py_cui.keys.KEY_ESCAPE,
                            py_cui.keys.KEY_SPACE,
                            py_cui.keys.KEY_DELETE] + py_cui.keys.KEY_BACKSPACE


    def _draw(self) -> None:
        """Draw function for MessagePopup. Calls superclass draw()
        """
        pass


class YesNoPopup(Popup):
    """Class for Yes/No popup. Extends Popup

    Attributes
    ----------
    _command : function, 1 boolean parameter
        Function that takes one boolean parameter. Called with True if yes, called with False if no.
    """

    def __init__(self, root, title, text, color, command, renderer, logger):
        """Initializer for YesNoPopup
        """

        super().__init__(root, title, text, color, renderer, logger)
        self._command = command


    def _handle_key_press(self, key_pressed: int):
        """Handle key press overwrite from superclass

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        pass


    def _draw(self):
        """Uses base class draw function
        """
        pass


class TextBoxPopup(Popup, py_cui.ui.TextBoxImplementation):
    """Class representing a textbox popup

    Attributes
    ----------
    _command : function
        The command to run when enter is pressed
    """

    def __init__(self, root, title, initial_text, color, command, renderer, password, logger):
        """Initializer for textbox popup. Uses TextBoxImplementation as base
        """

        Popup.__init__(self, root, title, initial_text, color, renderer, logger)
        py_cui.ui.TextBoxImplementation.__init__(self, initial_text, password, logger)
        self._command           = command
        self.update_height_width()


    def update_height_width(self) -> None:
        """Need to update all cursor positions on resize
        """
        pass


    def _handle_mouse_press(self, x: int, y: int, mouse_event) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """
        pass


    def _handle_key_press(self, key_pressed: int):
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


class MenuPopup(Popup, py_cui.ui.MenuImplementation):
    """A scroll menu popup.

    Allows for popup with several menu items to select from

    Attributes
    ----------
    _command : function
        a function that takes a single string parameter, run when ENTER pressed
    _run_command_if_none : bool
        Runs command even if there are no menu items (passes None)
    """

    def __init__(self, root: 'py_cui.PyCUI', items, title, color, command, renderer, logger, run_command_if_none):
        """Initializer for MenuPopup. Uses MenuImplementation as base
        """

        Popup.__init__(self, root, title, '', color, renderer, logger)
        py_cui.ui.MenuImplementation.__init__(self, logger)
        self.add_item_list(items)
        self._command              = command
        self._run_command_if_none  = run_command_if_none


    def _handle_mouse_press(self, x: int, y: int, mouse_event):
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        """
        pass



    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base handle key press function

        Enter key runs command, Escape key closes menu

        Parameters
        ----------
        key_pressed : int
            key code of key pressed
        """
        pass


    def _draw(self) -> None:
        """Overrides base class draw function
        """
        pass


class LoadingIconPopup(Popup):
    """Loading icon popup class

    MUST BE USED WITH A FORM OF ASYNC/THREADING

    Attributes
    ----------
    _loading_icons : list of str
        Animation frames for loading icon
    _icon_counter : int
        Current frame of animation
    _message : str
        Loading message
    """

    def __init__(self, root, title, message, color, renderer, logger):
        """Initializer for LoadingIconPopup
        """

        super().__init__(root, title, f'{message} ... \\', color, renderer, logger)
        self._loading_icons = ['\\', '|', '/', '-']
        self._icon_counter = 0
        self._message = message


    def _handle_key_press(self, key_pressed: int):
        """Override of base class function.

        Loading icon popups cannot be cancelled, so we wish to avoid default behavior

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """

        pass


    def _draw(self) -> None:
        """Overrides base draw function
        """
        pass


class LoadingBarPopup(Popup):
    """Class for Loading Bar Popup

    MUST BE USED WITH A FORM OF ASYNC/THREADING

    Attributes
    ----------
    num_items : int
        NUmber of items to count through
    completed_items : int
        counter for completed items
    """

    def __init__(self, root, title, num_items, color, renderer, logger):
        """Initializer for LoadingBarPopup
        """

        super().__init__(root, title, f'{"-" * num_items} (0/{num_items})', color, renderer, logger)
        self._num_items          = num_items
        self._loading_icons      = ['\\', '|', '/', '-']
        self._icon_counter       = 0
        self._completed_items    = 0


    def _handle_key_press(self, key_pressed: int):
        """Override of base class function.

        Loading icon popups cannot be cancelled, so we wish to avoid default behavior

        Parameters
        ----------
        key_pressed : int
            key code of pressed key
        """

        pass

    def _increment_counter(self) -> None:
        """Function that increments an internal counter
        """
        pass


    def _draw(self) -> None:
        """Override of base draw function
        """
        pass
