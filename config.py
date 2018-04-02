class Config(object):
	"""docstring for Config"""
	DEBUG = False
	SECRET_KEY = 'p9Bv<3Eid9%$i01'
	WTF_CSRF_SECRET_KEY = 'e8dd66459b397b76878b8ee3ec654120'
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
	pass

class DevelopementConfig(Config):
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	# database details
	#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:cybage@123@localhost/dreamteam_db'
	SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://SA:cybage@123@localhost:1433/TestDB'
	HOSTNAME = 'localhost'
	PORT = '1433'
	DBNAME = 'TestDB'
	USERNAME = 'SA'
	PASSWORD = 'cybage@123'

	# download url
	DOWNLOAD_URL = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&series=988cd0b770ba0ad45005ee731c6f93e4&lastobs=&from=%s&to=%s&filetype=csv&label=include&layout=seriescolumn'
		