from flask import render_template, Blueprint, request, make_response, flash
from dtask.scenarios.forms import ScenariosForm, RunAnalysisForm
from dtask import app
import pandas as pd
import subprocess
import pymssql
import os


##############################################################################
scenarios = Blueprint('scenarios', __name__, url_prefix='/scenarios')
##############################################################################


@scenarios.route('/runanalysis', methods=['GET', 'POST'])
def run_analysis():
	form = RunAnalysisForm()
	title = "Run Comparision Analysis"

	if request.method == 'POST' and form.validate_on_submit():
		# call R script
		if form.generate_excel.data:
			resp = callRScript()
			if resp == 0:
				flash ("Excel generated!!!")
				#return "EXCEL Generated!!"
				return (render_template('scenarios/run_analysis.html', form=form, title=title))

		# compare excel files
		elif form.compare_excel.data:
			curPcdfFile = form.currentPcdfFile.data
			prePcdfFile = form.previousPcdfFile.data
			curIdxFile = form.currentIdxFile.data
			preIdxFile = form.previousIdxFile.data

			if not (curPcdfFile and prePcdfFile and curIdxFile and preIdxFile):
				flash("please select the comparision files!!")
				return (render_template('scenarios/run_analysis.html', form=form, title=title))

			path = os.getcwd() + '/dtask/static/compfiles'
			preMonPCDF = pd.read_excel(os.path.join(path, prePcdfFile), sheetname = "Sheet1")
			newMonPCDF = pd.read_excel(os.path.join(path, curPcdfFile), sheetname = "Sheet1")
			preMonIdxDF = pd.read_excel(os.path.join(path, preIdxFile), sheetname = "Sheet1")
			newMonIdxDF = pd.read_excel(os.path.join(path, curIdxFile), sheetname = "Sheet1")

			preMonPCDF.reset_index(inplace = True)
			newMonPCDF.reset_index(inplace = True)
			preMonIdxDF.reset_index(inplace = True)
			newMonIdxDF.reset_index(inplace = True)
			preMonPCDF.rename(columns = {"index": "Date"}, inplace = True)
			newMonPCDF.rename(columns = {"index": "Date"}, inplace = True)
			preMonIdxDF.rename(columns = {"index": "Date"}, inplace = True)
			newMonIdxDF.rename(columns = {"index": "Date"}, inplace = True)

			missDF = preMonPCDF[~preMonPCDF.Date.isin(newMonPCDF.Date.values)]
			newDF = newMonPCDF[~newMonPCDF.Date.isin(preMonPCDF.Date.values)]

			# print missDF['Date']
			# print "=============="
			# print newDF['Date']
			rows = []
			newRows = []
			missRows = []
			if not newDF.empty:
				for index, row in newDF.iterrows():
					#print "ROW:  ", row
					date = row['Date']
					#print "Date: ", date
					driSeries = newMonIdxDF.loc[newMonIdxDF['Date'] == str(date), 'driver']
					#print driSeries
					driver = driSeries.values[0]
					#print "DRIVER: ", driver
					rank = makeAnalysisData(date, driver, newMonPCDF, 'New')
					rows.append(rank)
			if not missDF.empty:
				for index, row in missDF.iterrows():
					#print "ROW:  ", row
					date = row['Date']
					#print "Date: ", date
					driSeries = preMonIdxDF.loc[preMonIdxDF['Date'] == str(date), 'driver']
					driver = driSeries.values[0]
					#print "DRI: ", driver
					#print "DRIVER: ", driver
					rows.append(makeAnalysisData(date, driver, preMonPCDF, 'Missing'))


			return render_template("scenarios/disp_analysis.html",rows = rows)
		else:
			pass

	if form.errors:
		for error_field, error_message in form.errors.iteritems():
			flash("Field : {field}; error : {error}".format(field=error_field, error=error_message))

	return (render_template('scenarios/run_analysis.html', form=form, title=title))


@scenarios.route('/createMBSD', methods=['GET', 'POST'])
def createMBSD():
	form = ScenariosForm()
	title = "create MBSD scenario Data"
	choices = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'tenth': 10}

	if request.method == 'POST' and form.validate_on_submit():
		bus_dt = form.start_date.data
		liq_period = choices.get(request.form.get('liquidation_period'), 0)
		look_back_period = choices.get(request.form.get('lock_back_period'), 0)

		cur = getConnection()
		#cur.execute("select * from yld_crv_hist_v")
		#cur.execute("EXEC s_SGD_CPA_raw_data_R @bus_dt = '1990-01-10', @liq_period = 10, @look_back_period = 5")
		cur.execute("EXEC s_SGD_CPA_raw_data_R @bus_dt = '{}', @liq_period = {}, @look_back_period = {}".format(bus_dt, liq_period, look_back_period))

		rows = cur.fetchall();

		# print app.config['USERNAME']
		# print app.config['PASSWORD']
		# print rows
		return render_template("scenarios/disp_create.html",rows = rows)

	return (render_template('scenarios/create.html', form=form, title=title))


@scenarios.route('/createBSD', methods=['GET', 'POST'])
def createBSD():
	form = ScenariosForm()
	title = "create BSD scenario Data"
	return (render_template('scenarios/create.html', form=form, title=title))


@scenarios.route('/createNSE', methods=['GET', 'POST'])
def createNSE():
	form = ScenariosForm()
	title = "create NSE scenario Data"
	return (render_template('scenarios/create.html', form=form, title=title))


def callRScript():
	rspt = os.getcwd() + '/dtask/myrscript.R'
	res = subprocess.check_call(['Rscript', rspt], shell = False)
	return res

def getConnection():
	con = pymssql.connect(  app.config['HOSTNAME'],
								app.config['USERNAME'],
								app.config['PASSWORD'],
								app.config['DBNAME'],
								app.config['PORT'])

	cursor = con.cursor()

	return cursor


def makeAnalysisData(date, driver, pcFile, sln):
	pcFile.sort_values(by=[str(driver.lower())], ascending = True, inplace = True)
	dfLength = len(pcFile.index)

	#print "dfLength: ", dfLength
	#print date
	# get rank
	rank = getRank(pcFile, driver, date, dfLength)
	rowNumTop = rank + 1
	rowNumBottom = "-{}".format(dfLength - rank) 

	#print "rowNumTop: ", rowNumTop
	#print "rowNumBottom: ", rowNumBottom
	#print "DATE: {}, DRIVER: {}, RANK: {}".format(date, driver, rowNumTop)
	return (str(sln),
				str(date)[:10],
				str(rowNumTop),
				str(rowNumBottom),
				str(driver)
				)

def getRank(pcFile, driver, date, dfLength):
    rank = ''

    r = pcFile.loc[pcFile['Date'] == date, 'Date']
    #print r
    rank = r.index.values[0]
    return rank
