from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

def update_profile_form(user):
    class UpdateProfileForm(FlaskForm):
        """Form for updating user profile."""

        username = StringField('Username', default=user.username, validators=[DataRequired()])
        email = StringField('E-mail', default=user.email, validators=[DataRequired(), Email()])
        image_url = StringField('Profile Image URL', default=user.image_url)
        header_image_url = StringField('Header Image URL', default=user.header_image_url)
        bio = TextAreaField("Bio", default=user.bio)
        password = PasswordField('Password', validators=[Length(min=6)])

    return UpdateProfileForm()
