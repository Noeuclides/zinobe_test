import hashlib
import sqlite3 as sql
import time
from random import randint
from typing import Any

import pandas as pd
import requests
from pandas.core.frame import DataFrame


EMPTY_LIST = []


class BaseFetchProcess:
    URL = 'https://restcountries.eu/rest/v2/all'
    COLUMNS = ['Region', 'City Name', 'Languaje', 'Time']
    regions_table = {column: EMPTY_LIST[:] for column in COLUMNS}

    def __init__(self) -> None:
        self.regions_table = self.regions_table_set()

    def regions_table_set(self) -> dict:
        self.get_regions()
        self.fetch_regions()
        return self.regions_table

    def get_regions(self) -> None:
        json_resp = requests.get(self.URL).json()
        regions = [country.get('region')
                   for country in json_resp if country.get('region')]
        self.regions_table['Region'] = list(set(regions))

    def fetch_regions(self) -> None:
        pass

    @staticmethod
    def encrypt(string: str) -> str:
        return hashlib.sha1(bytes(string, 'utf-8')).hexdigest()

    def row_processing(self, json_resp: list) -> None:
        init_time = time.perf_counter()
        index = randint(0, len(json_resp) - 1)
        country = json_resp[index]
        lang = country.get('languages')
        lang_name = lang[0].get('name')
        self.regions_table['City Name'].append(country.get('name'))
        self.regions_table['Languaje'].append(self.encrypt(lang_name))
        t = (time.perf_counter() - init_time) * 1000
        self.regions_table['Time'].append(f'{t:.2f} ms')

    def create_df(self) -> DataFrame:
        return pd.DataFrame(self.regions_table, columns=self.COLUMNS)

    @staticmethod
    def df_to_sql(df: DataFrame, db_name: str) -> None:
        conn = sql.connect(f'{db_name}.db')
        df.to_sql(db_name, conn, if_exists='replace')

    @staticmethod
    def df_to_json(df: DataFrame, file_name: str) -> None:
        df.to_json(f'{file_name}.json', orient="table")

    @staticmethod
    def get_stats(df: DataFrame) -> None:
        column_cleaned = df['Time'].str.replace(' ms', '')
        str_to_num = pd.to_numeric(column_cleaned, errors='coerce')
        print(f'Maximum time to process table rows: {str_to_num.max()}')
        print(f'Minimum time to process table rows: {str_to_num.min()}')
        print(f'Mean time to process table rows: {str_to_num.mean():.2f}')
        print(f'Total time to process table rows: {str_to_num.sum():.2f}')
