import datetime
import random
import sqlite3
import os
import logging
from typing import List
import nextcord
from utils.data import get_server_path


users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    joined_date date,
                                    points integer NOT NULL DEFAULT 0
                                ); """


roles_table = """ CREATE TABLE IF NOT EXISTS roles (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL UNIQUE,
                                    type text NOT NULL
                                );"""

sentences_table = """ CREATE TABLE IF NOT EXISTS sentences (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    type text NOT NULL ,
                                    sentence text NOT NULL, 
                                    UNIQUE (type, sentence)
                                ); """

records_table = """ CREATE TABLE IF NOT EXISTS records (
                                    id integer PRIMARY KEY AUTOINCREMENT,
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
posts_table = """ CREATE TABLE IF NOT EXISTS posts (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    channel_id integer NOT NULL,
                                    visibility text NOT NULL, 
                                    accounts text NOT NULL
                                ); """

tables = [
    users_table,
    roles_table,
    sentences_table,
    records_table,
    channels_table,
    posts_table,
]
log = logging.getLogger(__name__)


def create_connection(guild: nextcord.Guild) -> sqlite3.Connection:
    """Creates a connection with a db file

    Args:
        db_file (str): database to connect to

    Returns:
        sqlite3.Connection
    """
    databases_path = get_server_path(guild)
    database = databases_path + "database.db"

    database_connection = None
    try:
        database_connection = sqlite3.connect(database)
        return database_connection
    except Exception as e:
        log.error("Error: Could not connect to database . {}".format(e))


def create_table(guild: nextcord.Guild, table_sql_sentence: str) -> None:
    """Creates a table in the database
    Args:
        guild (nextcord.Guild) : Guild to access its database
        table_sql_sentence (str): sql sentence
    """
    database_name = table_sql_sentence.split()[5]
    database_connection = create_connection(guild)

    try:
        if not table_exists(guild, database_name):
            c = database_connection.cursor()
            c.execute(table_sql_sentence)
            log.info("Created table {}".format(database_name))

    except Exception as e:
        log.error(
            "Error: Could not create table {}. Reason: {}".format(database_name, e)
        )
        database_connection.close()
    else:
        database_connection.close()


def table_exists(guild: nextcord.Guild, table_name: str) -> bool:
    """Checks if a table exists in the database

    Args:
        guild (nextcord.Guild) : Guild to access its database
        table_name (str): name of the table

    Returns:
        bool
    """
    database_connection = create_connection(guild)

    sql = "SELECT * FROM sqlite_master WHERE type='table' AND name=?"
    var = [table_name]
    cur = database_connection.cursor()
    try:
        cur.execute(sql, var)
        table_exists = cur.fetchone()
        if table_exists:
            return True
        else:
            return False
    except Exception as error:
        log.error(
            "Error: Could not check if table {} exists in database: {}".format(
                table_name, error
            )
        )
        database_connection.close()
    else:
        database_connection.close()


def setup_database(guild: nextcord.Guild) -> None:
    """Creates a db file and connects to it

    Args:
        db_file (str): db file to create
    """
    databases_path = get_server_path(guild)

    database = databases_path + "database.db"

    # Create db files
    if not os.path.isfile(database):
        log.info("Database file {} not exists, creating it".format(database))
        f = open(database, "x")
        f.close()

    # create a database connection

    # create tables
    for table in tables:
        create_table(guild, table)


###################### Creates and removes ######################
def create_user(guild: nextcord.guild, user_data) -> None:
    """Creates a user in the users table
    Args:
        guild (nextcord.Guild) : Guild to access its database
        user (tuple): info to add. Containing: [user_id, user_name, user_joined_at]
    """
    database_connection = create_connection(guild)

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
        database_connection.close()
    else:

        database_connection.commit()
        database_connection.close()


def remove_user(guild: nextcord.guild, user_id: int) -> None:
    """Removes a user from database
    Args:
        guild (nextcord.Guild) : Guild to access its database
        user_id (int): id of user to remove
    """
    database_connection = create_connection(guild)

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
        database_connection.close()
    else:
        database_connection.commit()
        database_connection.close()


def create_role(
    guild: nextcord.guild,
    role_id: int,
    name: str,
    role_type: str,
) -> None:
    """Creates a role in the roles table

    Args:
        guild (nextcord.Guild) : Guild to access its database
        role_id (int): id of role
        name (str): name of role
        role_type (str): type of role
    """
    database_connection = create_connection(guild)

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
        database_connection.close()
        raise error
    else:
        database_connection.commit()
        database_connection.close()


def remove_role(guild: nextcord.guild, role_id: int) -> None:
    """Removes a role entry

    Args:
        guild (nextcord.Guild) : Guild to access its database
        role_id (int): id of the role
    """
    database_connection = create_connection(guild)

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
        database_connection.close()
    else:
        database_connection.commit()
        database_connection.close()


def create_sentence(guild: nextcord.guild, sentence_data: list) -> None:
    """Creates a sentence in the sentences table
    Args:
        guild (nextcord.Guild) : Guild to access its database
        sentence (list): info of sentence. Containing [type, sentence]
    """
    database_connection = create_connection(guild)

    sql = """ INSERT INTO sentences(type,sentence)
              VALUES(?,?) """

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
        database_connection.close()
        raise error
    else:
        database_connection.commit()
        database_connection.close()


def create_record(guild: nextcord.guild, record_data: list) -> None:
    """Creates a record in the records table
    Args:
        guild (nextcord.Guild) : Guild to access its database
        record (list): info of record. Containing [type, record]
    """
    database_connection = create_connection(guild)

    sql = """ INSERT INTO records(type,record,date)
              VALUES(?,?,?) """

    record_data.append(datetime.date.today())

    cur = database_connection.cursor()
    try:
        cur.execute(sql, record_data)
    except Exception as error:
        log.error(
            "Error: Could not create record {id} {name}: {error}".format(
                id=record_data[0], name=record_data[1], error=error
            )
        )
        database_connection.close()
    else:
        database_connection.commit()
        database_connection.close()


def remove_records_2_days(guild: nextcord.guild, record_types: list) -> None:
    """Removes all records older than a date
    Args:
        guild (nextcord.Guild) : Guild to access its database
        date (str): date to compare with
        record(list): record type to delete
    """
    date = datetime.datetime.now() - datetime.timedelta(days=2)
    database_connection = create_connection(guild)

    sql = "DELETE FROM records WHERE date<date('now', '-2 day') AND type IN {}".format(
        record_types
    )
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        log.info("Deleted records from {} from database".format(date))
    except Exception as error:
        log.error(
            "Error: Could not delete records from {} from database: {}".format(
                date, error
            )
        )
        database_connection.close()

    else:
        database_connection.commit()
        database_connection.close()


def create_channel(guild: nextcord.guild, channel_data: list) -> None:
    """Creates a channel in the channels table
    Args:
        guild (nextcord.Guild) : Guild to access its database
        channel (list): info of channel. Containing [channel_id, type, channel]
    """
    database_connection = create_connection(guild)

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
        database_connection.close()
    else:
        database_connection.commit()
        database_connection.close()


def create_post(guild: nextcord.guild, post_data: list) -> None:
    """Creates a post in the posts table
    Args:
        guild (nextcord.Guild) : Guild to access its database
        post_data (list): info of post. Containing [channel_id, visibility(SFW/NSFW), account]
    """
    database_connection = create_connection(guild)

    sql = """ INSERT INTO posts(channel_id,visibility,accounts)
              VALUES(?,?,?) """

    cur = database_connection.cursor()
    try:
        cur.execute(sql, post_data)
        log.info(
            "Post {} {} was added to the database".format(post_data[1], post_data[0])
        )
    except Exception as error:
        log.error(
            "Error: Could not create post {} {}: {}".format(
                post_data[0], post_data[1], error
            )
        )
        database_connection.close()
    else:
        database_connection.commit()
        database_connection.close()


def remove_post(guild: nextcord.guild, id: int) -> None:

    database_connection = create_connection(guild)

    sql = "DELETE FROM posts WHERE id=?"
    cur = database_connection.cursor()
    try:
        cur.execute(sql, [id])
        log.info("Deleted post {} from database".format(id))
    except Exception as error:
        log.error("Error: Could not delete post {} from database: {}".format(id, error))
        database_connection.close()

    else:
        database_connection.commit()
        database_connection.close()


###################### Getters and setters ######################


def get_posts(guild: nextcord.guild) -> list:
    """Gets the posts for a server

    Args:
        guild (nextcord.guild): guild to get the posts for

    Returns:
        list: containing [(channel_id, visibility,account, id), (channel_id, visibility,account, id), ...]
    """
    database_connection = create_connection(guild)

    sql = "SELECT channel_id, visibility, accounts, id FROM posts "
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
    except Exception as error:
        log.error("Error: could not query posts {}: {}".format(error))
        database_connection.close()
    else:
        info = cur.fetchall()
        return info


def get_roles_by_type(guild: nextcord.guild, role_type: str):
    database_connection = create_connection(guild)

    sql = """ SELECT id
        FROM roles
        WHERE type=?
        """
    var = [role_type]
    cur = database_connection.cursor()
    try:
        cur.execute(sql, var)
    except Exception as error:
        log.error(
            "Error: could not query roles of type {}: {}".format(role_type, error)
        )
        database_connection.close()
    else:
        info = cur.fetchall()
        return info


def get_name(guild: nextcord.guild, user_id: int) -> str:
    """Gets the name of a user
    Args:
        guild (nextcord.Guild) : Guild to access its database
        user_id (int): id of user
    Returns:
        [str]: name of user
    """
    database_connection = create_connection(guild)

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
        database_connection.close()
    else:
        info = cur.fetchone()
        name = info[0]
        database_connection.close()
        return name


def get_joined_dates(guild: nextcord.Guild) -> list:
    """Gets all the joined dates of the users in the database

    Args:
        guild (nextcord.Guild): guild of the database

    Returns:
        list: containing [user_id, joined_date]
    """
    database_connection = create_connection(guild)

    sql = """ SELECT id,joined_date
        FROM users
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
    except Exception as error:
        log.error(
            "Error: could not query the joined_dates of guild {}: {}".format(
                guild, error
            )
        )
        database_connection.close()
    else:
        info = cur.fetchall()
        output = []

        for x in info:
            var = []
            var.append(x[0])
            var.append(x[1].split(" ")[0])
            output.append(var)
        database_connection.close()
        return output


def sort_by_points(guild: nextcord.Guild) -> list:
    """Sorts the users by their points

    Args:
        guild (nextcord.Guild): guild of the database

    Returns:
        list: containing [user_id, points]
    """
    database_connection = create_connection(guild)

    sql = """ SELECT id,points
        FROM users
        ORDER BY points DESC
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
    except Exception as error:
        log.error(
            "Error: could not query the points of guild {}: {}".format(guild, error)
        )
        database_connection.close()
    else:
        info = cur.fetchall()
        output = []

        for x in info:
            var = []
            var.append(x[0])
            var.append(x[1])
            output.append(var)
        database_connection.close()
        return output


def increase_points(guild: nextcord.Guild, user_id: int, points: int):
    """Increases the points of a user

    Args:
        guild (nextcord.Guild): guild of the database
        user_id (int): id of the user
        points (int): amount of points to increase
    """
    database_connection = create_connection(guild)

    sql = """ UPDATE users
        SET points=points + ?
        WHERE id=?
        """
    var = [points, user_id]
    cur = database_connection.cursor()
    try:
        cur.execute(sql, var)
    except Exception as error:
        log.error(
            "Error: could not update the points of user {}: {}".format(user_id, error)
        )
        database_connection.close()
    else:
        database_connection.commit()
        database_connection.close()


def set_name(guild: nextcord.Guild, user_id: int, name: str) -> None:
    """Changes the name of a user
    Args:
        guild (nextcord.Guild) : Guild to access its database
        user_id (int): id of user
        name (str): new name for a user
    """
    database_connection = create_connection(guild)

    sql = """ UPDATE users  
              SET name = ?
              WHERE id = ?"""

    cur = database_connection.cursor()
    var = [name, user_id]
    try:
        cur.execute(sql, var)
    except Exception as error:
        log.error("Error: Could not update name of user {}: {}".format(user_id, error))
        database_connection.close()
    else:
        database_connection.commit()
        database_connection.close()


def get_random_sentence(guild: nextcord.guild, sentence_type: str) -> str:
    """Gets a random sentence

    Args:
        guild (nextcord.Guild) : Guild to access its database
        type (str): type of sentence

    Returns:
        str: random sentence
    """
    database_connection = create_connection(guild)

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
        database_connection.close()
    else:
        database_connection.close()
        output = random.choice(info)
        return output[0]


def get_channel(guild: nextcord.guild, channel_type: str) -> int:
    """Gets id of saved channels

    Args:
        guild (nextcord.Guild) : Guild to access its database
        channel_type (str): type of channel. Can be general, memes, audit or lobby

    Returns:
        int: id of channel
    """
    database_connection = create_connection(guild)

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
        database_connection.close()

    else:
        info = cur.fetchone()
        database_connection.close()
        if info is None:
            return 0

        return int(info[0])


################################## Checks ##########################################
def check_entry_in_database(guild: nextcord.guild, table: str, entry_id: int) -> bool:
    """Check if entry exists in table

    Args:
        guild (nextcord.Guild) : Guild to access its database
        table (str): table to check
        entry_id (int): id of the entry

    Returns:
        bool: false if not exists, true on the contrary
    """
    database_connection = create_connection(guild)

    cursor = database_connection.cursor()
    sql = "SELECT rowid FROM {} WHERE id = ?".format(table)
    var = [entry_id]
    try:
        cursor.execute(sql, var)
    except Exception as error:
        log.error(
            "Error: Could not check if user {} exists: {}".format(entry_id, error)
        )
        database_connection.close()
    else:
        data = cursor.fetchall()
        database_connection.close()
        if len(data) == 0:
            return False
        return True


def check_record_in_database(guild: nextcord.Guild, record: str) -> bool:
    """Check if entry exists in table

    Args:
        guild (nextcord.Guild) : Guild to access its database
        record (int): record of the entry

    Returns:
        bool: false if not exists, true on the contrary
    """
    database_connection = create_connection(guild)

    cursor = database_connection.cursor()
    sql = """SELECT EXISTS(SELECT 1 FROM records WHERE record=?)"""
    try:
        cursor.execute(sql, (record,))
    except Exception as error:
        log.error(
            "Error: Could not check if record {} exists: {}".format(record, error)
        )
        database_connection.close()
    else:
        data = cursor.fetchone()
        database_connection.close()

        if data == (0,):
            return False
        return True


def table_empty(guild: nextcord.guild, table: str) -> bool:
    database_connection = create_connection(guild)
    sql = "SELECT count(*) FROM {}".format(table)
    cursor = database_connection.cursor()

    try:
        cursor.execute(sql)
    except Exception as error:
        log.error(
            "Error: Could not check if table {} is empty: {}".format(table, error)
        )
        database_connection.close()
    else:
        data = cursor.fetchone()
        database_connection.close()
        if data[0] == 0:
            return True
        return False


def exists_channel(guild: nextcord.Guild, channel_type: str) -> bool:
    """Check if channel exists

    Args:
        guild (nextcord.Guild) : Guild to access its database
        channel_type (str): type of channel. Can be general, memes, audit or lobby

    Returns:
        bool: false if not exists, true on the contrary
    """
    database_connection = create_connection(guild)

    cursor = database_connection.cursor()
    sql = "SELECT EXISTS(SELECT 1 FROM channels WHERE type=?)"
    var = [channel_type]
    try:
        cursor.execute(sql, var)
    except Exception as error:
        log.error(
            "Error: Could not check if channel {} exists: {}".format(
                channel_type, error
            )
        )
        database_connection.close()
    else:
        data = cursor.fetchone()
        database_connection.close()

        if data == (0,):
            return False
        return True
