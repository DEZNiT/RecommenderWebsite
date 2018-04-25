from flask import Flask, render_template, flash, request, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, RadioField, IntegerField, validators
from passlib.hash import sha256_crypt
from functools import wraps 
import bs4 as bs
import urllib.request
import json
from pprint import pprint
import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['movies']

# fiveResult = db.moviesData.find_one({"title" : "Jumanji"})
# pprint(fiveResult)
## scrapping web for latest movies in threater "Puppet Master III Toulon's Revenge"

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
    occupation = SelectField('Occupation', 
    choices = [(0, 'Other'), (1, 'Educator'), (2, 'Artist'), (3, 'Clerical'), (4, 'College Student'), (5, 'Customer Service'), (6, 'Doctor'), (7, 'Manager'),(8, 'Farmer'), (9, 'Homemaker'), (10, 'K-12 Student'), (11, 'lawer'), (12, 'Programmer'), (13, 'Retired'), (14, 'Sales'), (15, 'Scientist'), (16, 'Self Employed'), (17, 'Engineer'), (18, 'Craftsman'), (19, 'Unemployed'), (20, 'Writer')], coerce = int)
    # occupation = StringField('Occupation', [validators.Length(min=1,max=50)])
    gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    age = SelectField('Age', choices = [(1, 'Under-18'), (18, ' 18-24'), (25, ' 25-34'), (35, ' 35-44'), (45, ' 45-49'), (50, ' 50-55'), (56, '56+')], coerce = int)
    # *  1:  "Under 18"
	# * 18:  "18-24"
	# * 25:  "25-34"
	# * 35:  "35-44"
	# * 45:  "45-49"
	# * 50:  "50-55"
	# * 56:  "56+"
    password = PasswordField('Password', [validators.DataRequired(),
    validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm Password')

        # ==============================================================
        #  Function to check if user is logged in
        # ==============================================================

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, Please Loggin', 'danger')
            return redirect(url_for('login'))
    return wrap


        # ==============================================================
        # The route and function
        # to register new user
        # ==============================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name =form.name.data
        email =form.email.data
        username =form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        age = form.data['age']
        occupation = form.data['occupation']
        gender = form.data['gender']
        cur = mysql.connection.cursor()
        print(gender)
        cur.execute("SELECT COUNT(UserID) as maxUser FROM userData")
        totalUserNo = cur.fetchall()
        UserID = totalUserNo[0]['maxUser']
        print(UserID)
        # close
        cur.close()

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO userData(UserID, Gender, Age, Occupation) VALUES(%s, %s, %s, %s)", (UserID+1, gender, age, occupation))

        # commit to db
        mysql.connection.commit()

        # close

        cur.close()

        # create cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # commit to db
        mysql.connection.commit()

        # close

        cur.close()

        flash('You Are Now Registered And Can LogIn', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form= form)

        # ==============================================================
        # The route and function
        # to select category on first signup
        # ==============================================================

@app.route('/selectCategory',  methods=['GET', 'POST'])
@is_logged_in
def selectCategory():
    if request.method == 'POST':
        #print(request.form.getlist('categories'))
        categoriesList = request.form.getlist('categories')
        if(len(categoriesList ) != 3):
            flash('Please select only 3 categories', 'danger')
            return render_template('selectCategory.html')
        else:
            cur = mysql.connection.cursor()
            for i in range(len(categoriesList)):
                cur.execute("UPDATE users SET categories%s = %s WHERE email = %s", (i+1, categoriesList[i], session['email']))
                mysql.connection.commit()
            cur.close()
            print(session['email'])
            return redirect(url_for('dashboard'))
    return render_template('selectCategory.html') 

        # ==============================================================
        # The route and function
        # to login existing users
        # ==============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_candidate = request.form['password']

        # create cursor
        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE email = %s", [email])

        if result >0:
            data =cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['email'] = email
                session['id'] = data['id']+6040 
                session['name'] = data['name']
                flash('You Are Now Loggedin', 'sucess')
                return redirect(url_for('dashboard'))

            else:
                err = "Invalid Login Credentials"
                return render_template('login.html', err = err)
            cur.close();
        else:
            err = "No user Found"
            return render_template('login.html', err = err)

    return render_template('login.html')


        # ==============================================================
        # The route and function
        # to logout
        # and clear the session
        # ==============================================================
@app.route('/logout')
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('index'))

        # ==============================================================
        # The route and function
        # to dashboard
        # ==============================================================

@app.route('/dashboard')
@is_logged_in
def dashboard():
    alreadyRatedDf = {}
    id = session['id']
    idData = id-6040
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users WHERE id = %s", [idData])
    data = cur.fetchone()
    categoriesData = data['categories1']

    cur.close()
        # ===========================================================
        #         Mysql query to fetch all the rated movies by user
        # ===========================================================
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT movie.title, ratings.rating FROM movies movie INNER JOIN userRatings ratings ON ( ratings.MovieId = movie.MovieId) WHERE userId = %s", [id])
    # commit to db
    alreadyRatedtuple = cur.fetchall()
    cur.close()
         # ===========================================================
        #         Mysql query to fetch count of movies
        # ===========================================================
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT COUNT(MovieID) as totalMovieData FROM movies")
    # commit to db
    totalMovie = cur.fetchall()
    cur.close()
    totalMovie = totalMovie[0]['totalMovieData']

         # ===========================================================
        #         Mysql query to fetch count of users
        # ===========================================================

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT COUNT(UserID) as totalUserData FROM userData")
    # commit to db
    totalUsers = cur.fetchall()
    cur.close()
    totalUsers = totalUsers[0]['totalUserData']

    alreadyRated = list(alreadyRatedtuple)

    if(len(alreadyRated) < 1 and categoriesData == None):
        return redirect(url_for('selectCategory'))
    else :
        alreadyRatedFinal = []      
        for data in alreadyRated:
            titleData = data['title']
            rating = data['rating']
            title = titleData.strip()
            fiveResult = db.moviesData.find_one({"title" : title})
            if(fiveResult != None):
                data['link'] = fiveResult['poster_path']
                alreadyRatedFinal.append(data)
        totalRated = len(alreadyRatedFinal)
        return render_template('dashboard.html', alreadyRated = alreadyRatedFinal, totalUsers = totalUsers, totalMovie=totalMovie, totalRated = totalRated )
    # close
    
    
if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)
