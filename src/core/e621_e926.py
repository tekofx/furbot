import nextcord
from typing import List
import requests
from datetime import datetime
from core.database import Database
from nextcord import Embed
class Tags:
    def __init__(self, general:list[str], species:list[str], character:list[str], artist:list[str], invalid:list[str], lore:list[str], meta:list[str]) -> None:
        self.general=general
        self.species=species
        self.character=character
        self.artist=artist
        self.invalid=invalid
        self.lore=lore
        self.meta=meta
        
        
    def __repr__(self) -> str:
        output=" ".join(self.general)+" "+" ".join(self.species)+" "+" ".join(self.character)+" "+" ".join(self.artist)+" "+" ".join(self.invalid)+" "+" ".join(self.lore)+" "+" ".join(self.meta)
        return output

class File:
    def __init__(self, extension:str,url:str) -> None:
        self.extension=extension
        self.url=url
        
    def __repr__(self) -> str:
        return f"File(extension={self.extension}, url={self.url})"
        
 
class Post:
    def __init__(self, id:int, service:str,created_at:datetime,file:File,tags:Tags, description:str,pool:id=None) -> None:
        self.id=id
        self.created_at=created_at
        self.file=file
        self.tags=tags
        self.description=description
        self.pool_id=pool
        if pool!=None:
            self.pool_url=f"{service}/pools/{pool}"
        self.url=f"{service}/posts/{self.id}"
        
        
    def __repr__(self) -> str:
        return f"Post(id={self.id}, created_at={self.created_at}, file={self.file}, tags={self.tags}, description={self.description}, pool={self.pool_id})"
    


class E621_E926:
    def __init__(self, db:Database, url:str) -> None:
        self.url=url
        self.api_url=f"{url}/posts.json"
        self.db=db
        pass
    
    def get_posts(self, tags: str,page:int=1, limit: int = 100 ) -> List[Post]:
        """Get posts from e621.net

        Args:
            tags (str): Tags to search
            limit (int, optional): Number of posts to get. Defaults to 1.

        Returns:
            list: List of posts
        """
        params = {"tags": tags, "limit": limit, "page": page}
        result = requests.get(self.api_url, params=params, headers={"User-Agent": "Discord Bot"}).json()
        output = []
        if len(result["posts"])==0:
            return None
        for x in result["posts"]:
            tags=Tags(x["tags"]["general"],x["tags"]["species"],x["tags"]["character"],x["tags"]["artist"],x["tags"]["invalid"],x["tags"]["lore"],x["tags"]["meta"])
            file=File(x["file"]["ext"],x["file"]["url"])
            pool=None
            if len(x["pools"])>0:
                pool=x["pools"][0]
            post=Post(x["id"],self.url,datetime.strptime(x["created_at"],"%Y-%m-%dT%H:%M:%S.%f%z"),file,tags,x["description"],pool)
            output.append(post)
        return output
    
    def get_post_not_repeated(self, guild:nextcord.Guild, tags: str) -> Post:
        """Get a post from e621.net that is not repeated in the database

        Args:
            guild (nextcord.Guild): Guild to get the channel
            tags (str): Tags to search

        Returns:
            Post: Post from e621.net
        """
        posts=self.get_posts(tags)
        if posts==None:
            return None
        while True:
        
            for post in posts:
                if  not  self.db.record_exists(guild, post.id):
                    self.db.insert_record(guild, "e621", post.id)
                    return post
                
            # If all posts are repeated, get the next posts after the last one
            posts=self.get_posts(tags,page="a"+str(posts[-1].id))
            

class e621(E621_E926):
    def __init__(self,db:Database) -> None:
        super().__init__(db,"https://e621.net")
        
        
class e926(E621_E926):
    def __init__(self,db:Database) -> None:
        super().__init__(db,"https://e926.net")
    
    

""" e631 =e621()
posts=e631.get_posts(["fox"],limit=10)
print(posts) """
