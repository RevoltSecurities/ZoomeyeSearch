import httpx
from typing import Dict, List
from zoomeyesearch.logger.logger import Logger


class ZoomeyeSubenum:
    def __init__(self, apikey: str, domain: str, type: int = 1, verbose: bool = True):
        self.logger = Logger()
        self.apikey: str = apikey
        self.domain: str = domain
        self.type: int = type
        self.verbose: bool = verbose
        self.headers: Dict[str, str] = {"API-KEY": self.apikey}
        self.results: List[Dict] = []

    async def enumerate(self) -> List[Dict]:
        page = 1
        base_url = "https://api.zoomeye.ai/domain/search"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                while True:
                    url = f"{base_url}?q={self.domain}&type={self.type}&page={page}"
                    response = await client.request("GET",url, headers=self.headers,timeout=30)

                    if response.status_code != 200:
                        if self.verbose:
                            self.logger.error(f"[{response.status_code}] Failed: {response.text}")
                        break

                    json_data = response.json()

                    if json_data.get("status") != 200:
                        if self.verbose:
                            self.logger.error(f"Unexpected status in response: {json_data}")
                        break

                    subdomain_list = json_data.get("list", [])
                    if not subdomain_list or len(subdomain_list) == 0:
                        break

                    for subdomain in subdomain_list:
                        self.results.append(subdomain.get('name'))
                    page += 1
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Error occurred in Zoomeye subdomain module: {e}")
            else:
                raise

        return self.results
