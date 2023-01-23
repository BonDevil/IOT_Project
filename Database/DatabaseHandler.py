from configparser import ConfigParser

import psycopg2


def config(filename="database.ini", section='postgresql'):
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


# it doesn't check if RFID already exists in database
def insert_player(rfid, name, wins, defeats):
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute an INSERT statement
        cur.execute("INSERT INTO Player (RFID, name, wins, defeats) VALUES (%s, %s, %s, %s)", (rfid, name, wins, defeats))

        # commit changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
