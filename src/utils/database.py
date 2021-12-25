import datetime
import sqlite3
import os
import logging

database_path = "databases/"
users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    joined_date date,
                                    birthday date
                                ); """

ranks_table = """ CREATE TABLE IF NOT EXISTS ranks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL
                                ); """

species_table = """ CREATE TABLE IF NOT EXISTS species (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL
                                ); """

colors_table = """ CREATE TABLE IF NOT EXISTS colors (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL
                                ); """


tables = [users_table, ranks_table, species_table, colors_table]
log = logging.getLogger(__name__)


def create_connection(db_file: str):
    """Creates a connection to a database db_file
    Args:
        db_file (str): database file to connect
    Returns:
        sqlite3.Connection: connection to database
    """
    database = database_path + str(db_file) + ".db"

    conn = None
    try:
        conn = sqlite3.connect(database)
        log.info("Connection with database {} successful".format(database))
        return conn
    except Exception as e:
        log.error("Error: Could not connect to database . {}".format(e))

    return conn


def create_table(conn, table_sql_sentence: str):
    """Creates a table in the database
    Args:
        conn (sqlite3.Connection): Connection to database
        table_sql_sentence (str): sql sentence
    """
    database_name = table_sql_sentence.split()[5]

    try:
        c = conn.cursor()
        c.execute(table_sql_sentence)
        log.info("Created table {}".format(database_name))

    except Exception as e:
        log.error(
            "Error: Could not create table {}. Reason: {}".format(database_name, e)
        )


def setup_database(db_file: str):
    """Creates the db file and stablish connection to it
    Returns:
        sqlite3.Connection: connection to database
    """
    database = database_path + db_file + ".db"

    # Create db files
    if not os.path.isfile(database):
        log.info("Database file {} not exists, creating it".format(database))
        f = open(database, "x")
        f.close()

    # create a database connection
    conn = create_connection(db_file)

    # create tables
    for table in tables:
        create_table(conn, table)

    return conn


###################### Creates and removes ######################
def create_user(conn, user_data):
    """Creates a user in the users table
    Args:
        conn (sqlite3.Connection): Connection to database
        user (tuple): info to add
    """

    sql = """ INSERT INTO users(id,name,joined_date)
              VALUES(?,?,?) """

    cur = conn.cursor()
    try:
        cur.execute(sql, user_data)
        log.info(
            "User {user} with id {id} was added to the database".format(
                user=user_data[1], id=user_data[0]
            )
        )
    except Exception as error:
        log.error(
            "Error: Could not create user {id} {name}: {error}".format(
                id=user_data[0], name=user_data[1], error=error
            )
        )

    conn.commit()


def remove_user(con, user_id: int):
    """Removes a user from database
    Args:
        conn (sqlite3.Connection): Connection to database
        user_id (int): id of user to remove
    """
    sql = "DELETE FROM users WHERE id=?"
    var = [user_id]
    cur = con.cursor()
    try:
        cur.execute(sql, var)
        log.info("Deleted user {} from database".format(user_id))
    except:
        log.error("Error: Could not delete user {id} from database".format(user_id))

    con.commit()


def create_rank(conn, rank_data):
    """Creates a rank in the ranks table
    Args:
        conn (sqlite3.Connection): Connection to database
        rank_data (tuple): info to add
    """

    sql = """ INSERT INTO ranks(id,name)
              VALUES(?,?) """

    cur = conn.cursor()
    try:
        cur.execute(sql, rank_data)
        log.info(
            "Rank {rank} with id {id} was added to the database".format(
                rank=rank_data[1], id=rank_data[0]
            )
        )
    except:
        log.error(
            "Error: Could not add rank {id} {name}".format(
                id=rank_data[0], name=rank_data[1]
            )
        )

    conn.commit()


def remove_rank(con, rank_id: int):
    """Removes a rank entry

    Args:
        con ([type]): [description]
        rank_id (int): [id of the rank
    """
    sql = "DELETE FROM ranks WHERE id=?"
    var = [rank_id]
    cur = con.cursor()
    try:
        cur.execute(sql, var)
        log.info("Deleted rank {} from database".format(rank_id))
    except:
        log.error("Error: Could not delete rank {id} from database".format(rank_id))

    con.commit()


def create_specie(conn, specie_data):
    """Creates a specie in the species table
    Args:
        conn (sqlite3.Connection): Connection to database
        user (tuple): info to add
    """

    sql = """ INSERT INTO species(id,name)
              VALUES(?,?) """

    cur = conn.cursor()
    try:
        cur.execute(sql, specie_data)
        log.info(
            "Specie {specie} with id {id} was added to the database".format(
                specie=specie_data[1], id=specie_data[0]
            )
        )
    except:
        log.error(
            "Error: Could not add specie {id} {name}".format(
                id=specie_data[0], name=specie_data[1]
            )
        )

    conn.commit()


def remove_specie(con, specie_id: int):
    """Removes a specie entry

    Args:
        con ([type]): [description]
        specie_id (int): [id of the specie
    """
    sql = "DELETE FROM species WHERE id=?"
    var = [specie_id]
    cur = con.cursor()
    try:
        cur.execute(sql, var)
        log.info("Deleted specie {} from database".format(specie_id))
    except:
        log.error("Error: Could not delete specie {id} from database".format(specie_id))

    con.commit()


def create_color(conn, color_data):
    """Creates a color in the colors table
    Args:
        conn (sqlite3.Connection): Connection to database
        user (tuple): info to add
    """

    sql = """ INSERT INTO colors(id,name)
              VALUES(?,?) """

    cur = conn.cursor()
    try:
        cur.execute(sql, color_data)
        log.info(
            "color {color} with id {id} was added to the database".format(
                color=color_data[1], id=color_data[0]
            )
        )
    except:
        log.error(
            "Error: Could not add color {id} {name}".format(
                id=color_data[0], name=color_data[1]
            )
        )

    conn.commit()


def remove_color(con, color_id: int):
    """Removes a color entry

    Args:
        con ([type]): [description]
        color_id (int): [id of the color
    """
    sql = "DELETE FROM colors WHERE id=?"
    var = [color_id]
    cur = con.cursor()
    try:
        cur.execute(sql, var)
        log.info("Deleted color {} from database".format(color_id))
    except:
        log.error("Error: Could not delete color {id} from database".format(color_id))

    con.commit()


###################### Getters and setters ######################
def get_name(con, user_id: int):
    """Gets the name of a user
    Args:
        con ([type]): [description]
        user_id (int): id of user
    Returns:
        [str]: name of user
    """
    sql = """ SELECT name
        FROM users
        WHERE id=?
        """
    var = [user_id]
    cur = con.cursor()
    try:
        cur.execute(sql, var)
        log.info("Query of name for user {id} successful".format(id=user_id))
    except:
        log.error("Error: could not query the name of user {}".format(user_id))
    info = cur.fetchone()
    num_messages = int(info[0])

    return num_messages


def set_name(con, user_id: int, name: str):
    """Changes the name of a user
    Args:
        conn (sqlite3.Connection): Connection to database
        user_id (int): id of user
        name (str): new name for a user
    """
    sql = """ UPDATE users  
              SET name = ?
              WHERE id = ?"""

    cur = con.cursor()
    var = [name, user_id]
    try:
        cur.execute(sql, var)
        log.info("Updated name of user {}".format(user_id))
    except:
        log.error("Error: Could not update name of user {}".format(user_id))
    con.commit()


def get_birthday(con, user_id: int):
    sql = """ SELECT birthday
        FROM users
        WHERE id=?
        """

    var = [user_id]
    cur = con.cursor()
    try:
        cur.execute(sql, var)
        info = cur.fetchone()
        birthday = info[0]
    except Exception as error:
        log.error(
            "Error: could not query birthday of user {}. {}".format(user_id, error)
        )

    return birthday


def set_birthday(con, user_id: int, date: int):
    sql = """ UPDATE users  
              SET birthday = ?
              WHERE id = ?"""

    date = date.split("-")
    day = int(date[0])
    month = int(date[1])
    birthday = datetime.date(
        2000,
        month,
        day,
    )

    var = [birthday, user_id]
    try:
        cur = con.cursor()
        cur.execute(sql, var)
        log.info("Updated birthday of user {}".format(user_id))
    except:
        log.error("Error: Could not update birthday of user {}".format(user_id))
    con.commit()


def get_birthdays(con):
    sql = """ SELECT id,birthday
        FROM users
        """
    cur = con.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query birthdays: {}".format(error))
    else:

        return info


def get_ranks(con):
    sql = """ SELECT id
        FROM ranks
        """
    cur = con.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query ranks: {}".format(error))
    output = []
    for x in info:
        output.append(x[0])

    return output


def get_species(con):
    sql = """ SELECT id
        FROM species
        """
    cur = con.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query species: {}".format(error))
    output = []
    for x in info:
        output.append(x[0])

    return output


def get_colors(con):
    sql = """ SELECT id
        FROM colors
        """
    cur = con.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query colors: {}".format(error))
    output = []
    for x in info:
        output.append(x[0])

    return output


################################## Checks ##########################################
def check_entry_in_database(con, table: str, entry_id: int):
    """Check if entry exists in table

    Args:
        con ([type]): [description]
        table (str): table to check
        entry_id (int): id of the entry

    Returns:
        bool: false if not exists, true on the contrary
    """
    cursor = con.cursor()
    sql = "SELECT rowid FROM {} WHERE id = ?".format(table)
    var = [entry_id]
    try:
        cursor.execute(sql, var)
    except:
        log.error("Error: Could not check if user {id} exists".format(id=entry_id))
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    return True
