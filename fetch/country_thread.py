import logging
from concurrent import futures
from typing import Any, Generator

import requests

from fetch.base_fetch import BaseFetchProcess

logging.getLogger().setLevel(logging.INFO)


class FetchThreadCountry(BaseFetchProcess):

    def fetch_regions(self) -> Generator:
        url_list = []
        for region in self.regions_table['Region']:
            url = f'https://restcountries.eu/rest/v2/region/{region}'
            url_list.append(url)
        with futures.ThreadPoolExecutor() as executor:
            responses = executor.map(self.fetch_url, url_list)
        return responses

    def fetch_url(self, url: str) -> None:
        try:
            json_resp = requests.get(url).json()
            self.row_processing(json_resp)
        except Exception as e:
            logging.info(f'could not fetch {url}')
