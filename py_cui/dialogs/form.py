"""Form widget for py_cui. Allows for giving user several fillable text fields in one block
"""

from typing import Any, Callable, Dict, List, Optional, Tuple
import py_cui.ui
import py_cui.widgets
import py_cui.popups


class DuplicateFormKeyError(Exception):
    """Error thrown when a duplicate form field key is passed
    """

    pass


class FormField(py_cui.ui.TextBoxImplementation):
    """Class containing basic logic of a field in a form

    Attributes
    ----------
    _fieldname : str
        Title of the field
    _required : bool
        Toggle for making the field be required
    """

    def __init__(self, fieldname: str, initial_text: str, password: bool, required: bool, logger):
        """Initializer for base FormFields
        """

        super().__init__(initial_text, password, logger)
        self._fieldname = fieldname
        self._required = required


    def get_fieldname(self) -> str:
        """Getter for field name

        Returns
        -------
        fieldname : str
            Title of the field
        """
        pass


    def is_valid(self) -> Tuple[bool,Optional[str]]:
        """Function that checks if field is valid.

        This function can be implemented by subclasses to support different
        field types (ex. emails etc.)

        Returns
        -------
        is_valid : bool
            True of valid conditions are met, false otherwise
        msg : str
            Message explaining problem. None if valid
        """
        pass


    def is_required(self) -> bool:
        """Checks if field is required

        Returns
        -------
        required : bool
            True if required, false otherwise
        """
        pass


class FormFieldElement(py_cui.ui.UIElement, FormField):
    """Extension of UI element representing an individual field in the form

    Attributes
    ----------
    _field_index : int
        The index of the field in the form
    _parent_form : FormPopup / Form
        The parent UI Element that contains the form element
    """

    def __init__(self, parent_form, field_index: int, field, init_text: str, passwd: bool, required: bool, renderer: 'py_cui.renderer.Renderer', logger):
        """Initializer for the FormFieldElement class
        """

        self._parent_form = parent_form
        self._field_index = field_index
        py_cui.ui.UIElement.__init__(self, 0, field, renderer, logger)
        FormField.__init__(self, field, init_text, passwd, required, logger)
        self._help_text = 'Press Tab to move to the next field, or Enter to submit.'
        self._padx = 0
        self._pady = 0
        self._selected = False
        self.update_height_width()


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute start position

        Returns
        -------
        field_start_x, field_start_y : int, int
            The position in characters in the terminal window to start the Field element
        """
        pass


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute stop position

        Returns
        -------
        field_stop_x, field_stop_y : int, int
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


class FormImplementation(py_cui.ui.UIImplementation):
    """Main implementation class for the form widget/popup

    Attriubutes
    -----------
    _form_fields : List[FormField]
        The current fields in the form
    _required_fields : List[str]
        List for identifying required fields
    _selected_form_index : int
        Index of currently selected form
    _on_submit_action : no-arg or lambda function
        Function fired when submit is called
    """

    def __init__(self, field_implementations: List['FormField'], required_fields: List[str], logger):
        """Initializer for the FormImplemnentation class
        """

        super().__init__(logger)
        self._form_fields = field_implementations
        self._required_fields = required_fields

        self._selected_form_index = 0
        self._on_submit_action: Optional[Callable[[],Any]] = None


    def get_selected_form_index(self) -> int:
        """Getter for selected form index

        Returns
        -------
        selected_form_index : int
            the index of currently selected field
        """
        pass

    def set_selected_form_index(self, form_index: int) -> None:
        """Setter for selected form index

        Parameters
        ----------
        selected_form_index : int
            the index of the new selected field
        """
        pass


    def set_on_submit_action(self, on_submit_action: Callable[[],Any]):
        """Setter for callback on submit

        Parameters
        ----------
        on_submit_action : no-arg or lambda function
            Function fired when user 'submits' form
        """
        pass


    def jump_to_next_field(self) -> None:
        """Function used to jump between form fields
        """
        pass


    def is_submission_valid(self) -> Tuple[bool,Optional[str]]:
        """Function that checks if all fields are filled out correctly

        Returns
        -------
        is_valid : bool
            True of valid conditions are met, false otherwise
        msg : str
            Message explaining problem. None if valid
        """
        pass


    def get(self) -> Dict[str,str]:
        """Gets values entered into field as a dictionary

        Returns
        -------
        field_entries : dict
            A dictionary mapping field names to user inputs
        """
        pass


class Form(py_cui.widgets.Widget, FormImplementation):
    """Main Widget class extending the FormImplementation. TODO
    """

    pass


class InternalFormPopup(py_cui.popups.MessagePopup):
    """A helper class for abstracting a message popup tied to a parent popup

    Attributes
    ----------
    parent : FormPopup
        The parent form popup that spawned the message popup
    """

    def __init__(self, parent: 'FormPopup', *args):
        """Initializer for Internal form Popup
        """

        super().__init__(*args)
        self._parent = parent


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class, close in parent instead of root
        """
        pass


class FormPopup(py_cui.popups.Popup, FormImplementation):
    """Main Popup extension class for forms.

    Attributes
    ----------
    num_fields : int
        Number of fields added to form
    form_fields : List[FormFieldElement]
        individual form field ui element objects
    internal_popup : InternalFormPopup
        A popup spawned in the event of an invalid submission
    """

    def __init__(self, root, fields, passwd_fields, required_fields, fields_init_text, title, color, renderer, logger):

        pass


    def get_num_fields(self) -> int:
        """Getter for number of fields

        Returns
        -------
        num_fields : int
            Number of fields in form
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


    def update_height_width(self) -> None:
        """Override of base class function

        Also updates all form field elements in the form
        """
        pass


    def _handle_key_press(self, key_pressed: int) -> None:
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
