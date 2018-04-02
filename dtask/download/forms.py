from dtask import app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Optional

# choice = [('display', 'Select locl back period'),('first', 1), ('second', 2), ('third', 3), ('forth',4), ('fifth',5), ('tenth', 10)]

# class DownloadForm(FlaskForm):
# 	default_scenario_set = BooleanField('Default Scenario Set', validators=[])
# 	scenario_set_name = StringField('Scenario set Name', validators=[Optional()])
# 	scenario_set_desc = TextAreaField('Descriptions', validators=[Optional()])
# 	lock_back_period = SelectField('Lock Back Period', choices=choice)
# 	start_date = DateField('Start Date', validators=[DataRequired()], format='%d/%m/%Y')
# 	end_date = DateField('End Date', validators=[DataRequired()], format='%d/%m/%Y')
# 	effective_date = DateField('Effective Date', validators=[Optional()], format='%d/%m/%Y')
# 	expiry_date = DateField('Expiry Date', validators=[Optional()], format='%d/%m/%Y')
# 	liquidation_horizon = SelectField('Liquidation Horizon', choices=choice)
# 	liquidation_period = SelectField('Liquidation Period', choices=choice)
	

class DownloadCDCPForm(FlaskForm):
	start_date = StringField("Start Date", validators=[DataRequired()])
	end_date = StringField("End Date", validators=[DataRequired()])
