import datetime
from typing import List
from bs4 import BeautifulSoup


class UserField:
    def __init__(self, data: dict) -> None:
        self.name = data["name"]
        self.value = data["value"]
        self.verified_at = data["verified_at"]


class User:
    def __init__(
        self,
        data: dict,
    ) -> None:
        self.id = data["id"]
        self.username = data["username"]
        self.avatar = data["avatar"]
        self.bot = data["bot"]
        self.header = data["header"]
        self.display_name = data["display_name"]
        self.created_at = datetime.datetime.strptime(
            data["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.note = data["note"]
        self.url = data["url"]
        self.followers_count = data["followers_count"]
        self.following_count = data["following_count"]
        self.statuses_count = data["statuses_count"]
        self.fields = []
        for x in data["fields"]:
            self.fields.append(UserField(x))


class Status:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.created_at = datetime.datetime.strptime(
            data["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.in_reply_to_id = data["in_reply_to_id"]
        self.in_reply_to_account_id = data["in_reply_to_account_id"]
        self.url = data["url"]
        self.replies_count = data["replies_count"]
        self.reblogs_count = data["reblogs_count"]
        self.favourites_count = data["favourites_count"]

        soup = BeautifulSoup(data["content"], "html.parser")
        self.content = soup.get_text()
        self.account = User(data["account"])
        self.media_attachments = []
        for x in data["media_attachments"]:
            self.media_attachments.append(x["url"])
        self.mentions = data["mentions"]
        self.tags = data["tags"]
        self.emojis = data["emojis"]
        self.card = data["card"]
        self.poll = data["poll"]
        self.raw_data = data

    def __str__(self) -> str:
        return f"Status by {self.account.display_name}: {self.content}"

    def is_reblog(self) -> bool:
        return False

    def has_media_attachment(self) -> bool:
        return len(self.media_attachments) > 0


class RebloggedStatus(Status):
    def __init__(
        self,
        data: dict,
    ) -> None:
        super().__init__(data)
        self.reblog = Status(data["reblog"])

    def __str__(self) -> str:
        return f"Status of {self.reblog.account.display_name} rebloged by {self.account.display_name}: {self.reblog.content}"

    def is_reblog(self) -> bool:
        return True
