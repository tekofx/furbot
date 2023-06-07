import datetime
from dotenv import load_dotenv
import nextcord
from core import logger
import os
import mysql.connector

drop_tables = """DROP TABLE IF EXISTS users, roles, sentences, records, channels, posts;"""

users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id varchar(18),
                                    guild varchar(18) NOT NULL,
                                    name varchar(20) NOT NULL,
                                    joined_date datetime,
                                    birthday date,
                                    
                                    CONSTRAINT PK_users PRIMARY KEY (id, guild)
                                ); """
                                
                                
user_insert="""INSERT INTO users (id, guild, name, joined_date, birthday) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, joined_date=%s, birthday=%s;"""
user_remove="""DELETE FROM users WHERE id=%s AND guild=%s;"""
user_get="""SELECT * FROM users WHERE id=%s AND guild=%s;"""
user_exists="""SELECT * FROM users WHERE id=%s AND guild=%s;"""
users_get_with_joined_date_today="""SELECT * FROM users WHERE guild=%s AND joined_date LIKE %s;"""
users_get_from_guild="""SELECT * FROM users WHERE guild=%s;"""
user_set_birthday="""UPDATE users SET birthday=%s WHERE id=%s AND guild=%s;"""

roles_table = """ CREATE TABLE IF NOT EXISTS roles (
                                    id varchar(18),
                                    guild varchar(18) NOT NULL,
                                    name varchar(20) NOT NULL,
                                    type varchar(20),
                                    
                                    CONSTRAINT PK_roles PRIMARY KEY (id, guild)
                                );"""
                                
role_insert="""INSERT INTO roles (id, guild, name, type) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, type=%s;"""
role_remove="""DELETE FROM roles WHERE id=%s AND guild=%s;"""
role_get="""SELECT * FROM roles WHERE id=%s AND guild=%s;"""

records_table = """ CREATE TABLE IF NOT EXISTS records (
                                    id int(18) AUTO_INCREMENT,
                                    guild varchar(18) ,
                                    type varchar(20) NOT NULL,
                                    account varchar(20) NOT NULL,
                                    record varchar(20) NOT NULL,
                                    date datetime NOT NULL,
                                    
                                    CONSTRAINT PK_records PRIMARY KEY (id, guild)
                                ); """
                                
record_insert="""INSERT INTO records (id, guild, type, account, record, date) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE record=%s, date=%s;"""

record_remove="""DELETE FROM records WHERE id=%s AND guild=%s;"""
record_get="""SELECT * FROM records WHERE id=%s AND guild=%s;"""
records_get_of_type="""SELECT * FROM records WHERE guild=%s AND type=%s;"""
record_exists="""SELECT * FROM records WHERE id=%s AND guild=%s;"""


channels_table = """ CREATE TABLE IF NOT EXISTS channels (
                                    id varchar(18),
                                    guild varchar(18),
                                    type varchar(20),
                                    name varchar(20) NOT NULL,
                                    
                                    CONSTRAINT PK_channels PRIMARY KEY (id, guild)
                                ); """
                                
channel_insert="""INSERT INTO channels (id, guild, type, name) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s;"""
channel_remove="""DELETE FROM channels WHERE id=%s AND guild=%s;"""
channel_get="""SELECT * FROM channels WHERE id=%s AND guild=%s;"""
channels_get_from_guild="""SELECT * FROM channels WHERE guild=%s;"""
channel_set_type="""UPDATE channels SET type=%s WHERE id=%s AND guild=%s;"""
channel_exists="""SELECT * FROM channels WHERE id=%s AND guild=%s;"""
channel_get_of_type="""SELECT * FROM channels WHERE guild=%s AND type=%s;"""
channel_exists_of_type="""SELECT * FROM channels WHERE guild=%s AND type=%s;"""

posts_table = """ CREATE TABLE IF NOT EXISTS posts (
                                    id int(18) AUTO_INCREMENT,
                                    guild varchar(18) NOT NULL,
                                    channel varchar(18) NOT NULL,
                                    visibility ENUM('sfw','nsfw') NOT NULL, 
                                    service varchar(20) NOT NULL,
                                    account varchar(40) NOT NULL,
                                    frequency int(6) NOT NULL,
                                    
                                    CONSTRAINT PK_posts PRIMARY KEY (id, guild)
                                ); """
                                
post_insert="""INSERT INTO posts (guild, channel, visibility, service, account, frequency) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE visibility=%s, service=%s, account=%s, frequency=%s;"""
post_remove="""DELETE FROM posts WHERE id=%s AND guild=%s;"""                          
post_get="""SELECT * FROM posts WHERE id=%s AND guild=%s;"""
posts_get_from_guild="""SELECT * FROM posts WHERE guild=%s;"""


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
        
    def initialize(self):
        # Create tables
        self.execute_query(users_table)
        self.execute_query(roles_table)
        self.execute_query(records_table)
        self.execute_query(channels_table)
        self.execute_query(posts_table)
        log.info("Initialized database")

    def execute_query(self, query: str,data:list=None):
        if data:
            self.cursor.execute(query,data)
        else:
        
            self.cursor.execute(query)
        self.connection.commit()
        
    def fetch_query(self, query:str,data:list):
        self.cursor.execute(query,data)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
        
    def insert_user(self, user:nextcord.Member):
        self.execute_query(user_insert,(user.id,user.guild.id,user.name,user.joined_at,None,user.name,user.joined_at,None))
    
    def set_user_birthday(self, user:nextcord.Member, birthday:datetime.date):
        self.execute_query(user_set_birthday,(birthday,user.id,user.guild.id))
    
    def remove_user(self, user:nextcord.Member):
        self.execute_query(user_remove,(user.id,user.guild.id))
    
    def get_user(self, user:nextcord.Member):
        return self.fetch_query(user_get,(user.id,user.guild.id))
    
    def get_users(self, guild:nextcord.Guild):
        return self.fetch_query(users_get_from_guild,(guild.id,))
    def get_users_with_joined_day_today(self, guild:nextcord.Guild):
        return self.fetch_query(users_get_with_joined_date_today,(guild.id,))
    
    def exists_user(self, user:nextcord.Member):
        return self.fetch_query(user_exists,(user.id,user.guild.id))
    
    def insert_role(self, role:nextcord.Role):
        self.execute_query(role_insert,(role.id,role.guild.id,role.name,role.type,role.name,role.type))
        
    def remove_role(self, role:nextcord.Role):
        self.execute_query(role_remove,(role.id,role.guild.id))
        
    def get_role(self, role:nextcord.Role):
        return self.fetch_query(role_get,(role.id,role.guild.id))

    def insert_record(self, guild:nextcord.Guild, record_type:str, record:str,account:str=None):
        # TODO: Change list by record model
        """Inserts a record

        """        
        self.execute_query(record_insert,(record_type,account,record,guild.id,record_type,account,record,guild.id))
        
    def remove_record(self, record_id:int, guild:nextcord.Guild):
        self.execute_query(record_remove,(record_id,guild.id))
    
    def get_record(self, record_id:int, guild:nextcord.Guild):
        self.fetch_query(record_get,(record_id,guild.id))
        
    def get_records_of_type(self, guild_id:int, record_type:str):
        return self.fetch_query(records_get_of_type,(guild_id,record_type))
    
    def record_exists(self,  guild:nextcord.Guild,record_id:int):
        return self.fetch_query(record_exists,(record_id,guild.id))
        
    def clean_records(self, guild:nextcord.Guild,record_type,posts:list):
        """Removes records that are no longer fetched from twitter/reddit/api/etc

        Args:
            guild (nextcord.Guild): Guild to access its database
            record_type (str): type of record
            account (str): account of the record
            posts (list): list of posts
        """
        records=self.get_records_of_type(guild.id, record_type)
        for record in records:
            record_id=record[0]
            record_account=record[3]
            
            if record_id not in posts:
                self.remove_record(record_id,guild)
                log.debug(f"Removed {record_id} of account {record_account}")
        
    def insert_channel(self, channel:nextcord.TextChannel,type:str=None):
        self.execute_query(channel_insert,(channel.id,channel.guild.id,type,channel.name,channel.name))
    
    def remove_channel(self, channel:nextcord.TextChannel):
        self.execute_query(channel_remove,(channel.id,channel.guild.id))
    
    def get_channel(self, channel:nextcord.TextChannel ):
        var = self.fetch_query(channel_get,(channel.id,channel.guild.id))
        if len(var)==0:
            log.debug(f"Channel {channel.id} not found")
            return None
        return self.fetch_query(channel_get,(channel.id,channel.guild.id))[0]
    
    def get_channel_of_type(self,guild:nextcord.Guild, type:str):
        return self.fetch_query(channel_get_of_type,(guild.id,type))
   
    def update_channel_type(self, channel:nextcord.TextChannel,type:str):
        self.execute_query(channel_set_type,(type,channel.id,channel.guild.id))
    
    def exists_channel(self, channel:nextcord.TextChannel):
        return self.fetch_query(channel_exists,(channel.id,channel.guild.id))
    
    def exists_channel_of_type(self, guild:nextcord.Guild, type:str):
        return self.fetch_query(channel_exists_of_type,(guild.id,type))
    
    def insert_post(self, channel:nextcord.TextChannel, visibility:str, service:str, account:str, frequency:int):
        self.execute_query(post_insert,(channel.guild.id,channel.id,visibility,service,account,frequency,visibility,service,account,frequency))
    
    def remove_post(self, channel:nextcord.TextChannel,post_id:int):
        self.execute_query(post_remove,(post_id,channel.guild.id))
        
    def get_post(self, channel:nextcord.TextChannel,post_id:int):
        return self.fetch_query(post_get,(post_id,channel.guild.id))
    
    def get_posts(self, guild:nextcord.Guild):
        return self.fetch_query(posts_get_from_guild,(guild.id,))
    
    def get_channels(self, guild:nextcord.Guild):
        var=self.fetch_query(channels_get_from_guild,(guild.id,))
        log.info(var)
        return self.fetch_query(channels_get_from_guild,(guild.id,))
        
    
""" load_dotenv("./dev.env")
print(os.getenv("DB_USER"))
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
db.execute_query(post_insert,(1,1,"sfw","test","test",1,"sfw","test","test",1))
db.execute_query(channel_insert,(1,1,"test","test","test","test","test")) """