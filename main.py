#European soccer dataset & supervised learning
import pandas as pd
from IPython.display import display
from analysis import Analysis

#predict Arsenal away wins
#pick out feature most important to predicting away wins
league_id=1729
away_team_api_id=9825
sqlite_file = '/Users/schumanzhang/Desktop/machine_learning_projects/soccer_dataset/raw_data/database.sqlite'

try:
    processed_data = pd.read_csv('dataframe.csv')
except IOError:
    analysis = Analysis(league_id, away_team_api_id, sqlite_file)
    raw_data = analysis.retrieve_raw_data()
    basic_info_list = analysis.basic_data_info()
    print(basic_info_list)

    analysis.addInitAttributes()
    analysis.addPlayerSkillTotals()
    analysis.addPlayerHeightTotals()

    analysis.parse_selected_tags('shoton', ['away_shoton', 'home_shoton'])
    analysis.parse_selected_tags('shotoff', ['away_shotff', 'home_shotoff'])
    analysis.parse_selected_tags('foulcommit', ['away_fouls', 'home_fouls'])
    analysis.parse_selected_tags('card', ['away_cards', 'home_cards'])
    analysis.parse_selected_tags('cross', ['away_crosses', 'home_crosses'])
    analysis.parse_selected_tags('corner', ['away_corners', 'home_corners'])
    analysis.parse_selected_tags('possession', ['away_possession', 'home_possession'])
    analysis.addTargetVariable()
    processed_data = analysis.get_processed_dataframe()
    processed_data.to_csv('dataframe.csv')

print(processed_data.head())
