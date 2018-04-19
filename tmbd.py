import tmdbsimple as tmdb
tmdb.API_KEY = 'c6fee39b4911de8e990c80a3ae295895'
from pprint import pprint

search = tmdb.Search()
response = search.movie(query='Toy Story')
pprint(search.results[0])
# identity = tmdb.Movies(403)
# response = identity.info()
# pprint(response)


# import requests
# import urllib
# import urllib.parse
# def imdb_id_from_title(title):
#     """ return IMDb movie id for search string
        
#         Args::
#             title (str): the movie title search string
#         Returns: 
#             str. IMDB id, e.g., 'tt0095016' 
#             None. If no match was found
#     """
#     pattern = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q={movie_title}'
#     url = pattern.format(movie_title=urllib.parse.quote(title))
#     r = requests.get(url)
#     print(r)
#     res = r
#     # sections in descending order or preference
#     for section in ['popular','exact','substring']:
#         key = 'title_' + section 
#         if key in res:
#             return res[key][0]['id']
            
# if __name__=="__main__":
#     title = "Toy Story (1995)"
#     print("{0} has id {1}".format(title, imdb_id_from_title(title)))