import bs4 as bs
import urllib.request
import json

sause = urllib.request.urlopen('http://www.imdb.com/movies-in-theaters/').read()

soup = bs.BeautifulSoup(sause,'lxml')
img = soup.find_all('img',{'class': 'poster'})
data={}
for poster in img:
    title = poster.get('title')
    src = poster.get('src')
    data.update({title:src})
print(data)

with open('./jsonData/latestMovies.json', 'w') as fp:
    json.dump(data, fp, indent=4)