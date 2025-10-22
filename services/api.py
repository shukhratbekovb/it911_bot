import requests

from configs import API_URL, API_HEADERS


class ApiService:
    async def create_user(
            self
    ):
        pass

    def create_lead(
            self,
            data: dict,
            target_id: str = None

    ):
        url = f"{API_URL}/leads?target_id={target_id}" if target_id else f"{API_URL}/leads"
        response = requests.post(
            url="https://it911.uz/api/leads/",
            # headers=API_HEADERS,
            json=data,
        )
        if response.status_code != 201:
            return False
        return True


