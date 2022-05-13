

from datetime import datetime, timedelta
import json
import requests

proxies={}

start_date = end_date = datetime.strftime(
    datetime.now() - timedelta(1) - timedelta(hours=2), '%Y-%m-%d')
id_sport = 0
perpage = 50

all_sport_id = "{"

max_id_sport = 70
while(id_sport < max_id_sport):
    LINK_API = r"https://oddspedia.com/api/v1/getMatchList?excludeSpecialStatus=0&sortBy=default&perPageDefault="+str(perpage)+"&startDate="+start_date + \
        r"T00%3A00%3A00Z&endDate="+end_date + \
        r"T23%3A59%3A59Z&geoCode=CH&status=all&sport="+str(id_sport)+"&popularLeaguesOnly=0&page=1&perPage="+str(perpage)+"&language=en"
    try:
        response1 = requests.get(url=LINK_API, proxies=proxies)
        match_list = json.loads(response1.content)

        print(id_sport, ": ", match_list['data']['sportList'][str(id_sport)]['name'])
        all_sport_id += "'"+str(id_sport)+ "'"+":'"+str(match_list['data']['sportList'][str(id_sport)]['name']) +"'"+ ", "
    except:
        print("Error: ", id_sport)
    id_sport+=1

print(all_sport_id[:-2]+"}")
