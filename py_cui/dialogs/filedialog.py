"""Implementation, widget, and popup classes for file selection dialogs
"""

import py_cui.ui
import py_cui.widgets
import py_cui.popups
import py_cui.colors
import os
from typing import List, Optional, Tuple

# Imports used to detect hidden files
import sys
import stat


def is_filepath_hidden(path:  str) -> bool:
    """Function checks if file or folder is considered "hidden"

    Parameters
    ----------
    path : str
        Path to file or folder

    Returns
    -------
    marked_hidden : bool
        True if name starts with '.', or has hidden attribute in OS
    """
    pass


class FileDirElem:
    """Simple helper class defining a single file or directory

    Attributes
    ----------
    _type : str
        Either dir or file
    _name : str
        The name of the file or directory
    _path : str
        The absolute path to the directory or file
    _folder_icon : str
        icon or text for folder
    _file_icon : str
        icon for file
    """

    def __init__(self, elem_type: str, name: str, fullpath: str, ascii_icons: bool=False):
        """Intializer for FilDirElem
        """
        pass


    def get_path(self) -> str:
        """Getter for path

        Returns
        -------
        path : str
            Path of file/dir represented by elem
        """
        pass


    def __str__(self) -> str:
        """Override of to-string function

        Returns
        -------
        description : str
            Icon and name of dir or file
        """

        if self._type == 'file':
            return f'{self._file_icon} {self._name}'
        else:
            return f'{self._folder_icon} {self._name}'



class FileSelectImplementation(py_cui.ui.MenuImplementation):
    """Extension of menu implementation that allows for listing files and dirs in a location

    Attributes
    ----------
    _current_dir : str
        The current focused-on directory
    _ascii_icons : bool
        Toggle using ascii or unicode icons
    _dialog_type : str
        Type of open dialog
    _limit_extensions : List[str]
        List of file extensions to show as visible
    """


    def __init__(self, initial_loc: str, dialog_type: str, ascii_icons, logger, limit_extensions: List[str] = [], show_hidden: bool=False):
        """Initalizer for the file select menu implementation. Includes some logic for getting list of file and folders.
        """

        super().__init__(logger)

        self._current_dir = os.path.abspath(initial_loc)
        self._ascii_icons = ascii_icons
        self._dialog_type = dialog_type
        self._show_hidden = show_hidden

        self._limit_extensions = limit_extensions
        self.refresh_view()


    def refresh_view(self) -> None:
        """Function that refreshes the current list of files and folders in view
        """
        pass


class FileSelectElement(py_cui.ui.UIElement, FileSelectImplementation):
    """Custom UI Element for selecting files or directories.

    Displays list of files and dirs in a given location

    Attributes
    ----------
    _command : function
        a function that takes a single string parameter, run when ENTER pressed
    _run_command_if_none : bool
        Runs command even if there are no menu items (passes None)
    """

    def __init__(self, root, initial_dir, dialog_type: str, ascii_icons, title, color, command, renderer, logger, limit_extensions: List[str]=[]):
        """Initializer for MenuPopup. Uses MenuImplementation as base
        """

        py_cui.ui.UIElement.__init__(self, 0, os.path.abspath(initial_dir), renderer, logger)
        FileSelectImplementation.__init__(self, initial_dir, dialog_type, ascii_icons, logger, limit_extensions=limit_extensions)
        self._command              = command
        self._parent_dialog        = root
        self._text_color_rules = [
            py_cui.colors.ColorRule('\U0001f4c1', py_cui.BLUE_ON_BLACK, py_cui.WHITE_ON_BLUE,
                                    'startswith', 'region', [3, 1000], False, logger),
            py_cui.colors.ColorRule('<DIR>', py_cui.BLUE_ON_BLACK, py_cui.WHITE_ON_BLUE,
                                    'startswith', 'region', [6, 1000], False, logger),
            py_cui.colors.ColorRule('     ', py_cui.WHITE_ON_BLACK, py_cui.BLACK_ON_WHITE,
                                    'startswith', 'region', [6, 1000], True, logger),
            py_cui.colors.ColorRule('\U0001f5ce', py_cui.WHITE_ON_BLACK, py_cui.BLACK_ON_WHITE,
                                    'startswith', 'region', [3, 1000], False, logger)
        ]
        #self._run_command_if_none  = run_command_if_none


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute start position

        Returns
        -------
        start_x, start_y : int, int
            The position in characters in the terminal window to start the Field element
        """
        pass


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute stop position

        Returns
        -------
        stop_x, stop_y : int, int
            The position in characters in the terminal window to stop the Field element
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


class FileNameInput(py_cui.ui.UIElement, py_cui.ui.TextBoxImplementation):
    """UI Element class representing name input field for filedialog

    Attributes
    ----------
    _parent_dialog : FileDialog
        parent dialog widget or popup
    """


    def __init__(self, parent_dialog, title, initial_dir, renderer, logger):
        """Initializer for the FormFieldElement class
        """

        self._parent_dialog = parent_dialog
        py_cui.ui.UIElement.__init__(self, 0, title, renderer, logger)
        py_cui.ui.TextBoxImplementation.__init__(self, title, False, logger)
        self._help_text = 'Press Tab to move to the next field, or Enter to submit.'
        self.set_text(initial_dir)
        self._padx = 0
        self._pady = 0
        self._selected = False
        self.update_height_width()


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute start position

        Returns
        -------
        start_x, start_y : int, int
            The position in characters in the terminal window to start the Field element
        """
        pass


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute stop position

        Returns
        -------
        stop_x, stop_y : int, int
            The position in characters in the terminal window to stop the Field element
        """
        pass


    def update_height_width(self) -> None:
        """Override of base class. Updates text field variables for form field
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Handles text input for the field. Called by parent
        """
        pass


    def _draw(self) -> None:
        """Draw function for the field. Called from parent. Essentially the same as a TextboxPopup
        """
        pass


class FileDialogButton(py_cui.ui.UIElement):
    """Utility button element for parent filedialog

    Attributes
    ----------
    _parent_dialog : FileDialog
        Main filedialog popup or widget
    _button_num : int
        0 for submit button, 1 for cancel button
    """


    def __init__(self, parent_dialog, statusbar_msg, command, button_num, *args):
        """Initializer for Button Widget
        """
        pass


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute start position

        Returns
        -------
        start_x, start_y : int, int
            The position in characters in the terminal window to start the Field element
        """
        pass


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute stop position

        Returns
        -------
        stop_x, stop_y : int, int
            The position in characters in the terminal window to stop the Field element
        """
        pass


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Handles mouse presses

        Parameters
        ----------
        x : int
            x coordinate of click in characters
        y : int
            y coordinate of click in characters
        mouse_event : int
            Mouse event keycode of mouse press
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class, adds ENTER listener that runs the button's command

        Parameters
        ----------
        key_pressed : int
            Key code of pressed key
        """
        pass


    def perform_command(self) -> None:
        pass


    def _draw(self) -> None:
        """Override of base class draw function
        """
        pass


class InternalFileDialogPopup(py_cui.popups.MessagePopup):
    """A helper class for abstracting a message popup tied to a parent popup

    Attributes
    ----------
    parent : FormPopup
        The parent form popup that spawned the message popup
    """

    def __init__(self, parent, *args):
        """Initializer for Internal form Popup
        """

        super().__init__(*args)
        self._parent = parent


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class, close in parent instead of root
        """
        pass


class FileDialogPopup(py_cui.popups.Popup):
    """Main implementation class of a FileDialog poup.

    Attributes
    ----------
    _submit_action : func
        A function that takes a single string argument. Called with selected path when submit button is pressed
    _filename_input : FileNameInput
        Extension of textbox, acts as input field to create new dirs/files or select save name
    _file_dir_select : FileSelectElement
        Extension  of scroll menu used to display current files and dirs
    _submit_button : FileDialogButton
        Extension of button - Runs the callback with the selected file
    _cancel_button : FileDialogButton
        Extension of button - closes popup
    _internal_popup : InternalFileDialogPopup
        Extension of message popup, used to display warnings as secondary popup.
    _currently_selected : UIElement
        Currently selected sub-element of file dialog popup
    """


    def __init__(self, root, callback, initial_dir, dialog_type, ascii_icons, limit_extensions, color, renderer, logger):
        """Initalizer for the FileDialogPopup
        """
        pass


    def _submit(self, output: str) -> None:
        pass


    def display_warning(self, message: str) -> None:
        """Helper function for showing internal popup warning message

        Parameters
        ----------
        message : str
            Warning message to display
        """
        pass


    def output_valid(self, output) -> Tuple[bool,Optional[str]]:
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


    def update_height_width(self) -> None:
        """Override of base class function

        Also updates all form field elements in the form
        """
        pass


    def _handle_key_press(self, key_pressed:int) -> None:
        """Override of base class. Here, we handle tabs, enters, and escapes

        All other key presses are passed to the currently selected field element

        Parameters
        ----------
        key_pressed : int
            Key code of pressed key
        """
        pass


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function

        Simply enters the appropriate field when mouse is pressed on it

        Parameters
        ----------
        x, y : int, int
            Coordinates of the mouse press
        """
        pass


    def _draw(self) -> None:
        """Override of base class.

        Here, we only draw a border, and then the individual form elements
        """
        pass

#class FileDialogWidget
