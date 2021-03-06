#European soccer dataset & supervised learning
import pandas as pd
import numpy as np
from IPython.display import display
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from train_model import TrainModel
from knn_gridsearch import KNNModel

from analysis import Analysis

from sklearn.ensemble import RandomForestClassifier

#predict Arsenal away wins
#pick out feature most important to predicting away wins
league_id=1729
away_team_api_id=9825
sqlite_file = '/Users/schumanzhang/Desktop/machine_learning_projects/soccer_dataset/raw_data/database.sqlite'

try:
    processed_data = pd.read_csv('dataframe.csv', index_col=0)
except IOError:
    analysis = Analysis(league_id, away_team_api_id, sqlite_file)
    raw_data = analysis.retrieve_raw_data()
    basic_info_list = analysis.basic_data_info()
    print(basic_info_list)

    analysis.addInitAttributes()
    analysis.addPlayerSkillTotals()
    analysis.addPlayerHeightTotals()

    analysis.parse_selected_tags('shoton', ['away_shoton', 'home_shoton'])
    analysis.parse_selected_tags('shotoff', ['away_shotoff', 'home_shotoff'])
    analysis.parse_selected_tags('foulcommit', ['away_fouls', 'home_fouls'])
    analysis.parse_selected_tags('card', ['away_cards', 'home_cards'])
    analysis.parse_selected_tags('cross', ['away_crosses', 'home_crosses'])
    analysis.parse_selected_tags('corner', ['away_corners', 'home_corners'])
    analysis.parse_selected_tags('possession', ['away_possession', 'home_possession'])
    analysis.addTargetVariable()
    processed_data = analysis.get_processed_dataframe()
    processed_data.to_csv('dataframe.csv')

labels = processed_data.loc[:,['result']]
processed_data.drop(['result'], axis=1, inplace=True)

le = LabelEncoder()
le.fit(np.unique(labels.values))
labels_final = labels.apply(le.transform)

scaler = MinMaxScaler()
numerical = ['home_skills_total', 'away_skills_total', 'home_height_total', 'away_height_total', 'away_shoton',
            'home_shoton', 'away_shotoff', 'home_shotoff', 'away_fouls', 'home_fouls',
            'away_cards', 'home_cards', 'away_crosses', 'home_crosses', 'away_corners',
            'home_corners', 'away_possession', 'home_possession']

features_final = pd.DataFrame(data = processed_data)
features_final[numerical] = scaler.fit_transform(processed_data[numerical])

#split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features_final, labels_final, test_size=0.2, random_state=0) 

#Naive Bayes
from sklearn.naive_bayes import GaussianNB
naive_bayes_learner = GaussianNB()
naive_bayes_model = TrainModel(X_train.shape[0], naive_bayes_learner, X_train, y_train, X_test, y_test)
naive_bayes_model.train_predict()
print(naive_bayes_model.get_results())

#KNN
from sklearn.neighbors import KNeighborsClassifier
knn_learner = KNeighborsClassifier()
k = [3, 4, 5]
knn_model = KNNModel(X_train.shape[0], knn_learner, X_train, y_train, X_test, y_test, k)
knn_model.grid_search()
print(knn_model.get_results())

#SVM
#stochastic gradient descent classfier
#random_forest_classifier




