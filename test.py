from flask import Flask, render_template, flash, request, redirect, url_for, session, logging
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'anoop4488'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MySql
mysql = MySQL(app)

cur = mysql.connection.cursor()

result = cur.execute("select * from userRatings where userId = %s " [1])

# commit to db
print(result)

# close

cur.close()
