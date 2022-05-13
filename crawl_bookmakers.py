import requests
import json

match_key = 38
LINK_API=r"https://oddspedia.com/api/v1/getMatchOdds?wettsteuer=0&geoCode=CH&bookmakerGeoCode=CH&geoState=&matchKey="+str(match_key)+"&oddGroupId=1&inplay=0&language=en"

proxies = {}
response = requests.get(url=LINK_API, proxies=proxies)

bookmakers_list = json.loads(response.content)

print(bookmakers_list["generated_at"])

odds = bookmakers_list['data']['prematch'][0]['periods'][0]['odds']
for i in odds:
    print(i["bid"], "|", i["bookie_name"], '|', i["offer_id"])
