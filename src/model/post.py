import nextcord
from service import service,twitter,reddit
class post:
    def __init__(self,guild:nextcord.Guild, channel:nextcord.TextChannel, service:service, account:str, visibility:str,interval:int,id:int=None) -> None:
        """Creates a post. It represents a way of sending publications of an account into a Textchannel in a frequency

        Args:
            guild (nextcord.Guild): Guild of the channel
            channel (nextcord.TextChannel): channel to send the post
            service (str): Social media where the account is
            account (str): Account to get the publications
            visibility (str): SFW or NSFW
            interval (int): Time in minutes between posts
            id(int): Id of the post
        """        
        self.guild=guild
        self.channel=channel
        self.service=service
        self.account=account
        self.visibility=visibility
        self.interval=interval
        self.id=id
        
    def add_to_db(self):
        pass
    
    def remove_from_db(self):
        pass
        


post_meme=post(nextcord.Guild(),nextcord.TextChannel(),service.twitter,"account","sfw",5)