from flask import Flask, render_template
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

@app.route('/')
def index():
    return render_template('home.html', moviesInTheater = moviesInTheater)

if __name__ == '__main__':
    app.run(debug=True)
