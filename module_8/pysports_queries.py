'''
Andrew White
18 April 2022
Module 8.3 Assignment
'''

from ast import Try
from msilib.schema import Error
from sqlite3 import connect
import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "pysports_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "pysports",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)

    print('-- DISPLAYING TEAM RECORDS --')

    cursor = db.cursor()
    cursor.execute("SELECT team_id, team_name, mascot FROM team")
    teams = cursor.fetchall()

    for team in teams:
        print('Team ID: {}\nTeam Name: {}\nMascot: {}\n'.format(team[0],
            team[1], team[2]))

    print('\n-- DISPLAYING PLAYER RECORDS --')
    
    cursor = db.cursor()
    cursor.execute("SELECT player_id, first_name, last_name, team_id FROM player")
    players = cursor.fetchall()

    for player in players:
        print('Player ID: {}\nFirst Name: {}\nLast Name: {}\nTeam ID: {}\n'.format(player[0],
            player[1], player[2], player[3]))

    input("\n\nPress any key to continue...")


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    db.close()
