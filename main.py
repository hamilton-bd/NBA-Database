import csv
import MySQLdb


def get_key(filename="key.txt"):
    with open(filename, 'r') as file:
        fl = file.readline().strip()
        return fl


def populate_db():
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd=get_key(),
                           db='NBA_DATA')
    c = conn.cursor()

    player_insert = 'INSERT INTO Player(PlayerName, Year, Age, YearsExp, ' \
                    'Height, Weight, Salary, StatsID, TeamID) VALUES (%s, ' \
                    '%s, %s, %s, %s, %s, %s, %s, %s);'

    stats_insert = 'INSERT INTO Stats(Games, Minutes, PER, TruePer, ThreePer,'\
                   ' FTPer, ORB, DRB, TRB, AST, STL, BLK, TOV, USG, OWS, DWS,'\
                   ' WS, OBPM, DBPM, BPM, VORP, ShotPer) VALUES (%s, %s, %s,'\
                   ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'\
                   ' %s, %s, %s, %s, %s);'

    team_insert = 'INSERT INTO Team (TeamName) Values(%s);'

    with open('stats.csv', encoding='utf8', errors='ignore') as mfile:
        csvreader = csv.DictReader(mfile)
        for row in csvreader:
            print(row)
            c.execute(stats_insert, [row['Games'], row['MinutesPlayed'],
                                     row['PER'], row['TS%'], row['3P%'],
                                     row['FT%'], row['ORB'], row['DRB'],
                                     row['TRB'], row['AST%'], row['STL%'],
                                     row['BLK%'], row['TOV%'], row['USG%'],
                                     row['OWS'], row['DWS'], row['WS'],
                                     row['OBPM'], row['DBPM'], row['BPM'],
                                     row['VORP'], row['Shot%']])
            stats_id = c.lastrowid

            try:
                c.execute(team_insert, [row['Team']])
                team_id = c.lastrowid
            except MySQLdb.IntegrityError:
                c.execute('SELECT TeamID FROM Team WHERE TeamName=%s;',
                          [row['Team']])
                team_id = c.fetchone()[0]
            try:
                c.execute(player_insert,
                          [row['Player'], row['Year'], row['Age'],
                           row['Yrs Experience'], row['Height'], row['Weight'],
                           row['TrueSalary'], stats_id, team_id])

            except MySQLdb.IntegrityError:
                pass

        conn.commit()
        conn.close()


def main():
    prompt = input("Populate NBA_DATA? (y/n)")
    if prompt == "y":
            populate_db()
    else:
        print("NBA_DATA not populated")


if __name__ == '__main__':
    main()
