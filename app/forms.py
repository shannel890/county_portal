from flask_security import RegisterForm, LoginForm,Form
from wtforms import StringField, SelectField, TelField # Use wtforms for field types
from wtforms.validators import DataRequired, Optional, ValidationError, Length
from app.models.county import County # Assuming this import path is correct

# Note: Flask-Security's RegisterForm and LoginForm already inherit from wtforms.Form,
# so explicitly importing Form from flask_security.forms or wtforms is often not strictly
# necessary if you're only extending these specific forms.
# However, if you were defining a standalone form not extending Flask-Security's base forms,
# you would typically import `Form` from `wtforms`.

class ExtendRegisterForm(RegisterForm):
    """Enhanced registration form with additional user fields for county services.
    """
    first_name = StringField(
        'First Name', # Improved label for display
        validators=[
            DataRequired('First name is required.'), # Clearer error message
            Length(min=2, max=50, message='First name must be between 2 and 50 characters.')
        ]
    )

    last_name = StringField(
        'Last Name', # Improved label for display
        validators=[
            DataRequired('Last name is required.'), # Clearer error message
            Length(min=2, max=50, message='Last name must be between 2 and 50 characters.')
        ]
    )

    # Changed to TelField for semantic correctness and better browser support for phone numbers
    # Made Optional to align with the template's "(Optional)" placeholder
    phone_number = TelField(
        'Phone Number', # Improved label for display
        validators=[
            Optional(), # Allow the field to be empty
            Length(min=10, max=20, message='Phone number must be between 10 and 20 characters.')
        ]
    )

    county_id = SelectField(
        'County', # Improved label for display
        validators=[
            DataRequired(message='Please select your county.') # Clearer error message
        ],
        coerce=int, # Ensures the selected value is cast to an integer
        choices=[] # Choices are populated dynamically in __init__
    )

    def __init__(self, *args, **kwargs):
        """Initializes the form and dynamically populates county choices."""
        super().__init__(*args, **kwargs)
        # Populate county choices dynamically from the database
        # Ensure County.query is correctly configured (e.g., with SQLAlchemy session)
        self.county_id.choices = [
            (county.id, county.name)
            for county in County.query.filter_by(active=True).order_by(County.name).all()
        ]
        # Add a default "Select County" option at the beginning
        # The value 0 is used to indicate no selection, handled by validate_county_id
        self.county_id.choices.insert(0, (0, 'Select your county...'))

    def validate_phone_number(self, field):
        """Custom validator for phone number format and cleaning."""
        if field.data: # Only validate if data is provided (since it's Optional)
            # Remove any non-digit characters for validation and storage
            digits_only = ''.join(filter(str.isdigit, field.data))
            if len(digits_only) < 10:
                raise ValidationError('Phone number must contain at least 10 digits.')
            # Update field data with cleaned format for consistency
            field.data = digits_only

    def validate_county_id(self, field):
        """Ensure a valid county is selected (i.e., not the default placeholder)."""
        if field.data == 0: # Checks if the default placeholder value (0) is selected
            raise ValidationError('Please select your county.')


class ExtendedLoginForm(LoginForm):
    """Enhanced login form with better styling and placeholder support."""

    # Corrected typo: __init__ instead of _init_
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholder text and styling classes using render_kw
        self.email.render_kw = {
            'placeholder': 'Enter your email address',
            'class': 'form-control form-control-lg'
        }
        self.password.render_kw = {
            'placeholder': 'Enter your password',
            'class': 'form-control form-control-lg'
        }


class UserProfileForm(Form):
    """Form for users to update their profile information."""

    first_name = StringField(
        'First Name',
        validators=[DataRequired('First name is required.'), Length(min=2, max=50)]
    )

    last_name = StringField(
        'Last Name',
        validators=[DataRequired('Last name is required.'), Length(min=2, max=50)]
    )

    # Using TelField and Optional for phone number in profile update,
    # which is a common and flexible approach.
    phone_number = TelField(
        'Phone Number',
        validators=[Optional(), Length(min=10, max=15, message='Phone number must be between 10 and 15 characters.')]
    )

    def validate_phone_number(self, field):
        """Custom validator for phone number format and cleaning."""
        if field.data: # Only validate if data is provided
            digits_only = ''.join(filter(str.isdigit, field.data))
            if len(digits_only) < 10:
                raise ValidationError('Phone number must contain at least 10 digits.')
            field.data = digits_only