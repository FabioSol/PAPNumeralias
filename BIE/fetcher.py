import urllib.request
import json
import re
import pandas as pd
import warnings

class Fetcher:
    @staticmethod
    def request_url(url):
        data = urllib.request.urlopen(url).read()
        decoded = re.sub(r'\\u000d\\u000a|\\u000d|\\u000a|\xa0', ' ', data.decode("utf-8"))
        return json.loads(decoded)

    @staticmethod
    def get_series(series_key:str,format:str=None, raw:bool=False, ignore_warnings:bool=True):
        if ignore_warnings:
            warnings.filterwarnings('ignore', category=UserWarning)
        url = f"https://www.inegi.org.mx/app/api/indicadores/interna_v1_3/indicador/{series_key}/0700/es/false/0/json/96fbd1bf-21e6-28e3-6e64-2b15999d2c89"
        response = Fetcher.request_url(url)
        if raw:
            return response
        freq = response['MetaData']['Freq']
        name = f"{response['MetaData']['Name']} {response['MetaData']['Unit']} {response['MetaData']['Region']} {freq}"
        data = response["Data"]["Serie"]
        serie =pd.Series({entry['TimePeriod']: pd.to_numeric(entry['CurrentValue'], errors='coerce') for entry in data},name=name)
        serie.index = pd.to_datetime(serie.index, format=format)
        return serie


    @staticmethod
    def get_children_nodes(series_key:str):
        url=f"https://www.inegi.org.mx/app/api/indicadores/interna_v1_3/API.svc/NodosTemas/null/es/{series_key}/null/null/null/0/true/99/6/json/96fbd1bf-21e6-28e3-6e64-2b15999d2c89"
        response = Fetcher.request_url(url)
        return response

    @staticmethod
    def get_indicators_by_subject(series_key:str):
        url = f"https://www.inegi.org.mx/app/api/indicadores/interna_v1_3/API.svc/IndicadoresPorTemaRecursivo/null/{series_key}/es/null/0/1500/null/0/true/99%20/6/json/96fbd1bf-21e6-28e3-6e64-2b15999d2c89?"
        response = Fetcher.request_url(url)
        return list(filter(None, response['indicadoresTodos'].split(",")))
