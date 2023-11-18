from flask_wtf import FlaskForm, Recaptcha, RecaptchaField
from flask import current_app

from flask_user.forms import (
    unique_email_validator,
    LoginForm,
    RegisterForm
)
from flask_user import UserManager
from wtforms.widgets import TextArea, NumberInput
from wtforms import (
    StringField,
    BooleanField,
    SubmitField,
    validators,
    IntegerField,
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

class CustomRecaptcha(Recaptcha):
    def __call__(self, form, field):
        if not current_app.config.get("RECAPTCHA_ENABLE", False):
            return True
        return super(CustomRecaptcha, self).__call__(form, field)


class CustomUserManager(UserManager):
    def customize(self, app):
        self.RegisterFormClass = CustomRegisterForm
        self.LoginFormClass = CustomLoginForm

class CustomRegisterForm(RegisterForm):
    play_key_id = StringField(
        'Play Key',
        validators=[
            Optional(),
            validate_play_key,
        ]
    )
    recaptcha = RecaptchaField(
        validators=[CustomRecaptcha()]
    )

class CustomLoginForm(LoginForm):
    recaptcha = RecaptchaField(
        validators=[CustomRecaptcha()]
    )

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
        widget=NumberInput(min=0, max=9)
    )

    submit = SubmitField('Submit')


class EditEmailForm(FlaskForm):
    email = StringField(
        'E-Mail',
        validators=[
            Optional(),
            validators.Email('Invalid email address'),
            unique_email_validator,
        ]
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
            ("", ""),
            ("0", "All Characters"),
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
        choices=[(0, "No Attachment")]
    )

    attachment_count = IntegerField(
        'Attachment Count',
        default=0
    )

    submit = SubmitField('Submit')


class RescueForm(FlaskForm):

    save_world = SelectField(
        'Move to:',
        coerce=str,
        choices=[
            ("", ""),
        ],
        validators=[validators.DataRequired()]
    )

    submit = SubmitField('Submit')


class RejectPropertyForm(FlaskForm):
    rejection_reason = StringField(
        'Rejection Reason',
        widget=TextArea(),
        validators=[validators.DataRequired()]
    )

    submit = SubmitField('Submit')


class CharXMLUploadForm(FlaskForm):
    char_xml = StringField(
        'Paste minified charxml here:',
        widget=TextArea(),
        validators=[validators.DataRequired()]
    )

    submit = SubmitField('Submit')
