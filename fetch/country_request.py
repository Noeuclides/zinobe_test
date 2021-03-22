import requests
from fetch.base_fetch import BaseFetchProcess
import logging

logging.getLogger().setLevel(logging.INFO)


class FetchCountry(BaseFetchProcess):

    def fetch_regions(self) -> None:
        for region in self.regions_table['Region']:
            url = f'https://restcountries.eu/rest/v2/region/{region}'
            try:
                json_resp = requests.get(url).json()
                self.row_processing(json_resp)
            except Exception as e:
                logging.info(f'could not fetch {url}')
