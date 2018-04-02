from flask import render_template, Blueprint, request, make_response
from dtask.download.forms import DownloadCDCPForm
from dtask import app, db
from datetime import date
import traceback
import requests
import pymssql
import os
import re

##################################################################
download = Blueprint('download', __name__, url_prefix='/download')
##################################################################


@download.route('/downloadcdcp', methods=['GET', 'POST'])
def download_cdcp():
	form = DownloadCDCPForm()
	title = 'Download CD/CP data'

	if request.method == 'POST' and form.validate_on_submit():
		start_date = form.start_date.data
		end_date = form.end_date.data
		sdate = start_date.split('/')
		edate = end_date.split('/')
		sd = re.sub(r'/','', start_date)
		ed = re.sub(r'/','', end_date)
		file = 'dataAnalysis/static/downloadFiles/FRB_H15_' + sd + '_' + ed + '.csv'
		path = os.getcwd()
		fname = os.path.join(path, file)
		rows = []
		header = []

		url = get_frb_url(dtStart=date(int(sdate[2]), int(sdate[0]), int(sdate[1])),
						  dtEnd=date(int(edate[2]), int(edate[0]), int(edate[1])))
		#url = get_frb_url(dtStart=date(2017, 11, 02), dtEnd=date(2017, 11, 15))
		#frb_site = urllib.urlopen(url)
		frb_site = requests.get(url)
		#text = frb_site.read().strip()
		text = frb_site.text
		#print "TEXT: ", frb_site.text

		with open(fname, 'w') as wf:
			wf.write(text)

		with open(fname, 'r') as rf:
			cnt = 0
			try:
				con = getConnection()
				cursor = con.cursor()
				for line in rf:
					cnt += 1
					if cnt < 6:
						continue
					elif cnt == 6:
						data = line.split(',')
						header.extend([data[0], data[1], data[2]])
					else:
						data = line.split(',')
						rows.append((data[0], data[1], data[2]))

						dly_dt = 'NULL' if 'ND' in data[0] else data[0]
						fcp_val =  'NULL' if 'ND' in data[1] else data[1]
						nfcp_val = 'NULL' if 'ND' in data[2] else data[2]
						
						cursor.execute("INSERT INTO hist_cd_cp VALUES ('{}', {}, {})".format(dly_dt, fcp_val, nfcp_val))
						con.commit()
			except Error as e:
				app.logger.warning(e)
				print e
			finally:
				cursor.close()
				con.close()
		#print rows
		return render_template("download/list.html", rows=rows, header=header)

	return (render_template('download/form.html', form=form, title=title))

@download.route("/database")
def getDatabase():
	return "This page is under construction....."
	#return render_template('histscenario/database.html')

@download.route("/excel")
def getExcel():
	return "This page is under construction....."
	#return render_template('histscenario/excel.html')

def get_frb_url(dtStart, dtEnd):
	downloadUrl = app.config['DOWNLOAD_URL']

	url = downloadUrl % (dtStart.strftime('%m/%d/%Y'), dtEnd.strftime('%m/%d/%Y'))

	return url

def getConnection():
	con = pymssql.connect(  	app.config['HOSTNAME'],
								app.config['USERNAME'],
								app.config['PASSWORD'],
								'IRS_DFM',
								app.config['PORT'])

	return con
