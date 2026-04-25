"""Module containing py_cui logging utilities
"""

# Author:    Jakub Wlodek
# Created:   18-Mar-2020

import os
import logging
import inspect
import py_cui
import datetime
from typing import Any, Optional, Tuple


def _enable_logging(logger: 'PyCUILogger', replace_log_file: bool=True, filename: str='py_cui.log', logging_level=logging.DEBUG) :
    """Function that creates basic logging configuration for selected logger

    Parameters
    ----------
    logger : PyCUILogger
        Main logger object
    filename : os.Pathlike
        File path for output logfile
    logging_level : logging.LEVEL, optional
        Level of messages to display, by default logging.DEBUG

    Raises
    ------
    PermissionError
        py_cui logs require permission to cwd to operate.
    TypeError
        Only the custom PyCUILogger can be used here.
    """
    pass

def _initialize_logger(py_cui_root: 'py_cui.PyCUI', name: Optional[str]=None, custom_logger: bool=True) :
    """Function that retrieves an instance of either the default or custom py_cui logger.
    
    Parameters
    ----------
    py_cui_root : py_cui.PyCUI
        reference to the root py_cui window
    name : str, optional
        The name of the logger, by default None
    custom_logger : bool, optional
        Use a custom py_cui logger, by default True
    
    Returns
    -------
    logger : py_cui.debug.PyCUILogger
        A custom logger that allows for live debugging
    """
    pass


class LiveDebugImplementation(py_cui.ui.MenuImplementation):
    """Implementation class for the live debug menu - builds off of the scroll menu implementation

    Attributes
    ----------
    level : int
        Debug level at which to display messages. Can be separate from the default logging level
    _buffer_size : List[str]
        Number of log messages to keep buffered in the live debug window
    """


    def __init__(self, parent_logger):
        """Initializer for LiveDebugImplementation
        """

        super().__init__(parent_logger)
        self.level      = logging.ERROR
        # Make default buffer size 100
        self._buffer_size           = 100


    def print_to_buffer(self, msg: str, log_level) -> None:
        """Override of default MenuImplementation add_item function

        If items override the buffer pop the oldest log message

        Parameters
        ----------
        msg : str
            Log message to add
        """
        pass


class LiveDebugElement(py_cui.ui.UIElement, LiveDebugImplementation):
    """UIElement class for the live debug utility. extends from base UIElement class and LiveDebugImplementation
    """

    def __init__(self, parent_logger):
        """Initializer for LiveDebugElement class
        """

        LiveDebugImplementation.__init__(self, parent_logger)
        py_cui.ui.UIElement.__init__(self, 'LiveDebug', 'PyCUI Live Debug', None, parent_logger)

        # Initialize these to some dummy values to start with - will get overriden once 
        # parent logger is assigned a root py_cui window
        self._start_x = 5
        self._start_y = 5
        self._stop_x = 150
        self._stop_y = 25


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base UI element class function. Sets start position relative to entire UI size

        Returns
        -------
        start_x, start_y : int, int
            Start position x, y coords in terminal characters
        """
        pass


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base UI element class function. Sets stop position relative to entire UI size

        Returns
        -------
        stop_x, stop_y : int, int
            Stop position x, y coords in terminal characters
        """
        pass


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function, handles mouse press in menu

        Parameters
        ----------
        x, y : int
            Coordinates of mouse press
        mouse_event : int
            Key code for py_cui mouse event
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class function.

        Essentially the same as the ScrollMenu widget _handle_key_press, with the exception that Esc breaks
        out of live debug mode.

        Parameters
        ----------
        key_pressed : int
            The keycode of the pressed key
        """
        pass
        

    def _draw(self) -> None:
        """Overrides base class draw function. Mostly a copy of ScrollMenu widget - but reverse item list
        """
        pass


class PyCUILogger(logging.Logger):
    """Custom logger class for py_cui, extends the base logging.Logger Class
    
    Attributes
    ----------
    py_cui_root : py_cui.PyCUI
        The root py_cui program for which the logger runs
    live_debug : bool
        Flag to toggle live debugging messages
    """

    def __init__(self, name):
        """Initializer for the PyCUILogger helper class

        Raises
        ------
        TypeError
            If root variable instance is not a PyCUI object raise a typeerror
        """

        super(PyCUILogger, self).__init__(name)
        self._live_debug_enabled    = False
        self.py_cui_root            = None
        self._live_debug_element    = LiveDebugElement(self)

 
    def is_live_debug_enabled(self):
        pass

    def toggle_live_debug(self):
        pass

    def draw_live_debug(self):
        """Function that draws the live debug UI element if applicable
        """
        pass


    def _assign_root_window(self, py_cui_root: 'py_cui.PyCUI') -> None:
        """Function that assigns a PyCUI root object to the logger. Important for live-debug hooks

        Parameters
        ----------
        py_cui_root : PyCUI
            Root PyCUI object for the application
        """
        pass


    def _get_debug_text(self, text: str) -> str:
        """Function that generates full debug text for the log

        Parameters
        ----------
        text : str
            Log message

        Returns
        -------
        msg : str
            Log message with function, file, and line num info
        """
        pass
    
    
    def info(self, msg: Any, *args, **kwargs) -> None : # to overcome signature mismatch in error
        """Override of base logger info function to add hooks for live debug mode
        
        Parameters
        ----------
        text : str
            The log text ot display
        """
        pass


    def debug(self, msg: str, *args, **kwargs) -> None:
        """Override of base logger debug function to add hooks for live debug mode
        
        Parameters
        ----------
        text : str
            The log text ot display
        """
        pass


    def warn(self, msg: str, *args, **kwargs) -> None:
        """Override of base logger warn function to add hooks for live debug mode
        
        Parameters
        ----------
        text : str
            The log text ot display
        """
        pass


    def error(self, msg: str, *args, **kwargs) -> None:
        """Override of base logger error function to add hooks for live debug mode
        
        Parameters
        ----------
        text : str
            The log text ot display
        """
        pass


    def critical(self, msg: str, *args, **kwargs) -> None:
        """Override of base logger critical function to add hooks for live debug mode
        
        Parameters
        ----------
        text : str
            The log text ot display
        """
        pass

