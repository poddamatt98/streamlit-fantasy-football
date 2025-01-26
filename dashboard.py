import streamlit as st
import pandas as pd
from utils import get_github_files, read_remote_csv, read_remote_yaml, process_data, highlight_rows
import yaml
import os

st.title('Fantacalcio manager')

data_path = 'data/release_prices'
config_path = 'data/config'

# files = get_github_files(data_path)
files = os.listdir(data_path)

seasons = set([f.split('_')[0] for f in files])

season_col, league_col, team_col = st.columns(3)

selected_season = season_col.selectbox('Stagione', options=seasons)

leagues = set([f.split('_')[1] for f in files if f.startswith(selected_season)])

selected_league = league_col.selectbox('Lega', options=leagues)

# read file
data_file = [f for f in files if f.startswith(f'{selected_season}_{selected_league}')][0]
config_file = '_'.join(data_file.split('_')[:-1]) + '_config.yaml'

data = pd.read_csv(data_path + '/' + data_file).dropna().reset_index(drop=True)

with open(config_path + '/' + config_file, 'r') as f:
    config = yaml.safe_load(f)

processed_data = process_data(data, config)

teams = processed_data.team.unique()
selected_team = team_col.selectbox('Squadra', options=teams)

team_data = processed_data[processed_data.team == selected_team].drop('team', axis=1).reset_index(drop=True)
team_data = team_data.rename({
    'role': 'Ruolo',
    'name': 'Nome',
    'buyPrice': 'P. Acq.',
    'startingFCPrice': 'Quot. Iniz.',
    'actualFCPrice': 'Quot. Att.',
    'releasePrice': 'Prezzo di Svincolo'
}, axis=1)

table = team_data.style.apply(highlight_rows, axis=1)

st.table(table)