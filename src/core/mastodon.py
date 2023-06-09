from typing import List
from dotenv import load_dotenv
import nextcord
import requests
import os
from nextcord import Embed, Colour
from model.mastodon import User, UserField, Status, RebloggedStatus
from core.database import Database

class Mastodon:
    def __init__(self,db:Database) -> None:
        """Creates a new Mastodon object

        Args:
            token (str): application token
            app_instance (str): Instace where the app is hosted
        """
        self._token = os.getenv("MASTODON_TOKEN")
        self._app_instance = os.getenv("MASTODON_APP_INSTANCE")
        self.db=Database()

    def exists_instance(self, instance: str) -> bool:
        """Check if instance exists

        Args:
            instance (str): Instance to check (without @)

        Returns:
            bool: True if instance exists, False if not
        """
        try:
            requests.get(f"https://{instance}")
        except:
            return False
        return True
    
    def exists_account(self, username: str, instance: str) -> bool:
        """Check if account exists

        Args:
            username (str): Username of account (without @)
            instance (str): Instance where the account is hosted (without @)
            
        Returns:
            bool: True if account exists, False if not
        """
        try:
            self._get_user(username, instance)
        except:
            return False
        return True
    

    def _get_user(self, username: str, instance: str) -> User:
        """Gets user object from username and instance

        Args:
            username (str): Username of user (without @)
            instance (str): Instance where the user is hosted (without @)

        Returns:
            model.mastodon.User: User object
        """
        user = f"@{username}@{instance}"
        headers = {
            "Authorization": f"Bearer {self._token}",
        }
        try:
            result = requests.get(
                f"https://{self._app_instance}/api/v1/accounts/search",
                headers=headers,
                params={"q": f"{user}"},
            ).json()[0]
        except:
            raise Exception("User not found")
        user_fields = []
        for field in result["fields"]:
            user_fields.append(UserField(field))

        user = User(result)

        return user

    def get_statuses(self, username: str, instance: str,limit:int=20) -> List[Status]:
        """Get latest statuses from a user

        Args:
            username (str): Username of user (without @)
            instance (str): Instance where the user is hosted (without @)

        Example:
            get_statuses("teko", "meow.social")

        Returns:
            list: List of statuses
        """
        user = self._get_user(username, instance)

        result = requests.get(
            f"https://{self._app_instance}/api/v1/accounts/{user.id}/statuses",
            params={"limit": limit},
        ).json()
        output = []
        for x in result:
            if x["reblog"] != None:  # Rebloged status
                rebloged_status = RebloggedStatus(x)
                output.append(rebloged_status)

            else:
                status = Status(x)
                output.append(status)
        return output

    def get_latest_status(self, username: str, instance: str) -> Status:
        """Get latest status from a user

        Args:
            username (str): Username of user (without @)
            instance (str): Instance where the user is hosted (without @)

        Example:
            get_latest_status("teko", "meow.social")

        Returns:
            str: Latest status
        """
        statuses = self.get_statuses(username, instance)
        return statuses[5]
    
    def get_latest_image_not_repeated(
        self,
        guild: nextcord.Guild,
        username: str,
        instance:str,
    ) -> Embed:
        """ Creates an embed from the latest image of a user

        Args:
            guild (nextcord.Guild): To get the database
            username (str): Of the account
            instance (str): Instance where the account is hosted

        Returns:
            Embed: Embed of the image
        """
        output = None
        statuses= self.get_statuses(username, instance,200)
       

        for status in statuses:

            if status.has_media_attachment():
                media_attachment = status.media_attachments[0]
                
                if not self.db.record_exists(guild,media_attachment):
                    self.db.insert_record(guild,instance,media_attachment,username)

                    output = status
                    break

        if output is None:
            return None

        # Remove statuses from db if they are not fetched
        media_attachments = [
            x.media_attachments[0] if x.has_media_attachment() else ""
            for x in statuses
        ]
        self.db.clean_records(guild,instance,media_attachments)

        embed = self.create_embed(output)

        return embed

    def create_embed(self, status: Status | RebloggedStatus) -> Embed:
        """Creates an embed from a status

        Args:
            status (list): Status to create embed from

        Returns:
            Embed: embed of status
        """

        embed = Embed(
            color=Colour.from_rgb(99, 100, 255),
        )

        if status.is_reblog():
            embed.title = f"{status.account.display_name} reblogged {status.reblog.account.display_name}"
            embed.description = status.reblog.content
            embed.set_author(
                name=status.reblog.account.display_name,
                icon_url=status.reblog.account.avatar,
            )
            embed.add_field(name="Link to post", value=status.reblog.url, inline=False)

            if status.reblog.has_media_attachment():
                embed.set_image(url=status.reblog.media_attachments[0])
        else:
            embed.title = status.account.display_name
            embed.description = status.content
            embed.set_author(
                name=status.account.display_name, icon_url=status.account.avatar
            )
            embed.add_field(name="Link to post", value=status.url, inline=False)
            
            if status.has_media_attachment():
                embed.set_image(url=status.media_attachments[0])
        return embed
