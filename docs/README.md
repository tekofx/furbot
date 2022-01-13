# Python Documentation

## Classes

**[animal](animal.md)**: 

**[memes](memes.md)**: 

**[fun](fun.md)**: 

**[administration](administration.md)**: 

**[utilities](utilities.md)**: 

**[tasks](tasks.md)**: 

**[roast](roast.md)**: 

**[stickers](stickers.md)**: 

**[Twitter](Twitter.md)**: 

**[Bot](Bot.md)**: 

**[Reddit](Reddit.md)**: 

**[Data](Data.md)**: 


## Functions

### setup



#### Parameters
name | description | default
--- | --- | ---
bot |  | 





### create_meme


Crea un meme   
Args: pictures (list): lista de imagenes, siendo pictures[0] el meme y el resto avatares avatar_url (str): url del avatar a añadir al meme avatar_size (int): tamañao al que convertir el avatar de webp a png position (list): posiciones en las que colocar las imagenes, siendo position[0] y position[1] la x,y del meme invert (bool): Si es True usa el meme como canvas, en caso contrario, usa el avatar 
#### Parameters
name | description | default
--- | --- | ---
pictures |  | 
avatar_url |  | 
avatar_size |  | 
position |  | 
invert |  | 





### setup



#### Parameters
name | description | default
--- | --- | ---
bot |  | 





### setup



#### Parameters
name | description | default
--- | --- | ---
bot |  | 





### setup



#### Parameters
name | description | default
--- | --- | ---
bot |  | 





### setup



#### Parameters
name | description | default
--- | --- | ---
bot |  | 





### get_user_species


Get user roles that are species   
Args: user (nextcord.Member): user to search for roles   
Returns: str: String containing roles 
#### Parameters
name | description | default
--- | --- | ---
user |  | 





### get_user_roles


Get user roles that are not ranks   
Args: user (nextcord.Member): user to search for roles   
Returns: str: String containing roles 
#### Parameters
name | description | default
--- | --- | ---
user |  | 





### get_user_ranks


Get ranks from a user   
Args: user (nextcord.User): user to search for roles   
Returns: str: String containing all ranks 
#### Parameters
name | description | default
--- | --- | ---
user |  | 





### get_user_color_code


Get user roles that are not ranks   
Args: user (nextcord.User): user to search for roles   
Returns: str: String containing roles 
#### Parameters
name | description | default
--- | --- | ---
user |  | 





### setup



#### Parameters
name | description | default
--- | --- | ---
bot |  | 





### setup



#### Parameters
name | description | default
--- | --- | ---
bot |  | 





### setup



#### Parameters
name | description | default
--- | --- | ---
bot |  | 





### check_sticker


checks if a sticker already exists and if file extension is correct   
Args: stickerName ([String]): [Name of sticker to add] stickerExtension ([String]): [Extension of sticker to add]   
Returns: [0]: [name used by other sticker] [1]: [if file extension is correct, must be jpg or png] 
#### Parameters
name | description | default
--- | --- | ---
stickerName |  | 
stickerExtension |  | 





### create_connection


Creates a connection to a database db_file Args: db_file (str): database file to connect Returns: sqlite3.Connection: connection to database 
#### Parameters
name | description | default
--- | --- | ---
db_file |  | 





### create_table


Creates a table in the database Args: conn (sqlite3.Connection): Connection to database table_sql_sentence (str): sql sentence 
#### Parameters
name | description | default
--- | --- | ---
conn |  | 
table_sql_sentence |  | 





### setup_database


Creates the db file and stablish connection to it Returns: sqlite3.Connection: connection to database 
#### Parameters
name | description | default
--- | --- | ---
db_file |  | 





### create_user


Creates a user in the users table Args: conn (sqlite3.Connection): Connection to database user (tuple): info to add 
#### Parameters
name | description | default
--- | --- | ---
conn |  | 
user_data |  | 





### remove_user


Removes a user from database Args: conn (sqlite3.Connection): Connection to database user_id (int): id of user to remove 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
user_id |  | 





### create_rank


Creates a rank in the ranks table Args: conn (sqlite3.Connection): Connection to database rank_data (tuple): info to add 
#### Parameters
name | description | default
--- | --- | ---
conn |  | 
rank_data |  | 





### remove_rank


Removes a rank entry   
Args: con ([type]): [description] rank_id (int): [id of the rank 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
rank_id |  | 





### create_specie


Creates a specie in the species table Args: conn (sqlite3.Connection): Connection to database user (tuple): info to add 
#### Parameters
name | description | default
--- | --- | ---
conn |  | 
specie_data |  | 





### remove_specie


Removes a specie entry   
Args: con ([type]): [description] specie_id (int): [id of the specie 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
specie_id |  | 





### create_color


Creates a color in the colors table Args: conn (sqlite3.Connection): Connection to database user (tuple): info to add 
#### Parameters
name | description | default
--- | --- | ---
conn |  | 
color_data |  | 





### remove_color


Removes a color entry   
Args: con ([type]): [description] color_id (int): [id of the color 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
color_id |  | 





### create_sentence


Creates a sentence in the sentences table Args: conn (sqlite3.Connection): Connection to database sentence (list): info of sentence. Containing [type, sentence] 
#### Parameters
name | description | default
--- | --- | ---
conn |  | 
sentence_data |  | 





### create_record


Creates a record in the records table Args: conn (sqlite3.Connection): Connection to database record (list): info of record. Containing [type, record] 
#### Parameters
name | description | default
--- | --- | ---
conn |  | 
record_data |  | 





### get_name


Gets the name of a user Args: con ([type]): [description] user_id (int): id of user Returns: [str]: name of user 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
user_id |  | 





### set_name


Changes the name of a user Args: conn (sqlite3.Connection): Connection to database user_id (int): id of user name (str): new name for a user 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
user_id |  | 
name |  | 





### get_birthday



#### Parameters
name | description | default
--- | --- | ---
con |  | 
user_id |  | 





### set_birthday



#### Parameters
name | description | default
--- | --- | ---
con |  | 
user_id |  | 
date |  | 





### get_birthdays



#### Parameters
name | description | default
--- | --- | ---
con |  | 





### get_ranks



#### Parameters
name | description | default
--- | --- | ---
con |  | 





### get_species



#### Parameters
name | description | default
--- | --- | ---
con |  | 





### get_colors



#### Parameters
name | description | default
--- | --- | ---
con |  | 





### get_random_sentence


Gets a random sentence   
Args: con ([type]): [description] type (str): type of sentence   
Returns: str: random sentence 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
sentence_type |  | 





### get_latest_id


Gets id of latest item in a table   
Args: con ([type]): [description] table ([str]): table to look   
Returns: int: id of latest sentence 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
table |  | 





### check_entry_in_database


Check if entry exists in table   
Args: con ([type]): [description] table (str): table to check entry_id (int): id of the entry   
Returns: bool: false if not exists, true on the contrary 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
table |  | 
entry_id |  | 





### check_record_in_database


Check if entry exists in table   
Args: con ([type]): [description] table (str): table to check entry_id (int): id of the entry   
Returns: bool: false if not exists, true on the contrary 
#### Parameters
name | description | default
--- | --- | ---
con |  | 
record |  | 





### get_user_avatar


Downloads the avatar of a user   
Args: user (hikari.User): user to download avatar from name (str): user to download avatar from 
#### Parameters
name | description | default
--- | --- | ---
url |  | 
name |  | 





### convert_pic


Converts an image to PNG with a differents size   
Args: picture (str): picture to convert imgName (str): exported picture name imgSize (str): exported image size 
#### Parameters
name | description | default
--- | --- | ---
picture |  | 
imgName |  | 
imgSize |  | None





### get_user


Gets user from a message   
Args: context (Message): Message to get an avatar user (hikari.User, optional): User of a message. Defaults to None.   
Returns: hikari.User: user 
#### Parameters
name | description | default
--- | --- | ---
ctx |  | 
user |  | None





### exists_string_in_file


Checks if string is contained as line in file_name   
Args: file_name (str): file to check string (str): string to search   
Returns: bool: True if string is in file_name, False if not 
#### Parameters
name | description | default
--- | --- | ---
file_name |  | 
string |  | 





### count_lines_in_file


Counts lines of a file   
Args: file (str): file to count lines from   
Returns: int: number of lines 
#### Parameters
name | description | default
--- | --- | ---
file |  | 





### count_files_in_dir


Counts files in a directory   
Args: directory (str): directory to count files from   
Returns: int: number of files in directory 
#### Parameters
name | description | default
--- | --- | ---
directory |  | 





### get_files_in_directory


Get a list of files in a directory   
Args: directory (str): directory to search   
Returns: [list]: list of files in dir 
#### Parameters
name | description | default
--- | --- | ---
directory |  | 





### write_in_file


Writes text in a file   
Args: file (str): file to write string (str): string to write 
#### Parameters
name | description | default
--- | --- | ---
file |  | 
string |  | 





### get_random_line_of_file


Gets random line of a file   
Args: file (str): file to get the line   
Returns: [str]: random line 
#### Parameters
name | description | default
--- | --- | ---
file |  | 





### delete_files


Delete files needed to create a meme   
Args: elements (list): files used in a meme 
#### Parameters
name | description | default
--- | --- | ---
elements |  | 




