import httpx
import base64
from zoomeyesearch.logger.logger import Logger
from zoomeyesearch.barchart.barchart import BarChart
from zoomeyesearch.utils.utils import Utils

class ZoomeyeStats():
    def __init__(
        self,
        jwt:str, 
        field: str,
        query:str,
        verbose = True,
        limit:int=1000):
        self.query = query
        self.jwt = jwt
        self.field = field
        self.limit = limit
        self._headers = {
            "cube-authorization": self.jwt
        }
        self._url = f"https://www.zoomeye.ai/api/analysis/aggs"
        self._logger = Logger()
        self._utils = Utils()
        self.verbose = verbose
        
    async def search(self) -> dict:
        try:
            query = self.query.encode('utf-8')
            query = base64.b64encode(query).decode('utf-8')
            params = {
                "language": "en",
                "field": self.field,
                "limit": self.limit,
                "q": query
            }
            self._headers["User-Agent"] = self._utils.random_useragent()
            async with httpx.AsyncClient(verify=False) as session:
                response:httpx.Response = await session.request("GET", self._url,headers=self._headers, params=params, timeout=60)
                data = response.json()
                status = data.get("status")
                if status != 200 or status is None:
                    if self.verbose:
                        self._logger.warn(f"Bad API response code, please check your API usage")
                    return None
                return data
        except Exception as e:
            if self.verbose:
                self._logger.warn(f"Error occurred in the zoomeye stats search due to: {e}")
            else:
                raise
            
    def display(self,data: dict):
        try:
            top_data = data.get(self.field, None)
            if top_data is None or len(top_data) == 0:
                if self.verbose:
                    self._logger.warn(f"No data found for field: {self.field}")
                return
            chart_data = [{"name": str(data["name"]), "value": data["count"]} for data in top_data]
            chart = BarChart(
            chart_data,
            width=100,
            show_values=True,
            show_percent=True
            )
            chart.render()
        except Exception as e:
            if self.verbose:
                self._logger.warn(f"Error occurred while displaying the stats due to: {e}")
            else:
                raise
        