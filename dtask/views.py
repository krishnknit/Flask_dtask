from flask import render_template, request, session, g
from dtask import app


@app.route("/")
@app.route("/home/", methods=['GET'])
def home():
	title = 'Data Analysis'
	return (render_template('home.html', title=title))

@app.route("/healthcheck")
def healthcheck():
	out = 'we are UP'
	return out
	
