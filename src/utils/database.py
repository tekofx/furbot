import datetime
import random
import sqlite3
import os
import logging
from utils.data import databases_path


users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    joined_date date,
                                    birthday date
                                ); """


roles_table = """ CREATE TABLE IF NOT EXISTS roles (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL UNIQUE,
                                    type text NOT NULL
                                );"""

sentences_table = """ CREATE TABLE IF NOT EXISTS sentences (
                                    id integer PRIMARY KEY,
                                    type text NOT NULL ,
                                    sentence text NOT NULL, 
                                    UNIQUE (type, sentence)
                                ); """

records_table = """ CREATE TABLE IF NOT EXISTS records (
                                    id integer PRIMARY KEY,
                                    type text NOT NULL ,
                                    record text NOT NULL,
                                    date date NOT NULL
                                ); """

channels_table = """ CREATE TABLE IF NOT EXISTS channels (
                                    channel_id integer,
                                    type text NOT NULL ,
                                    name text NOT NULL,
                                    PRIMARY KEY(channel_id, type )
                                ); """

tables = [users_table, roles_table, sentences_table, records_table, channels_table]
log = logging.getLogger(__name__)


def create_connection(db_file: str) -> sqlite3.Connection:
    """Creates a connection with a db file

    Args:
        db_file (str): database to connect to

    Returns:
        sqlite3.Connection
    """
    database = databases_path + str(db_file) + ".db"

    database_connection = None
    try:
        database_connection = sqlite3.connect(database)
        return database_connection
    except Exception as e:
        log.error("Error: Could not connect to database . {}".format(e))


def create_table(
    database_connection: sqlite3.Connection, table_sql_sentence: str
) -> None:
    """Creates a table in the database
    Args:
        database_connection(sqlite3.Connection): Connection to database
        table_sql_sentence (str): sql sentence
    """
    database_name = table_sql_sentence.split()[5]

    try:
        c = database_connection.cursor()
        c.execute(table_sql_sentence)
        log.info("Created table {}".format(database_name))

    except Exception as e:
        log.error(
            "Error: Could not create table {}. Reason: {}".format(database_name, e)
        )


def setup_database(db_file: str) -> None:
    """Creates a db file and connects to it

    Args:
        db_file (str): db file to create
    """
    database = databases_path + db_file + ".db"

    # Create db files
    if not os.path.isfile(database):
        log.info("Database file {} not exists, creating it".format(database))
        f = open(database, "x")
        f.close()

    # create a database connection
    database_connection = create_connection(db_file)

    # create tables
    for table in tables:
        create_table(database_connection, table)


###################### Creates and removes ######################
def create_user(database_connection: sqlite3.Connection, user_data) -> None:
    """Creates a user in the users table
    Args:
        database_connection(sqlite3.Connection): Connection to database
        user (tuple): info to add. Containing: [user_id, user_name, user_joined_at]
    """

    sql = """ INSERT INTO users(id,name,joined_date)
              VALUES(?,?,?) """

    cur = database_connection.cursor()
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

    database_connection.commit()


def remove_user(database_connection: sqlite3.Connection, user_id: int) -> None:
    """Removes a user from database
    Args:
        database_connection(sqlite3.Connection): Connection to database
        user_id (int): id of user to remove
    """
    sql = "DELETE FROM users WHERE id=?"
    var = [user_id]
    cur = database_connection.cursor()
    try:
        cur.execute(sql, var)
        log.info("Deleted user {} from database".format(user_id))
    except Exception as error:
        log.error(
            "Error: Could not delete user {} from database: {}".format(user_id, error)
        )

    database_connection.commit()


def create_role(
    database_connection: sqlite3.Connection,
    role_id: int,
    name: str,
    role_type: str,
) -> None:
    """Creates a role in the roles table

    Args:
        database_connection(sqlite3.Connection): Connection to database
        role_id (int): id of role
        name (str): name of role
        role_type (str): type of role
    """

    sql = """ INSERT INTO roles(id,name, type)
              VALUES(?,?,?) """

    cur = database_connection.cursor()
    try:
        cur.execute(sql, [role_id, name, role_type])
        log.info(
            "Role {role} with id {id} was added to the database".format(
                role=name, id=role_id
            )
        )
    except Exception as error:
        log.error(
            "Error: Could not add role {id} {name}: {error}".format(
                id=role_id, name=name, error=error
            )
        )
        raise error

    database_connection.commit()


def remove_role(database_connection: sqlite3.Connection, role_id: int) -> None:
    """Removes a role entry

    Args:
        database_connection(sqlite3.Connection): Connection to database
        role_id (int): id of the role
    """
    sql = "DELETE FROM roles WHERE id=?"
    var = [role_id]
    cur = database_connection.cursor()
    try:
        cur.execute(sql, var)
        log.info("Deleted role {} from database".format(role_id))
    except Exception as error:
        log.error(
            "Error: Could not delete role {} from database: {}".format(role_id, error)
        )

    database_connection.commit()


def create_sentence(
    database_connection: sqlite3.Connection, sentence_data: list
) -> None:
    """Creates a sentence in the sentences table
    Args:
        database_connection(sqlite3.Connection): Connection to database
        sentence (list): info of sentence. Containing [type, sentence]
    """

    sql = """ INSERT INTO sentences(id,type,sentence)
              VALUES(?,?,?) """

    try:
        latest_id = get_latest_id(database_connection, "sentences") + 1
    except Exception as error:
        log.error("Error: {}".format(error))
        return
    sentence_data.insert(0, latest_id)

    cur = database_connection.cursor()
    try:
        cur.execute(sql, sentence_data)
        log.info(
            "sentence {sentence} with id {id} was added to the database".format(
                sentence=sentence_data[1], id=sentence_data[0]
            )
        )
    except Exception as error:
        log.error(
            "Error: Could not create sentence {id} {name}: {error}".format(
                id=sentence_data[0], name=sentence_data[1], error=error
            )
        )
        raise error

    database_connection.commit()


def create_record(database_connection: sqlite3.Connection, record_data: list) -> None:
    """Creates a record in the records table
    Args:
        database_connection(sqlite3.Connection): Connection to database
        record (list): info of record. Containing [type, record]
    """

    sql = """ INSERT INTO records(id,type,record,date)
              VALUES(?,?,?,?) """

    try:
        latest_id = get_latest_id(database_connection, "records") + 1
    except Exception as error:
        log.error("Error: {}".format(error))
        return
    record_data.insert(0, latest_id)
    record_data.append(datetime.date.today())

    cur = database_connection.cursor()
    try:
        cur.execute(sql, record_data)
        log.info(
            "record {record} with id {id} was added to the database".format(
                record=record_data[1], id=record_data[0]
            )
        )
    except Exception as error:
        log.error(
            "Error: Could not create record {id} {name}: {error}".format(
                id=record_data[0], name=record_data[1], error=error
            )
        )

    database_connection.commit()


def remove_records_from_a_date(
    database_connection: sqlite3.Connection, date: datetime.date
) -> None:
    """Removes all records from a date
    Args:
        database_connection(sqlite3.Connection): Connection to database
        date (str): date to remove records from
    """
    sql = "DELETE FROM records WHERE date=?"
    var = [date]
    cur = database_connection.cursor()
    try:
        cur.execute(sql, var)
        log.info("Deleted records from {} from database".format(date))
    except Exception as error:
        log.error(
            "Error: Could not delete records from {} from database: {}".format(
                date, error
            )
        )

    database_connection.commit()


def create_channel(database_connection: sqlite3.Connection, channel_data: list) -> None:
    """Creates a channel in the channels table
    Args:
        database_connection(sqlite3.Connection): Connection to database
        channel (list): info of channel. Containing [channel_id, type, channel]
    """

    sql = """ INSERT INTO channels(channel_id,type,name)
              VALUES(?,?,?) """

    cur = database_connection.cursor()
    try:
        cur.execute(sql, channel_data)
        log.info(
            "channel {channel} with id {id} was added to the database".format(
                channel=channel_data[1], id=channel_data[0]
            )
        )
    except Exception as error:
        log.error(
            "Error: Could not create channel {id} {name}: {error}".format(
                id=channel_data[0], name=channel_data[1], error=error
            )
        )

    database_connection.commit()


###################### Getters and setters ######################
def get_name(database_connection: sqlite3.Connection, user_id: int) -> str:
    """Gets the name of a user
    Args:
        database_connection(sqlite3.Connection): Connection to database
        user_id (int): id of user
    Returns:
        [str]: name of user
    """
    sql = """ SELECT name
        FROM users
        WHERE id=?
        """
    var = [user_id]
    cur = database_connection.cursor()
    try:
        cur.execute(sql, var)
    except Exception as error:
        log.error(
            "Error: could not query the name of user {}: {}".format(user_id, error)
        )
    info = cur.fetchone()
    name = info[0]

    return name


def set_name(database_connection: sqlite3.Connection, user_id: int, name: str) -> None:
    """Changes the name of a user
    Args:
        database_connection(sqlite3.Connection): Connection to database
        user_id (int): id of user
        name (str): new name for a user
    """
    sql = """ UPDATE users  
              SET name = ?
              WHERE id = ?"""

    cur = database_connection.cursor()
    var = [name, user_id]
    try:
        cur.execute(sql, var)
    except Exception as error:
        log.error("Error: Could not update name of user {}: {}".format(user_id, error))
    database_connection.commit()


def get_birthday(database_connection: sqlite3.Connection, user_id: int) -> str:
    """Gets the birthday of a user

    Args:
        database_connection(sqlite3.Connection): Connection to database
        user_id (int): id of user

    Returns:
        str: birthday of user
    """

    sql = """ SELECT birthday
        FROM users
        WHERE id=?
        """

    var = [user_id]
    cur = database_connection.cursor()
    try:
        cur.execute(sql, var)
        info = cur.fetchone()
        birthday = info[0]
    except Exception as error:
        log.error(
            "Error: could not query birthday of user {}. {}".format(user_id, error)
        )

    return birthday


def set_birthday(
    database_connection: sqlite3.Connection, user_id: int, date: str
) -> None:
    """Sets the birthday of a user

    Args:
        database_connection(sqlite3.Connection): Connection to database
        user_id (int): id of user
        date (str): birthday of user
    """
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
        cur = database_connection.cursor()
        cur.execute(sql, var)
    except Exception as error:
        log.error(
            "Error: Could not update birthday of user {}: {}".format(user_id, error)
        )
    database_connection.commit()


def get_birthdays(database_connection: sqlite3.Connection) -> list:
    """Gets birtdays of all users

    Args:
        database_connection(sqlite3.Connection): Connection to database

    Returns:
        list: containing other lists with [user_id, birtday]
    """
    sql = """ SELECT id,birthday
        FROM users
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query birthdays: {}".format(error))
    else:

        return info


def get_ranks(database_connection: sqlite3.Connection) -> list:
    """Gets a list with all ranks

    Args:
        database_connection (sqlite3.Connection): Connection to database

    Returns:
        list: containing ids of all ranks
    """
    sql = """ SELECT id
        FROM ranks
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query ranks: {}".format(error))
    output = []
    for x in info:
        output.append(x[0])

    return output


def get_species(database_connection: sqlite3.Connection) -> list:
    """Get a list with all species

    Args:
        database_connection (sqlite3.Connection): Connection to database

    Returns:
        list: containing ids of all species
    """
    sql = """ SELECT id
        FROM species
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query species: {}".format(error))
    output = []
    for x in info:
        output.append(x[0])

    return output


def get_colors(database_connection: sqlite3.Connection) -> list:
    """Returns a list with all colors

    Args:
        database_connection (sqlite3.Connection): Connection to database

    Returns:
        list: containing ids of all colors
    """
    sql = """ SELECT id
        FROM colors
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query colors: {}".format(error))
    output = []
    for x in info:
        output.append(x[0])

    return output


def get_random_sentence(
    database_connection: sqlite3.Connection, sentence_type: str
) -> str:
    """Gets a random sentence

    Args:
        database_connection (sqlite3.Connection): Connection to database
        type (str): type of sentence

    Returns:
        str: random sentence
    """
    sql = """ SELECT sentence
        FROM sentences
        WHERE type=?
        """
    cur = database_connection.cursor()
    sentence_type = [
        sentence_type,
    ]
    try:
        cur.execute(sql, sentence_type)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query sentences: {}".format(error))
    else:
        output = random.choice(info)
        return output[0]


def get_latest_id(database_connection: sqlite3.Connection, table: str) -> int | None:
    """Gets id of latest item in a table

    Args:
        database_connection (sqlite3.Connection): Connection to database
        table (str): table to look

    Returns:
        int: id of latest sentence
        None: if error occurs
    """
    sql = """ SELECT id FROM {} """.format(table)
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query sentences: {}".format(error))
        return
    else:
        if info == []:  # If theres no sentences
            return 0
        return info[-1][0]


def get_channel(database_connection: sqlite3.Connection, channel_type: str) -> int:
    """Gets id of saved channels

    Args:
        database_connection (sqlite3.Connection): Connection to database
        channel_type (str): type of channel. Can be general, memes, audit or lobby

    Returns:
        int: id of channel
    """
    sql = """ SELECT channel_id
        FROM channels
        WHERE type=?
        """
    var = [channel_type]
    cur = database_connection.cursor()
    try:
        cur.execute(sql, var)
    except Exception as error:
        log.error(
            "Error: could not query the channel of type {}: {}".format(
                channel_type, error
            )
        )
    info = cur.fetchone()
    if info is None:
        return 0

    return int(info[0])


################################## Checks ##########################################
def check_entry_in_database(
    database_connection: sqlite3.Connection, table: str, entry_id: int
) -> bool:
    """Check if entry exists in table

    Args:
        database_connection (sqlite3.Connection): Connection to database
        table (str): table to check
        entry_id (int): id of the entry

    Returns:
        bool: false if not exists, true on the contrary
    """
    cursor = database_connection.cursor()
    sql = "SELECT rowid FROM {} WHERE id = ?".format(table)
    var = [entry_id]
    try:
        cursor.execute(sql, var)
    except Exception as error:
        log.error(
            "Error: Could not check if user {} exists: {}".format(entry_id, error)
        )
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    return True


def check_record_in_database(database_connection, record: str) -> bool:
    """Check if entry exists in table

    Args:
        database_connection (sqlite3.Connection): Connection to database
        record (int): record of the entry

    Returns:
        bool: false if not exists, true on the contrary
    """
    cursor = database_connection.cursor()
    sql = """SELECT EXISTS(SELECT 1 FROM records WHERE record=?)"""
    try:
        cursor.execute(sql, (record,))
    except Exception as error:
        log.error(
            "Error: Could not check if record {} exists: {}".format(record, error)
        )

    data = cursor.fetchone()
    if data == (0,):
        return False
    return True
