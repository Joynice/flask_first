#encoding:utf-8
import os
import pymysql
DEBUG = True
SECRET_KEY = os.urandom(24)
# host = '127.0.0.1'
# port = '3306'
# username = 'root'
# password = ''
# database = 'zl'
DB_url = 'mysql+pymysql://root@localhost:3306/zl?charset=utf8'
SQLALCHEMY_DATABASE_URI = DB_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
