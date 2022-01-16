from flask_wtf import FlaskForm
from flask import current_app

from flask_user.forms import (
    unique_email_validator,
    password_validator,
    unique_username_validator
)
from flask_user import UserManager
from wtforms.widgets import TextArea, NumberInput
from wtforms import (
    StringField,
    HiddenField,
    PasswordField,
    BooleanField,
    SubmitField,
    validators,
    IntegerField,
    StringField,
    SelectField
)

from wtforms.validators import DataRequired, Optional
from app.models import PlayKey

def validate_play_key(form, field):
    """Validates a field for a valid phone number
    Args:
        form: REQUIRED, the field's parent form
        field: REQUIRED, the field with data
    Returns:
        None, raises ValidationError if failed
    """
    # jank to get the fireign key that we need back into the field
    if current_app.config["REQUIRE_PLAY_KEY"]:
        field.data = PlayKey.key_is_valid(key_string=field.data)
    return


class CustomUserManager(UserManager):
    def customize(self, app):
        self.RegisterFormClass = CustomRegisterForm


class CustomRegisterForm(FlaskForm):
    """Registration form"""
    next = HiddenField()
    reg_next = HiddenField()

    # Login Info
    email = StringField(
        'E-Mail',
        validators=[
            Optional(),
            validators.Email('Invalid email address'),
            unique_email_validator,
        ]
    )

    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            unique_username_validator,
        ]
    )

    play_key_id = StringField(
        'Play Key',
        validators=[
            Optional(),
            validate_play_key,
        ]
    )

    password = PasswordField('Password', validators=[
        DataRequired(),
        password_validator
    ])
    retype_password = PasswordField('Retype Password', validators=[
        validators.EqualTo('password', message='Passwords did not match')
    ])

    invite_token = HiddenField('Token')

    submit = SubmitField('Register')

class CreatePlayKeyForm(FlaskForm):

    count = IntegerField(
        'How many Play Keys to create',
        validators=[DataRequired()]
    )
    uses = IntegerField(
        'How many uses each new play key will have',
        validators=[DataRequired()]
    )
    submit = SubmitField('Create!')

class EditPlayKeyForm(FlaskForm):

    active = BooleanField(
        'Active'
    )

    uses = IntegerField(
        'Play Key Uses'
    )

    notes = StringField(
        'Notes',
        widget=TextArea()
    )

    submit = SubmitField('Submit')


class EditGMLevelForm(FlaskForm):

    gm_level = IntegerField(
        'GM Level',
        widget=NumberInput(min = 0, max = 9)
    )

    submit = SubmitField('Submit')


class ResolveBugReportForm(FlaskForm):

    resolution = StringField(
        'Resolution',
        widget=TextArea(),
        validators=[DataRequired()]
    )

    submit = SubmitField('Submit')


class SendMailForm(FlaskForm):

    recipient = SelectField(
        'Recipient: ',
        coerce=str,
        choices=[
            ("",""),
            ("0","All Characters"),
        ],
        validators=[validators.DataRequired()]
    )

    subject = StringField(
        'Subject',
        validators=[validators.DataRequired()]
    )

    body = StringField(
        'Body',
        widget=TextArea(),
        validators=[validators.DataRequired()]
    )

    attachment = SelectField(
        "Attachment",
        coerce=str,
        choices=[(0,"No Attachment")]
    )

    attachment_count = IntegerField(
        'Attachment Count',
        default=0
    )

    submit = SubmitField('Submit')
