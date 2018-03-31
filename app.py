from flask import Flask, render_template, flash, request, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

import bs4 as bs
import urllib.request
import json

## scrapping web for latest movies in threater

sause = urllib.request.urlopen('http://www.imdb.com/movies-in-theaters/').read()

soup = bs.BeautifulSoup(sause,'lxml')
img = soup.find_all('img',{'class': 'poster'})
moviesInTheater={}
for poster in img:
    title = poster.get('title')
    src = poster.get('src')
    moviesInTheater.update({title:src})
#print(data)

app = Flask(__name__)
# config mySql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'anoop4488'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MySql
mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('home.html', moviesInTheater = moviesInTheater)
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1,max=50)])
    username = StringField('UserName', [validators.Length(min=4,max=20)])
    email = StringField('Email', [validators.Length(min=4,max=50)])
    password = PasswordField('Password', [validators.DataRequired(),
    validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name =form.name.data
        email =form.email.data
        username =form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # create cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # commit to db
        mysql.connection.commit()

        # close

        cur.close()

        flash('You Are Now Registered And Can LogIn', 'sucess')
        return redirect(url_for('index'))
    return render_template('register.html', form= form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and form.validate():
        email = request.form['email']
        password_candidate = request.form['password']

        # create cursor
        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE email = %s", [email])

        if result >0:
            data =cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                app.logger.info(' PASSWORD MATCHED')
        
        else:
            app.logger.info('NO USER')

        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # commit to db
        mysql.connection.commit()

        # close

        cur.close()

        flash('You Are Now Registered And Can LogIn', 'sucess')
        return redirect(url_for('index'))
    return render_template('login.html', form= form)


if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)
