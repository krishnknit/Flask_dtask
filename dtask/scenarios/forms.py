from dtask import app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional
from os.path import join, isfile
import os


choice = [('display', 'Select options'),('first', 1), ('second', 2), ('third', 3), ('forth',4), ('fifth',5), ('tenth', 10)]
choicePCFiles = [('','')]
choiceIdxFiles = [('','')]

def get_files():
	currentPath = os.getcwd()
	compFilePath = join(currentPath, 'dtask/static/compfiles')
	files = [f for f in os.listdir(compFilePath) if isfile(join(compFilePath, f))]
	#print "COMPARE FILES: ", files
	#choiceFiles = [('Select File for comparision','Select File for comparision')]
	for file in files:
		if 'PC' in file or 'pc' in file:
			choicePCFiles.append((file, file))
		elif 'indx' in file:
			choiceIdxFiles.append((file, file))

	#return choiceFiles

class ScenariosForm(FlaskForm):
	"""docstring for HistScenarioForm"""
	default_scenario_set = BooleanField('Default Scenario Set', validators=[])
	scenario_set_name = StringField('Scenario set Name', validators=[Optional()])
	scenario_set_desc = TextAreaField('Scenario set Descriptions', validators=[Optional()])
	lock_back_period = SelectField('Lock Back Period', choices=choice)
	start_date = DateField('Start Date', validators=[DataRequired()], format='%d/%m/%Y')
	end_date = DateField('End Date', validators=[DataRequired()], format='%d/%m/%Y')
	effective_date = DateField('Effective Date', validators=[Optional()], format='%d/%m/%Y')
	expiry_date = DateField('Expiry Date', validators=[Optional()], format='%d/%m/%Y')
	liquidation_horizon = SelectField('Liquidation Horizon', choices=choice)
	liquidation_period = SelectField('Rankings per Up/Down Selection', choices=choice)
	
	
class RunAnalysisForm(FlaskForm):
	"""docstring for RunAnalysisForm"""
	get_files()
	currentPcdfFile = SelectField('Current PCDF File:', choices=choicePCFiles)
	previousPcdfFile = SelectField('Previous PCDF File:', choices=choicePCFiles)

	currentIdxFile = SelectField('Current Idx File:', choices=choiceIdxFiles)
	previousIdxFile = SelectField('Previous Idx File:', choices=choiceIdxFiles)

	compare_excel = SubmitField(label='Compare Excel')
	generate_excel = SubmitField(label='Generate Excel')

	



