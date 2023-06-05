from typing import List
from dotenv import load_dotenv
import requests
import os
from nextcord import Embed, Colour
from model.mastodon import User, UserField, Status, RebloggedStatus


class Mastodon:
    def __init__(self) -> None:
        """Creates a new Mastodon object

        Args:
            token (str): application token
            app_instance (str): Instace where the app is hosted
        """
        self._token = os.getenv("MASTODON_TOKEN")
        self._app_instance = os.getenv("MASTODON_APP_INSTANCE")

    def instance_exists(self, instance: str) -> bool:
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
        result = requests.get(
            f"https://{self._app_instance}/api/v1/accounts/search",
            headers=headers,
            params={"q": f"{user}"},
        ).json()[0]
        user_fields = []
        for field in result["fields"]:
            user_fields.append(UserField(field))

        user = User(result)

        return user

    def get_statuses(self, username: str, instance: str) -> List[Status]:
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
            f"https://{self._app_instance}/api/v1/accounts/{user.id}/statuses"
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

    def get_latest_status(self, username: str, instance: str) -> str:
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
        return statuses[0]

    def get_embed(self, status: list) -> str:
        """Creates an embed from a status

        Args:
            status (list): Status to create embed from

        Returns:
            Embed: embed of status
        """
        user = status["account"]["username"]
        avatar = status["account"]["avatar"]

        # Status is a reblog
        if "reblog":
            text = status["reblog"]["content"]
        else:
            text = status["content"]

        embed = Embed(
            title="Twitter",
            description=text,
            color=Colour.from_rgb(99, 100, 255),
        )
        embed.set_image(url=tweet.entities["media"][0]["media_url"])
        embed.set_author(name=user, icon_url=avatar)
        return embed


load_dotenv("dev.env")
mastodon = Mastodon()

user = mastodon._get_user("teko", "meow.social")
print(user.created_at)

status = mastodon.get_latest_status("teko", "meow.social")
print(status)
