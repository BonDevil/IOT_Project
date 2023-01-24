from configparser import ConfigParser

import sqlite3

from Player import Player
import os

def create_database():
    if os.path.exists("iot_database.db"):
        os.remove("iot_database.db")
        print("Old database removed.")
    connection = sqlite3.connect("iot_database.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE Player (
        RFID varchar(255),
        name varchar(255),
        wins int,
        defeats int,
        draws int,
        PRIMARY KEY(RFID),
        CHECK (wins >= 0),
        CHECK (defeats >= 0),
        CHECK (draws >= 0)
        );
"""
    )
    connection.commit()
    connection.close()
    print("New database created")

# def config(filename=r"Database.ini", section='postgresql'):
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read(filename)

#     # get section, default to postgresql
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception('Section {0} not found in the {1} file'.format(section, filename))

#     return db


def get_players_rfid():
    """Retrieve all Player's RFID from the database"""
    conn = None
    try:


        # connect to the PostgreSQL server
        conn = sqlite3.connect("iot_database.db")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute("SELECT RFID FROM Player")

        # retrieve results
        rfid_tuples = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()

        # convert the tuples to a list of strings
        rfid_list = [rfid[0] for rfid in rfid_tuples]

        return rfid_list
    except (Exception, sqlite3.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_player_by_rfid(rfid):
    """Retrieve all Player's RFID from the database"""
    conn = None
    try:


        # connect to the PostgreSQL server
        conn = sqlite3.connect("iot_database.db")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(f"SELECT * FROM Player WHERE RFID={rfid}")

        # retrieve results
        player = cur.fetchone()
        print(player)

        # close the communication with the PostgreSQL
        cur.close()

        return player
    except (Exception, sqlite3.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# it doesn't check if RFID already exists in database
def insert_player(rfid, name, wins=0, defeats=0, draws=0):
    conn = None
    try:

        # connect to the PostgreSQL server
        conn = sqlite3.connect("iot_database.db")

        # create a cursor
        cur = conn.cursor()

        # execute an INSERT statement
        cur.execute("INSERT INTO Player (RFID, name, wins, defeats, draws) VALUES (?,?,?,?,?)",
                    (rfid, name, wins, defeats, draws))

        # commit changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, sqlite3.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_all_players():
    """Retrieve all players from the database"""
    conn = None
    try:

        # connect to the PostgreSQL server
        conn = sqlite3.connect("iot_database.db")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute("SELECT RFID, name, wins, defeats FROM Player")

        # retrieve results
        players_tuples = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()

        # create a list of Player objects
        players = [Player(*player_tuple) for player_tuple in players_tuples]

        return players
    except (Exception, sqlite3.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# it doesn't check if RFID already exists in database
def add_win_to_player(rfid):
    """Add a win to a player in the Player table"""
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = sqlite3.connect("iot_database.db")

        # create a cursor
        cur = conn.cursor()

        # execute an update statement
        cur.execute("UPDATE Player SET wins = wins + 1 WHERE RFID = %s", (rfid,))

        # commit changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, sqlite3.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# it doesn't check if RFID already exists in database
def add_loose_to_player(rfid):
    """Add a loose to a player in the Player table"""
    conn = None
    try:

        # connect to the PostgreSQL server
        conn = sqlite3.connect("iot_database.db")

        # create a cursor
        cur = conn.cursor()

        # execute an update statement
        cur.execute("UPDATE Player SET defeats = defeats + 1 WHERE RFID = %s", (rfid,))

        # commit changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, sqlite3.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# it doesn't check if RFID already exists in database
def add_draw_to_players(rfid1, rfid2):
    """Add a loose to a player in the Player table"""
    conn = None
    try:

        # connect to the PostgreSQL server
        conn = sqlite3.connect("iot_database.db")

        # create a cursor
        cur = conn.cursor()

        # execute an update statement
        cur.execute("UPDATE Player SET draws = draws + 1 WHERE RFID = %s", (rfid1,))
        cur.execute("UPDATE Player SET draws = draws + 1 WHERE RFID = %s", (rfid2,))


        # commit changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, sqlite3.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == "__main__":
    create_database()