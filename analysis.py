import sqlite3
import pandas as pd
import numpy as np
from helpers import ParseShotOn

class Analysis(object):

    def __init__(self, league_id, team_id, sqlite_file):
        self.league_id = league_id
        self.team_id = team_id
        self.raw_dataframe = pd.DataFrame()
        self.processed_dataframe = pd.DataFrame()
        self.conn = sqlite3.connect(sqlite_file)
        self.cur = self.conn.cursor()

    def retrieve_raw_data(self):
        query = "select * from Match where league_id=? and away_team_api_id=?"
        self.raw_dataframe = pd.read_sql_query(query, self.conn, params=(self.league_id, self.team_id))

    def basic_data_info(self):
        n_records = self.raw_dataframe.shape[0]
        n_away_team_wins = self.raw_dataframe.loc[self.raw_dataframe['away_team_goal'] > self.raw_dataframe['home_team_goal']].shape[0]
        n_draws = self.raw_dataframe.loc[self.raw_dataframe['away_team_goal'] == self.raw_dataframe['home_team_goal']].shape[0]
        n_home_team_wins = self.raw_dataframe.loc[self.raw_dataframe['away_team_goal'] < self.raw_dataframe['home_team_goal']].shape[0]
        return [n_records, n_away_team_wins, n_draws, n_home_team_wins]

    def addInitAttributes(self):
        self.processed_dataframe = self.raw_dataframe[['stage', 'home_team_api_id']]
        
    def addPlayerSkillTotals(self):
        away_team_skills = []
        home_team_skills = []
        for index, row in self.raw_dataframe.iterrows():
            query = "select overall_rating from Player_Attributes where player_api_id in (?,?,?,?,?,?,?,?,?,?,?)"
            df = pd.read_sql_query(query, self.conn, params=(row['away_player_1'], row['away_player_2'], row['away_player_3'], row['away_player_4'], row['away_player_5'], row['away_player_6'],
            row['away_player_7'], row['away_player_8'], row['away_player_9'], row['away_player_10'], row['away_player_11']))
            away_team_skills.append(df['overall_rating'].sum())

            query = "select overall_rating from Player_Attributes where player_api_id in (?,?,?,?,?,?,?,?,?,?,?)"
            df = pd.read_sql_query(query, self.conn, params=(row['home_player_1'], row['home_player_2'], row['home_player_3'], row['home_player_4'], row['home_player_5'], row['home_player_6'],
            row['home_player_7'], row['home_player_8'], row['home_player_9'], row['home_player_10'], row['home_player_11']))
            home_team_skills.append(df['overall_rating'].sum())

        self.processed_dataframe['home_skills_total'] = pd.Series(home_team_skills).values
        self.processed_dataframe['away_skills_total'] = pd.Series(away_team_skills).values
     
    def addPlayerHeightTotals(self):
        away_team_height = []
        home_team_height = []
        for index, row in self.raw_dataframe.iterrows():
            query = "select height from Player where player_api_id in (?,?,?,?,?,?,?,?,?,?,?)"
            df = pd.read_sql_query(query, self.conn, params=(row['away_player_1'], row['away_player_2'], row['away_player_3'], row['away_player_4'], row['away_player_5'], row['away_player_6'],
            row['away_player_7'], row['away_player_8'], row['away_player_9'], row['away_player_10'], row['away_player_11']))
            away_team_height.append(df['height'].sum())

            query = "select height from Player where player_api_id in (?,?,?,?,?,?,?,?,?,?,?)"
            df = pd.read_sql_query(query, self.conn, params=(row['home_player_1'], row['home_player_2'], row['home_player_3'], row['home_player_4'], row['home_player_5'], row['home_player_6'],
            row['home_player_7'], row['home_player_8'], row['home_player_9'], row['home_player_10'], row['home_player_11']))
            home_team_height.append(df['height'].sum())

        self.processed_dataframe['home_height_total'] = pd.Series(home_team_height).values
        self.processed_dataframe['away_height_total'] = pd.Series(away_team_height).values

    def parse_shoton_tags(self):
        away_team_shots_blocked = []
        home_team_shots_blocked = []
        away_team_shots_on_target = []
        home_team_shots_on_target = []
        for index, row in self.raw_dataframe.iterrows():
            parser = ParseShotOn()
            parser.feed(row['shoton'])
            parser.split_data_for_row(self.team_id)

            data = parser.get_split_data()
            away_team_shots_blocked.append(data['away_team_shots_blocked'])
            home_team_shots_blocked.append(data['home_team_shots_blocked'])
            away_team_shots_on_target.append(data['away_team_shots_on_target'])
            home_team_shots_on_target.append(data['home_team_shots_on_target'])

        self.processed_dataframe['away_team_shots_blocked'] = pd.Series(away_team_shots_blocked).values
        self.processed_dataframe['home_team_shots_blocked'] = pd.Series(home_team_shots_blocked).values
        self.processed_dataframe['away_team_shots_on_target'] = pd.Series(away_team_shots_on_target).values
        self.processed_dataframe['home_team_shots_on_target'] = pd.Series(home_team_shots_on_target).values

    # Getters
    def get_raw_dataframe(self):
        return self.raw_dataframe

    def get_processed_dataframe(self):
        return self.processed_dataframe



