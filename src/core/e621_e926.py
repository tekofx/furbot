
from typing import List
import requests
from datetime import datetime

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
        return f"Tags(general={self.general}, species={self.species}, character={self.character}, artist={self.artist}, invalid={self.invalid}, lore={self.lore}, meta={self.meta})"

class File:
    def __init__(self, extension:str,url:str) -> None:
        self.extension=extension
        self.url=url
        
    def __repr__(self) -> str:
        return f"File(extension={self.extension}, url={self.url})"
        

class Post:
    def __init__(self, id:int, created_at:datetime,file:File,tags:Tags, description:str) -> None:
        self.id=id
        self.created_at=created_at
        self.file=file
        self.tags=tags
        self.description=description
        
        
    def __repr__(self) -> str:
        return f"Post(id={self.id}, created_at={self.created_at}, file={self.file}, tags={self.tags}, description={self.description})"
    


class E621_E926:
    def __init__(self) -> None:
        pass
    
    def get_posts(self, tags: List[str], limit: int = 1) -> List[Post]:
        """Get posts from e621.net

        Args:
            tags (str): Tags to search
            limit (int, optional): Number of posts to get. Defaults to 1.

        Returns:
            list: List of posts
        """
        url = "https://e621.net/posts.json"
        params = {"tags": tags, "limit": limit}
        result = requests.get(url, params=params, headers={"User-Agent": "Discord Bot"}).json()
        output = []
        for x in result["posts"]:
            tags=Tags(x["tags"]["general"],x["tags"]["species"],x["tags"]["character"],x["tags"]["artist"],x["tags"]["invalid"],x["tags"]["lore"],x["tags"]["meta"])
            file=File(x["file"]["ext"],x["file"]["url"])
            post=Post(x["id"],datetime.strptime(x["created_at"],"%Y-%m-%dT%H:%M:%S.%f%z"),file,tags,x["description"])
            output.append(post)
        return output
        


e631 = E621_E926()
posts=e631.get_posts(["fox"],limit=10)
print(posts)