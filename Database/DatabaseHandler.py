from configparser import ConfigParser

import psycopg2

from Player import Player


def config(filename=r"C:\Users\Piotr\PycharmProjects\IOT_Project\Database\Database.ini", section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def get_players_rfid():
    """Retrieve all Player's RFID from the database"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_player_by_rfid(rfid):
    """Retrieve all Player's RFID from the database"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# it doesn't check if RFID already exists in database
def insert_player(rfid, name, wins=0, defeats=0, draws=0):
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute an INSERT statement
        cur.execute("INSERT INTO Player (RFID, name, wins, defeats, draws) VALUES (%s, %s, %s, %s, %s)",
                    (rfid, name, wins, defeats, draws))

        # commit changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_all_players():
    """Retrieve all players from the database"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# it doesn't check if RFID already exists in database
def add_win_to_player(rfid):
    """Add a win to a player in the Player table"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute an update statement
        cur.execute("UPDATE Player SET wins = wins + 1 WHERE RFID = %s", (rfid,))

        # commit changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
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
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute an update statement
        cur.execute("UPDATE Player SET defeats = defeats + 1 WHERE RFID = %s", (rfid,))

        # commit changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
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
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute an update statement
        cur.execute("UPDATE Player SET draws = draws + 1 WHERE RFID = %s", (rfid1,))
        cur.execute("UPDATE Player SET draws = draws + 1 WHERE RFID = %s", (rfid2,))


        # commit changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
