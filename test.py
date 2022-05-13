import sqlite3
import os
import time

DATABASE_PATH = "database.db"

def delete_database():
    try:
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

create_database()
# delete_database()