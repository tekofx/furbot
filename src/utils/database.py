import datetime
import random
import sqlite3
import os
import logging
import nextcord
from utils.data import server_path


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

tables = [users_table, roles_table, sentences_table, records_table, channels_table]
log = logging.getLogger(__name__)


def create_connection(guild: nextcord.Guild) -> sqlite3.Connection:
    """Creates a connection with a db file

    Args:
        db_file (str): database to connect to

    Returns:
        sqlite3.Connection
    """
    databases_path = server_path.format(guild_name=guild.name, guild_id=guild.id)
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
    databases_path = server_path.format(guild_name=guild.name, guild_id=guild.id)

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
        database_connection.close()
    else:
        database_connection.commit()
        database_connection.close()


def remove_records_from_a_date(guild: nextcord.guild, date: datetime.date) -> None:
    """Removes all records from a date
    Args:
        guild (nextcord.Guild) : Guild to access its database
        date (str): date to remove records from
    """
    database_connection = create_connection(guild)

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


###################### Getters and setters ######################
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


def set_name(guild: nextcord.guild, user_id: int, name: str) -> None:
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


def get_birthday(guild: nextcord.guild, user_id: int) -> str:
    """Gets the birthday of a user

    Args:
        guild (nextcord.Guild) : Guild to access its database
        user_id (int): id of user

    Returns:
        str: birthday of user
    """
    database_connection = create_connection(guild)

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
        database_connection.close()
    else:
        database_connection.close()
        return birthday


def set_birthday(guild: nextcord.guild, user_id: int, date: str) -> None:
    """Sets the birthday of a user

    Args:
        guild (nextcord.Guild) : Guild to access its database
        user_id (int): id of user
        date (str): birthday of user
    """
    database_connection = create_connection(guild)

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
        database_connection.close()
    else:
        database_connection.commit()
        database_connection.close()


def get_birthdays(guild: nextcord.guild) -> list:
    """Gets birtdays of all users

    Args:
        guild (nextcord.Guild) : Guild to access its database

    Returns:
        list: containing other lists with [user_id, birtday]
    """

    database_connection = create_connection(guild)

    sql = """ SELECT id,birthday
        FROM users
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query birthdays: {}".format(error))
        database_connection.close()
    else:
        database_connection.close()
        return info


def get_ranks(guild: nextcord.guild) -> list:
    """Gets a list with all ranks

    Args:
        guild (nextcord.Guild) : Guild to access its database

    Returns:
        list: containing ids of all ranks
    """
    database_connection = create_connection(guild)

    sql = """ SELECT id
        FROM ranks
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query ranks: {}".format(error))
        database_connection.close()
    else:
        database_connection.close()
        output = []
        for x in info:
            output.append(x[0])

        return output


def get_species(guild: nextcord.guild) -> list:
    """Get a list with all species

    Args:
        guild (nextcord.Guild) : Guild to access its database

    Returns:
        list: containing ids of all species
    """
    database_connection = create_connection(guild)

    sql = """ SELECT id
        FROM species
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query species: {}".format(error))
        database_connection.close()
    else:
        database_connection.close()
        output = []
        for x in info:
            output.append(x[0])

        return output


def get_colors(guild: nextcord.guild) -> list:
    """Returns a list with all colors

    Args:
        guild (nextcord.Guild) : Guild to access its database

    Returns:
        list: containing ids of all colors
    """
    database_connection = create_connection(guild)

    sql = """ SELECT id
        FROM colors
        """
    cur = database_connection.cursor()
    try:
        cur.execute(sql)
        info = cur.fetchall()
    except Exception as error:
        log.error("Error: could not query colors: {}".format(error))
        database_connection.close()
    else:
        database_connection.close()
        output = []
        for x in info:
            output.append(x[0])

        return output


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
        database_connection.close()
        data = cursor.fetchall()
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
