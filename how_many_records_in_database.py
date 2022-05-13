import sqlite3
from time import time

separate_char = ","
database_path = "database.db"


def get_data_from_database():
    cmd = '''select count(*)
             from results'''
    with sqlite3.connect(database_path) as conn:
        try:
            cur = conn.execute(cmd)
            conn.commit()
        except:
            return get_data_from_database()
        for i in cur:
            return i[0]
    time.sleep(0.5)
    return get_data_from_database()

if __name__ == "__main__":
    print(get_data_from_database())
