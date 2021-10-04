import os

SECRET_KEY = os.urandom(24)

DEBUG = True

HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'nirsdb'
USERNAME = 'root'
PASSWORD = 'wanmidi'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD,host=HOSTNAME,port=PORT,db=DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False