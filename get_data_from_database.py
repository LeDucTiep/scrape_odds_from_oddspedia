import sqlite3

separate_char = ","
database_path = "database.db"


def get_data_from_database():
    results = []
    cmd = '''select which_odd,
        data,
        team_home,
        team_away,
        url,
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
    with sqlite3.connect(database_path) as conn:
        try:
            cur = conn.execute(cmd)
            conn.commit()
        except:
            return get_data_from_database()
        for i in cur:
            results.append(i)
    return results


def get_csvFile():
    csv_file = open("results.csv", "w", encoding='utf-8')
    csv_file.write("WHICH_ODD"+separate_char +
                   "DATE"+separate_char+"TEAM_HOME"+separate_char+"TEAM_AWAY"+separate_char+"URL"+separate_char+"COUNTRY"+separate_char+"COMPETITION"+separate_char+"SCORE"+separate_char+"STATUS"+separate_char+"SPORTNAME"+separate_char+"ODD_TYPE"+separate_char+"BOOKMAKER"+separate_char+"ODD_NAME"+separate_char+"FullTime_1stHalf_etc"+separate_char+"TIMESTAMP"+separate_char+"ODD\n")
    result_data = get_data_from_database()
    for i in result_data:
        row = ''
        for x in i:
            row += str(x) + separate_char
        row = row[:-1] + '\n'
        csv_file.write(row)
    csv_file.close()
    print("Successful!")


if __name__ == "__main__":
    get_csvFile()
