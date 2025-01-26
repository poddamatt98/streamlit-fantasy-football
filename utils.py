import requests
import io
import pandas as pd
import streamlit as st
import yaml


@st.cache_data
def get_github_files(path):
    """Retrieve a list of files in a GitHub repository subfolder."""

    response = requests.get(path, headers={})
    if response.status_code == 200:
        data = response.json()
        files = [item['name'] for item in data if item['type'] == 'file']
        return files
    else:
        raise Exception(f"Error {response.status_code}: {response.json()}")

# @st.cache_data
def read_remote_yaml(path):
    download_url = requests.get(path).json()['download_url']
    data_str = requests.get(download_url).content
    
    config = yaml.safe_load(io.StringIO(data_str.decode('utf-8')))

    return config

# @st.cache_data
def read_remote_csv(path):
    download_url = requests.get(path).json()['download_url']
    data_str = requests.get(download_url).content
    data = pd.read_csv(io.StringIO(data_str.decode('utf-8')))

    return data

def process_data(data, config):
    data['buyPrice'] = data['buyPrice'].astype(int)
    data['startingFCPrice'] = data['startingFCPrice'].astype(int)
    data['actualFCPrice'] = data['actualFCPrice'].astype(int)

    data['Rapporto'] = (data['actualFCPrice'] / data['startingFCPrice']).clip(upper=config['ratio_ub'], lower=config['ratio_lb']).round(int(config['precision']))
    data['releasePrice'] = (data['Rapporto'] * data['buyPrice']).round(0).clip(lower=1).astype(int)
    
    return data
    
def highlight_rows(row):
    if row["Rapporto"] >= 1:
        return ['background-color: green'] * len(row)  # Apply light green to the entire row
    else:
        return ['background-color: red'] * len(row)  # Apply light coral to the entire row