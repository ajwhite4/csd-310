'''
Andrew White
28 April 2022
Module 9.3 Assignment
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

    cursor = db.cursor()
    cursor.execute("INSERT INTO player (first_name, last_name, team_id) VALUES('Smeagol', 'Shire Folk', 1)")

    print('-- DISPLAYING PLAYERS AFTER INSERT --')
    cursor = db.cursor()
    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id ORDER BY player_id")
    players = cursor.fetchall()
    
    for player in players:
        print('Player ID: {}\nFirst Name: {}\nLast Name: {}\nTeam Name: {}\n'.format(player[0],
            player[1], player[2], player[3]))

    cursor.execute("UPDATE player SET team_id = 2, first_name = 'Gollum', last_name = 'Ring Stealer' WHERE first_name = 'Smeagol'")

    print('-- DISPLAYING PLAYERS AFTER UPDATE --')
    cursor = db.cursor()
    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id ORDER BY player_id")
    players = cursor.fetchall()
    
    for player in players:
        print('Player ID: {}\nFirst Name: {}\nLast Name: {}\nTeam Name: {}\n'.format(player[0],
            player[1], player[2], player[3]))

    cursor.execute("DELETE FROM player WHERE first_name = 'Gollum'")

    print('-- DISPLAYING PLAYERS AFTER DELETE --')
    cursor = db.cursor()
    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id ORDER BY player_id")
    players = cursor.fetchall()
    
    for player in players:
        print('Player ID: {}\nFirst Name: {}\nLast Name: {}\nTeam Name: {}\n'.format(player[0],
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
