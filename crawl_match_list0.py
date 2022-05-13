import requests
import json
import threading

start_date = "2022-05-10"
end_date = "2022-05-10"

csv_file = open("results.csv", "w")
csv_file.write("match_md	match_ht	match_ht_abbr	match_at	match_at_abbr	match_uri	match_league_round_name	sport_name	bookmakers_generated_at	bookmaker_name	oddsnames	time	y\n")
proxies = {}
result_data = []
done_flag = 0

def request3(c, sports, match, bookmakers_list):
    global done_flag
    done_flag = 0
    offer_id = str(c["offer_id"])
    match_id = str(match['id'])
    LINK_API_ODDMOVEMENT = r"https://oddspedia.com/api/v1/getOddsMovements?ot=100&matchId="+match_id+r"&inplay=0&wettsteuer=0&geoCode=CH&geoState=&offerId="+offer_id+"&language=en"
    response3 = requests.get(url=LINK_API_ODDMOVEMENT, proxies=proxies)
    
    oddmovement = json.loads(response3.content)
    try:
        data = oddmovement["data"]['1']
    except:
        done_flag = 1
        return
    home = data["moves"]
    for d in home:
        for temp in [match['md'],"\t",match['ht'],"\t",match['ht_abbr'],"\t",match['at'],"\t",match['at_abbr'],"\t",match['uri'],"\t",match['league_round_name'], "\t",sports[str(match["sport_id"])]['name'], "\t",bookmakers_list["generated_at"],"\t", c["bookie_name"], "\thome\t", d["t"], "\t", d["y"], "\n"]:
            result_data.append(temp)

    data = oddmovement["data"]['2']
    home = data["moves"]
    for e in home:
        for temp in [match['md'],"\t",match['ht'],"\t",match['ht_abbr'],"\t",match['at'],"\t",match['at_abbr'],"\t",match['uri'],"\t",match['league_round_name'], "\t",sports[str(match["sport_id"])]['name'],"\t",bookmakers_list["generated_at"],"\t", c["bookie_name"], "\tdraw\t",e["t"], "\t", e["y"], "\n"]:
            result_data.append(temp)

    data = oddmovement["data"]['3']
    home = data["moves"]
    for f in home:
        for temp in [match['md'],"\t",match['ht'],"\t",match['ht_abbr'],"\t",match['at'],"\t",match['at_abbr'],"\t",match['uri'],"\t",match['league_round_name'], "\t",sports[str(match["sport_id"])]['name'], "\t",bookmakers_list["generated_at"],"\t", c["bookie_name"], "\taway\t",f["t"], "\t", f["y"], "\n"]:
            result_data.append(temp)
    done_flag = 1
def run():
    dem = 0
    LINK_API=r"https://oddspedia.com/api/v1/getMatchList?excludeSpecialStatus=0&sortBy=default&perPageDefault=150&startDate="+start_date+r"T00%3A00%3A00Z&endDate="+end_date+r"T23%3A59%3A59Z&geoCode=VN&status=all&sport=&popularLeaguesOnly=1&page=1&perPage=150&language=en"

    response1 = requests.get(url=LINK_API, proxies=proxies)

    match_list = json.loads(response1.content)

    # sport list
    sports = match_list['data']['sportList']

    matchs = match_list['data']['matchList']
    for match in matchs:

        match_key = match['uri'][match['uri'].rfind('-')+1:]
        if(match_key.find("?m=") != -1):
            match_key = match_key[:match_key.find("?m=")]
        LINK_API_MATCHODD=r"https://oddspedia.com/api/v1/getMatchOdds?wettsteuer=0&geoCode=CH&bookmakerGeoCode=CH&geoState=&matchKey="+match_key+r"&oddGroupId=1&inplay=1&language=en"

        response2 = requests.get(url=LINK_API_MATCHODD, proxies=proxies)
        try:
            bookmakers_list = json.loads(response2.content)
        except:
            pass
        # i want to found the offer id
        for a in bookmakers_list['data']['inplay']:
            if(a['id'] == 1):
                for b in a['periods']:
                    if(b["ot_id"] == 100):
                        odds = b["odds"]
                        for c in odds:
                            dem += 1
                            
                            # print("loading"+str(dem))
                            threading.Thread(target=request3,args=(c, sports, match, bookmakers_list)).start()
                        while(not done_flag):
                            pass
    print("Loaded successful!")
    print("Writting to csv file!")
    for i in result_data:
        csv_file.write(str(i))
    csv_file.close()
    print("Successful!")

if __name__ == "__main__":
    run()
