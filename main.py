#European soccer dataset & supervised learning
import pandas as pd
from IPython.display import display
from analysis import Analysis

#predict Arsenal away wins
#pick out feature most important to predicting away wins
league_id=1729
away_team_api_id=9825
sqlite_file = '/Users/schumanzhang/Desktop/machine_learning_projects/soccer_dataset/raw_data/database.sqlite'

analysis = Analysis(league_id, away_team_api_id, sqlite_file)
analysis.retrieve_raw_data()

print "raw features: {}".format(analysis.get_raw_dataframe().columns.values)

basic_info_list = analysis.basic_data_info()

print "total records: {}".format(basic_info_list[0])
print "total away team wins: {}".format(basic_info_list[1])
print "total draws: {}".format(basic_info_list[2])
print "total home team wins: {}".format(basic_info_list[3])

analysis.addInitAttributes()
analysis.addPlayerSkillTotals()

print(analysis.get_processed_dataframe().head())
