from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField

class AssessmentForm(Form):
    name = StringField('name', [validators.Length(min=4, max=20)])
    status = IntegerField('status', [validators.NumberRange(min=0, max=10),validators.InputRequired()]) 