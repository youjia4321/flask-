from wtforms import form, fields, validators

class BlogLoginForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

class BlogRegisterForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])
    