import json
import requests
import sys

# search_term = sys.argv[1]
search_term = 'shoes'
API = "https://www.walmart.com/typeahead/v3/complete?term="+search_term

response3 = requests.get(
    url=API, timeout=5)
html = json.loads(response3.content)

for i in html['queries']:
    print(i['displayName'])
