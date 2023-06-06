from dotenv import load_dotenv
from core import logger
import os
import mysql.connector


users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id int(18),
                                    guild int(18) NOT NULL,
                                    name varchar(20) NOT NULL,
                                    joined_date datetime,
                                    birthday date,
                                    
                                    CONSTRAINT PK_users PRIMARY KEY (id, guild)
                                ); """
                                
                                
user_insert="""INSERT INTO users (id, guild, name, joined_date, birthday) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, joined_date=%s, birthday=%s;"""
drop_tables = """DROP TABLE IF EXISTS users, roles, sentences, records, channels, posts;"""

roles_table = """ CREATE TABLE IF NOT EXISTS roles (
                                    id int(18),
                                    guild int(18) integer NOT NULL,
                                    name varchar(20) NOT NULL ,
                                    type text varchar(20)
                                    
                                    CONSTRAINT PK_roles PRIMARY KEY (id, guild)
                                );"""
                                
role_insert="""INSERT INTO roles (id, guild, name, type) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, type=%s;"""



records_table = """ CREATE TABLE IF NOT EXISTS records (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    guild_id integer NOT NULL,
                                    type text NOT NULL ,
                                    account text,
                                    record text NOT NULL,
                                    date date NOT NULL
                                ); """

channels_table = """ CREATE TABLE IF NOT EXISTS channels (
                                    id integer NOT NULL PRIMARY KEY,
                                    guild_id integer NOT NULL,
                                    type text,
                                    policy text NOT NULL,
                                    name text NOT NULL
                                ); """
posts_table = """ CREATE TABLE IF NOT EXISTS posts (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    guild_id integer NOT NULL,
                                    channel_id integer NOT NULL,
                                    visibility text NOT NULL, 
                                    service text NOT NULL,
                                    account text NOT NULL, 
                                    interval integer NOT NULL
                                ); """
                                
tables = [
    users_table,
    roles_table,
    records_table,
    channels_table,
    posts_table,
]
log = logger.getLogger(__name__)



        


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="db"
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str,data:str=None):
        if data:
            self.cursor.execute(query,data)
        else:
        
            self.cursor.execute(query)
        self.connection.commit()

    def fetch_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


load_dotenv("../dev.env")
db=Database()
db.execute_query(drop_tables)
db.execute_query(users_table)
db.execute_query(user_insert,(1,1,"test","2020-01-01","2020-01-01","test","2020-01-01","2020-01-01"))