from wtforms import Form,StringField,  EmailField, PasswordField, SubmitField, validators

class Sign_up_form(Form):
    """Will display form fields for sign up"""
    user_name = StringField(label="What's your name ?")
    email = EmailField(label= 'Enter your email',validators=[validators.input_required()])
    password = PasswordField(label='Enter your password', validators=[validators.input_required()])
    submit = SubmitField(label="Sign Up")
class Login_form(Form):
    """Will display form fields for login"""
    email = EmailField(label= 'Enter your email',validators=[validators.input_required()])
    password = PasswordField(label='Enter your password', validators=[validators.input_required()])
    submit = SubmitField(label="Login")

    