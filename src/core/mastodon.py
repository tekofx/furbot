import requests


def get_statuses(user_id: int, instance: str):
    result = requests.get(
        f"https://{instance}/api/v1/accounts/{user_id}/statuses"
    ).json()
    return result


def instance_exists(instance: str) -> bool:
    try:
        requests.get(f"https://{instance}")
    except:
        return False
    return True


def get_user_id(username: str, instance: str) -> int:
    result = requests.get(
        f"https://{instance}/api/v1/accounts/search",
        headers={"Authorization": "Bearer iyKgbU8HrL7mQEzY3roxgyHvzSgtkG_h1j6JdniSPHI"},
        params={"q": f"{username}@{instance}"},
    ).json()

    user_id = 0
    for x in result:
        if x["url"] == f"https://{instance}/@{username}":
            user_id = x["id"]
            return user_id
