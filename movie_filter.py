import requests
import json

API_KEY = 'f3a05026119d09f84c9aaef927a18ac2'
DIRECTOR_ID = 138  # Quentin Tarantino id
ORDER = 'desc'
SORT = 'release_date.%s' % ORDER

""""
This script prints the title of the movies where Quentin Tarantino was part of the crew
"""

QUERY = {
    'api_key': API_KEY,
    'with_crew': DIRECTOR_ID,
    'sort_by': SORT,
}
URL = 'https://api.themoviedb.org/3/discover/movie'

QUERY = '&'.join(['%s=%s' % (key, value) for key, value in QUERY.items()])
URL = '%s?%s' % (URL, QUERY)

data = requests.get(URL)
result = json.loads(data.text)

for movie in result['results']:
    print(movie['title'])

print('Total Movies: %s' % len(result['results']))