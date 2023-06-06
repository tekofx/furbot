from dotenv import load_dotenv
import logger
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
                                    guild int(18) NOT NULL,
                                    name varchar(20) NOT NULL,
                                    type varchar(20),
                                    
                                    CONSTRAINT PK_roles PRIMARY KEY (id, guild)
                                );"""
                                
role_insert="""INSERT INTO roles (id, guild, name, type) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, type=%s;"""



records_table = """ CREATE TABLE IF NOT EXISTS records (
                                    id int(18) AUTO_INCREMENT,
                                    guild int(18) ,
                                    type varchar(20) NOT NULL,
                                    account varchar(20) NOT NULL,
                                    record varchar(20) NOT NULL,
                                    date datetime NOT NULL,
                                    
                                    CONSTRAINT PK_records PRIMARY KEY (id, guild)
                                ); """
                                
record_insert="""INSERT INTO records (id, guild, type, account, record, date) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE record=%s, date=%s;"""

channels_table = """ CREATE TABLE IF NOT EXISTS channels (
                                    id int(18),
                                    guild int(18),
                                    type varchar(20) NOT NULL,
                                    policy varchar(20) NOT NULL,
                                    name varchar(20) NOT NULL,
                                    
                                    CONSTRAINT PK_channels PRIMARY KEY (id, guild)
                                ); """
                                
channel_insert="""INSERT INTO channels (id, guild, type, policy, name) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE policy=%s, name=%s;"""
posts_table = """ CREATE TABLE IF NOT EXISTS posts (
                                    id int(18) AUTO_INCREMENT,
                                    guild int(18) NOT NULL,
                                    channel int(18) NOT NULL,
                                    visibility ENUM('sfw','nsfw') NOT NULL, 
                                    service varchar(20) NOT NULL,
                                    account varchar(40) NOT NULL,
                                    frequency int(6) NOT NULL,
                                    
                                    CONSTRAINT PK_posts PRIMARY KEY (id, guild)
                                ); """
                                
post_insert="""INSERT INTO posts (id, guild, channel, visibility, service, account, frequency) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE visibility=%s, service=%s, account=%s, frequency=%s;"""
                                
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


load_dotenv("../../dev.env")
db=Database()
db.execute_query(drop_tables)

# Create tables
db.execute_query(users_table)
db.execute_query(roles_table)
db.execute_query(records_table)
db.execute_query(channels_table)
db.execute_query(posts_table)

# Insert data
db.execute_query(user_insert,(1,1,"test","2020-01-01","2020-01-01","test","2020-01-01","2020-01-01"))
db.execute_query(role_insert,(1,1,"test","test","test","test"))
db.execute_query(record_insert,(1,1,"test","test","test","2020-01-01","test","2020-01-01"))
db.execute_query(post_insert,(1,1,1,"sfw","test","test",1,"sfw","test","test",1))
db.execute_query(channel_insert,(1,1,"test","test","test","test","test"))