# Zinobe

App that generates a pandas dataframe by fetching the 
[restcountries API](https://rapidapi.com/apilayernet/api/rest-countries-v1).

## Requirements
Python3.7 or greater.

To run the django app use the python package manager [pipenv](https://pipenv-es.readthedocs.io/es/latest/).

## Installation

Install the dependencies:

```bash
pipenv install
```

## Usage

In the fetch package are three modules that fetch an API endpoint in different ways.
Therefore, you can run the app in three different modes in order to see the performance differences using threads, async request or simple requests with python.


### Threads:
```bash
pipenv run python main.py thread
```

### Async:
```bash
pipenv run python main.py async
```

### Requests:
```bash
pipenv run python main.py
```


