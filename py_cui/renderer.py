"""Module containing the py_cui renderer. It is used to draw all of the onscreen ui_elements and items.
"""

# Author:    Jakub Wlodek
# Created:   12-Aug-2019

import curses
import py_cui
import py_cui.colors
from typing import Dict, List, Union



class Renderer:
    """Main renderer class used for drawing ui_elements to the terminal.

    Has helper functions for drawing the borders, cursor,
    and text required for the cui. All of the functions supplied by the renderer class should only be used internally.

    Attributes
    ----------
    root : py_cui.PyCUI
        The parent window
    stdscr : standard cursor
        The cursor with which renderer draws text
    color_rules : list of py_cui.colors.ColorRule
        List of currently loaded rules to apply during drawing
    """

    def __init__(self, root: 'py_cui.PyCUI', stdscr, logger):
        """Constructor for renderer object
        """

        self._root         = root
        self._stdscr       = stdscr
        self._color_rules: List['py_cui.colors.ColorRule'] = []
        self._logger       = logger

        # Define ui_element border characters
        self._border_characters = {
            'UP_LEFT'       : '+',
            'UP_RIGHT'      : '+',
            'DOWN_LEFT'     : '+',
            'DOWN_RIGHT'    : '+',
            'HORIZONTAL'    : '-',
            'VERTICAL'      : '|'
        }


    def _set_border_renderer_chars(self, border_char_set: Dict[str,str]) -> None:
        """Function that sets the border characters for ui_elements

        Parameters
        ----------
        border_characters : Dict of str to str
            The border characters as specified by user
        """
        pass


    def _set_bold(self) -> None:
        """Sets bold draw mode
        """
        pass


    def _unset_bold(self) -> None:
        """Unsets bold draw mode
        """
        pass


    def set_color_rules(self, color_rules) -> None:
        """Sets current color rules

        Parameters
        ----------
        color_rules : List[py_cui.colors.ColorRule]
            List of currently loaded rules to apply during drawing
        """
        pass


    def set_color_mode(self, color_mode: int) -> None:
        """Sets the output color mode

        Parameters
        ----------
        color_mode : int
            Color code to apply during drawing
        """
        pass


    def unset_color_mode(self, color_mode: int) -> None:
        """Unsets the output color mode

        Parameters
        ----------
        color_mode : int
            Color code to unapply during drawing
        """
        pass


    def reset_cursor(self, ui_element: 'py_cui.ui.UIElement', fill: bool=True) -> None:
        """Positions the cursor at the bottom right of the selected element

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            ui element for which to reset cursor
        fill : bool
            a flag that tells the renderer if the element is filling its grid space, or not (ex. Textbox vs textblock)
        """
        pass


    def draw_cursor(self, cursor_y: int, cursor_x: int) -> None:
        """Draws the cursor at a particular location

        Parameters
        ----------
        cursor_x, cursor_y : int
            x, y coordinates where to draw the cursor
        """
        pass


    def draw_border(self, ui_element: 'py_cui.ui.UIElement', fill: bool=True, with_title: bool=True) -> None:
        """Draws ascii border around ui element

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        fill : bool
            a flag that tells the renderer if the ui_element is filling its grid space, or not (ex. Textbox vs textblock)
        with_title : bool
            flag that tells whether or not to draw ui_element title
        """
        pass


    def _draw_border_top(self, ui_element:'py_cui.ui.UIElement', y: int, with_title: bool) -> None:
        """Internal function for drawing top of border

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        y : int
            the terminal row (top down) on which to draw the text
        with_title : bool
            Flag that tells renderer if title should be superimposed into border.
        """
        pass


    def _draw_border_bottom(self, ui_element: 'py_cui.ui.UIElement', y: int) -> None:
        """Internal function for drawing bottom of border

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        y : int
            the terminal row (top down) on which to draw the text
        """
        pass


    def _draw_blank_row(self, ui_element: 'py_cui.ui.UIElement', y: int) -> None:
        """Internal function for drawing a blank row

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        y : int
            the terminal row (top down) on which to draw the text
        """
        pass


    def _get_render_text(self, ui_element: 'py_cui.ui.UIElement', line: str, centered: bool, bordered: bool, selected, start_pos:int) -> List[List[Union[int,str]]]:
        """Internal function that computes the scope of the text that should be drawn

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        line : str
            the line of text being drawn
        centered : bool
            flag to set if the text should be centered
        bordered : bool
            a flag to set if the text should be bordered
        start_pos : int
            position to start rendering the text from.

        Returns
        -------
        render_text : str # to be checked, returns a List of [int,str]
            The text shortened to fit within given space
        """
        pass


    def _generate_text_color_fragments(self, ui_element: 'py_cui.ui.UIElement', line: str, render_text: str, selected) -> List[List[Union[int,str]]]:
        """Function that applies color rules to text, dividing them if match is found

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        line : str
            the line of text being drawn
        render_text : str
            The text shortened to fit within given space

        Returns
        -------
        fragments : list of [int, str]
            list of text - color code combinations to write
        """
        pass


    def draw_text(self, ui_element: 'py_cui.ui.UIElement', line: str, y: int, centered: bool = False, bordered: bool = True, selected: bool = False, start_pos: int = 0):
        """Function that draws ui_element text.

        Parameters
        ----------
        ui_element : py_cui.ui.UIElement
            The ui_element being drawn
        line : str
            the line of text being drawn
        y : int
            the terminal row (top down) on which to draw the text
        centered : bool
            flag to set if the text should be centered
        bordered : bool
            a flag to set if the text should be bordered
        selected : bool
            Flag that tells renderer if ui_element is selected.
        start_pos : int
            position to start rendering the text from.
        """
        pass
