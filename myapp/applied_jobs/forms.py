from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class AppliedJobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    date_applied = StringField('Company', validators=[DataRequired()])
    accepted = BooleanField('Accepted', default=False)
    in_process = BooleanField('InProcess', default=False)
    rejected = BooleanField('Rejected', default=False)
    submit = SubmitField('Post')
