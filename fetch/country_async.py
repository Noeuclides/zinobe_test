import asyncio
import logging
from typing import Any

from aiohttp import ClientResponseError
from aiohttp.client import ClientSession

from fetch.base_fetch import BaseFetchProcess

logging.getLogger().setLevel(logging.INFO)


EMPTY_LIST = []


class FetchAsyncCountry(BaseFetchProcess):

    def fetch_regions(self) -> None:
        for region in self.regions_table['Region']:
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self.fetch_async(region))
            loop.run_until_complete(future)
            future.result()

    async def fetch_async(self, region: str) -> list:
        url = f'https://restcountries.eu/rest/v2/region/{region}'
        tasks = []
        async with ClientSession() as session:
            task = asyncio.ensure_future(self.fetch(session, url))
            tasks.append(task)
            responses = await asyncio.gather(*tasks)
        return responses

    async def fetch(self, session: ClientSession, url: str) -> Any:
        try:
            async with session.get(url, timeout=15) as response:
                json_resp = await response.json()
                self.row_processing(json_resp)
        except ClientResponseError as e:
            logging.warning(e.code)
        except asyncio.TimeoutError:
            logging.warning("Timeout")
        except Exception as e:
            logging.warning(e)
        else:
            return json_resp
        return
