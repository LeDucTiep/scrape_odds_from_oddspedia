import os
import random
import sqlite3
import sys
import time
import requests
import json
import threading
from datetime import datetime, timedelta
from pytz import timezone

# 12 hours
TIME_WAIT_FOR_NEXT_LAUNCH = 12 * 60 * 60
DATABASE_PATH = "database.db"
TIMEOUT_FOR_API = 10
separate_char = ","
is_run_multithreading = False

search_markets = {
    1: "Full Time Result",
    3: "Asian Handicap",
    4: "Total Goals",
    5: "Draw No Bet",
    6: "European Handicap",
    7: "Double Chance",
    8: "Correct Score",
    9: "Half Time / Full Time",
    11: "Both Teams to Score",
    10: "Odd or Even",
    12: "First Team to Score",
    13: "Asian Handicap Corners",
    16: "Asian Handicap Cards",
    18: "Corners Odd or Even",
    19: "Total Cards Over/Under",
    21: "Clean Sheet",
    23: "To Win to Nil",
    24: "To Win From Behind",
    25: "To Win Both Halves",
    26: "To Score a Penalty",
    27: "To Score in Both Halves",
    30: "Next Goal"}

# run the file get_all_sport_id.py to update this list
all_sport_will_be_scraped = {'1': 'Football', '2': 'Ice Hockey', '3': 'Basketball', '5': 'Tennis',
                             '6': 'American Football', '7': 'Baseball', '8': 'Handball', '12': 'Golf', '13': 'Volleyball', '68': 'Horse Racing'}
bookmaker_list = ['Pinnacle', '22Bet', 'Melbet', 'N1Bet', 'Dafabet', 'nextbet', 'Ladbrokes',
                  'betwinner', '1XBit', 'interwetten', 'bet365', 'unibet', '888sport']
# Get the yesterday
yesterday = datetime.now(timezone('UTC')) - timedelta(days=1)
start_date = end_date = datetime.strftime(
    yesterday, '%Y-%m-%d')


def get_records_count():
    cmd = '''select count(*)
             from results'''
    with sqlite3.connect(DATABASE_PATH) as conn:
        try:
            cur = conn.execute(cmd)
            conn.commit()
        except:
            return get_records_count()
        for i in cur:
            return i[0]
    time.sleep(0.5)
    return get_records_count()


def insert_to_database(WHICH_ODD, DATE, TEAM_HOME, TEAM_AWAY, COUNTRY, COMPETITION, SCORE, STATUS, SPORTNAME, ODD_TYPE, BOOKMAKER, ODD_NAME, FullTime_1stHalf_etc, TIMESTAMP, ODD):
    if(WHICH_ODD == None):
        return
    if(DATE == None):
        return
    if(TEAM_HOME == None):
        return
    if(TEAM_AWAY == None):
        return
    if(COUNTRY == None):
        return
    if(COMPETITION == None):
        return
    if(SCORE == None):
        return
    if(STATUS == None):
        return
    if(SPORTNAME == None):
        return
    if(ODD_TYPE == None):
        return
    if(BOOKMAKER == None):
        return
    if(ODD_NAME == None):
        return
    if(FullTime_1stHalf_etc == None):
        return
    if(TIMESTAMP == None):
        return
    if(ODD == None):
        return
    try:
        cmd = "insert into results values ('"+WHICH_ODD.replace("'", "''")+"','"+DATE.replace("'", "''")+"','"+TEAM_HOME.replace("'", "''")+"','"+TEAM_AWAY.replace("'", "''")+"','"+COUNTRY.replace("'", "''")+"','"+COMPETITION.replace("'", "''")+"','"+SCORE.replace("'", "''") + \
            "','"+STATUS.replace("'", "''")+"','"+SPORTNAME.replace("'", "''")+"','"+ODD_TYPE.replace("'", "''")+"','"+BOOKMAKER.replace("'", "''")+"','" + \
            ODD_NAME.replace("'", "''")+"','"+FullTime_1stHalf_etc.replace("'", "''") + \
            "','"+TIMESTAMP.replace("'", "''")+"','" + \
            ODD.replace("'", "''")+"')"
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.execute('PRAGMA encoding="UTF-8";')
            conn.execute(cmd)
            conn.commit()
    except Exception as e:
        if(str(e).find('lock') != -1 or str(e).find('attempt to write a readonly database') != -1):
            time.sleep(random.randint(0, 2))
            return insert_to_database(WHICH_ODD, DATE, TEAM_HOME, TEAM_AWAY, COUNTRY, COMPETITION, SCORE, STATUS, SPORTNAME, ODD_TYPE, BOOKMAKER, ODD_NAME, FullTime_1stHalf_etc, TIMESTAMP, ODD)
        if(str(e).lower().find('unique') == -1):
            print(str(e))


def get_data_from_database():
    results = []
    cmd = '''select which_odd,
        data,
        team_home,
        team_away,
        country,
        competition,
        score,
        status,
        sportname,
        odd_type,
        bookmaker,
        odd_name,
        FullTime_1stHalf_etc,
        timestamp,
        odd 
        from results'''
    with sqlite3.connect(DATABASE_PATH) as conn:
        try:
            conn.execute('PRAGMA encoding="UTF-8";')
            cur = conn.execute(cmd)
            conn.commit()
        except:
            return get_data_from_database()
        for i in cur:
            results.append(i)
    return results


def get_input_from_user():
    return input("is the script running on the server? [y/n] ")


input_text = get_input_from_user()

while(input_text != 'y' and input_text != 'n'):
    input_text = get_input_from_user()

if(input_text.lower() == 'y'):
    hours_less = 2
else:
    hours_less = 0


def format_to_time_zone_of_Switzerland(date_time_str):
    global hours_less
    format = "%Y-%m-%d %H:%M:%S"
    date_time_str = str(date_time_str)
    if(date_time_str.find("+") != -1):
        if(date_time_str[-3:] == '+00'):
            date_time_obj = datetime.strptime(date_time_str[:-3], format)
            date_time_obj += timedelta(hours=hours_less)
            return date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
        input("Error: new time format " + date_time_str)
    else:
        date_time_obj = datetime.strptime(date_time_str, format)
        date_time_obj += timedelta(hours=hours_less)
        return date_time_obj.strftime("%Y-%m-%d %H:%M:%S")


proxies = {}


def request3(c, sports, match, categoryList, FullTime_1stHalf_etc, oddsnames, WHICH_ODD, ot_id):
    global dead_flag
    if(dead_flag):
        return
    global inplay
    try:
        offer_id = str(c["offer_id"])
        match_id = str(match['id'])
        LINK_API_ODDMOVEMENT = r"https://oddspedia.com/api/v1/getOddsMovements?ot="+str(ot_id)+"&matchId="+match_id + \
            r"&inplay=" + \
            str(inplay)+"&wettsteuer=0&geoCode=CH&geoState=&offerId=" + \
            offer_id+"&language=en"
    except Exception as e:
        print(str(e))
    try:
        response3 = requests.get(
            url=LINK_API_ODDMOVEMENT, proxies=proxies,  timeout=5)
    except Exception as e:
        if(str(e).find("An existing connection was forcibly closed by the remote host")):
            print("you scrape too fast, so the server has block you.")

    # with open(r"C:\Users\tiepl\Desktop\first_freelance\api3.json", "w")as f:
    #     f.writelines(str(response3.content))
    try:
        oddmovement = json.loads(response3.content)
    except Exception as e:
        # if(str(e).find("line 1 column 1") != -1):
        #     print("No data")
        return

    try:
        data = oddmovement["data"]['1']
    except:
        # print(LINK_API_ODDMOVEMENT)
        return

    try:
        int(match["winner"])
        status = "Finished"
    except:
        status = "Unfinished"

    if(inplay):
        ODD_TYPE = "LIVE"
    else:
        ODD_TYPE = "PRE"

    country = categoryList[str(match["category_id"])]["name"]

    for number in range(len(oddsnames)):
        data = oddmovement["data"][str(number+1)]
        home = data["moves"]
        for d in home:
            try:
                insert_to_database(WHICH_ODD, format_to_time_zone_of_Switzerland(match['md']), match['ht'], match['at'], country, match['league_round_name'], str(match["hscore"])+"-"+str(
                    match["ascore"]), status, sports[str(match["sport_id"])]['name'], ODD_TYPE, c["bookie_name"], str(oddsnames[number]), FullTime_1stHalf_etc, format_to_time_zone_of_Switzerland(d["t"]), d["y"])
            except:
                pass


def run(input_of_run, id_sport_name, SPORT_NAME):
    global dead_flag
    if(dead_flag):
        return
    global inplay, is_run_multithreading, bookmaker_list

    inplay = input_of_run
    perpage = 150
    max_match_per_page = 0
    # while(True):
    print(SPORT_NAME)
    if(dead_flag):
        return
    LINK_API = r"https://oddspedia.com/api/v1/getMatchList?excludeSpecialStatus=0&sortBy=default&perPageDefault="+str(perpage)+"&startDate="+start_date + \
        r"T00%3A00%3A00Z&endDate="+end_date + \
        r"T23%3A59%3A59Z&geoCode=CH&status=all&sport=" + \
    str(id_sport_name)+"&popularLeaguesOnly=0&page=1&perPage=" + \
    str(perpage)+"&language=en"

    response1 = requests.get(url=LINK_API, proxies=proxies,  timeout=5)
    with open(SPORT_NAME+'.txt', "w") as f:
        f.write(str(response1.content))

def get_csvFile():
    print("Writting to csv file!")
    csv_file = open("results.csv", "w", encoding='utf-8')
    csv_file.write("WHICH_ODD"+separate_char +
                   "DATE"+separate_char+"TEAM_HOME"+separate_char+"TEAM_AWAY"+separate_char+"COUNTRY"+separate_char+"COMPETITION"+separate_char+"SCORE"+separate_char+"STATUS"+separate_char+"SPORTNAME"+separate_char+"ODD_TYPE"+separate_char+"BOOKMAKER"+separate_char+"ODD_NAME"+separate_char+"FullTime_1stHalf_etc"+separate_char+"TIMESTAMP"+separate_char+"ODD\n")
    result_data = get_data_from_database()
    for i in result_data:
        row = ''
        for x in i:
            row += str(x) + separate_char
        row = row[:-1] + '\n'
        csv_file.write(row)
    csv_file.close()
    print("Successful!")


def delete_database():
    try:
        if(os.path.exists(DATABASE_PATH)):
            os.remove(DATABASE_PATH)
    except Exception as e:
        print(str(e))
        time.sleep(1)
        delete_database()


def create_database():
    cmd = '''CREATE TABLE results (
        which_odd            TEXT,
        data                 TEXT,
        team_home            TEXT,
        team_away            TEXT,
        country              TEXT,
        competition          TEXT,
        score                TEXT,
        status               TEXT,
        sportname            TEXT,
        odd_type             TEXT,
        bookmaker            TEXT,
        odd_name             TEXT,
        FullTime_1stHalf_etc TEXT,
        timestamp            TEXT,
        odd                  TEXT,
        PRIMARY KEY (
            which_odd,
            data,
            team_home,
            team_away,
            country,
            competition,
            score,
            status,
            sportname,
            odd_type,
            bookmaker,
            odd_name,
            FullTime_1stHalf_etc,
            timestamp,
            odd
        )
    );
    '''
    db = sqlite3.connect(DATABASE_PATH)
    c = db.cursor()
    c.execute('PRAGMA encoding="UTF-8";')
    c.execute(cmd)
    db.commit()


def main_process():
    global dead_flag
    delete_database()
    create_database()
    print("Running...")
    # 1 is liveOdds, 0 is preMatchOdds
    for id_name in all_sport_will_be_scraped:
        if(dead_flag):
            return
        run(1, int(id_name), all_sport_will_be_scraped[id_name])
        # run(0, int(id_name), all_sport_will_be_scraped[id_name])


def run_main_process():
    global thread_main, dead_flag
    timeout_for_mainprocess = 10 * 60 * 60
    thread_main = threading.Thread(target=main_process)
    thread_main.start()
    while(timeout_for_mainprocess > 0):
        if(dead_flag):
            return
        time.sleep(1)
        # print("still alive...")
        timeout_for_mainprocess -= 1
    dead_flag = True


def input_kill():
    global dead_flag
    while(not dead_flag):
        user_command = input(
            "Type: \n\t'kill' to kill this process. \n\t'getdata' to get output data. \n\t'getdatacount' to see how many records.\n----------------------> ")
        if(user_command == 'kill'):
            print("Killing...")
            dead_flag = True

        elif(user_command == 'getdata'):
            get_csvFile()

        elif(user_command == 'getdatacount'):
            print(get_records_count())


if __name__ == "__main__":
    global dead_flag
    while(1):
        dead_flag = False
        time_start_running = datetime.now()
        thread1 = threading.Thread(target=run_main_process, args=())
        thread1.start()
        time.sleep(3)
        thread2 = threading.Thread(target=input_kill, args=())
        thread2.start()

        while(1):
            time.sleep(1)
            if(not thread_main.is_alive()):
                thread1.join()
                thread2.join()
                break
        print("Loaded successful!")
        get_csvFile()
        delete_database()

        while((datetime.now() - time_start_running).seconds < TIME_WAIT_FOR_NEXT_LAUNCH):
            time_left = TIME_WAIT_FOR_NEXT_LAUNCH - (datetime.now() -
                  time_start_running).seconds
            sys.stdout.write('\r')
            # the exact output you're looking for:
            sys.stdout.write("%d  seconds remaining" % (time_left))
            sys.stdout.flush()
            time.sleep(1)
