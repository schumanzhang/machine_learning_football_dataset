from sklearn.metrics import accuracy_score, fbeta_score, precision_score, recall_score, make_scorer
from time import time

class TrainModel(object):

    def __init__(self, sample_size, learner, X_train, y_train, X_test, y_test):
        self.sample_size = sample_size
        self.learner = learner
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.results = {}

    def train_predict(self):
        start = time()
        self.learner = self.learner.fit(self.X_train[:int(self.sample_size)], self.y_train[:int(self.sample_size)])
        end = time()
        self.results['train_time'] = end - start

        start = time()
        predictions_train = self.learner.predict(self.X_train)
        predictions_test = self.learner.predict(self.X_test)
        end = time()
        self.results['pred_time'] = end - start

        self.results['acc_training'] = accuracy_score(self.y_train, predictions_train)
        self.results['acc_test'] = accuracy_score(self.y_test, predictions_test)

        self.results['f_train'] = fbeta_score(self.y_train, predictions_train, average='macro', beta=0.5)
        self.results['f_test'] = fbeta_score(self.y_test, predictions_test, average='macro', beta=0.5)

        self.results['precision_train'] = precision_score(self.y_train, predictions_train, average='macro')
        self.results['precision_test'] = precision_score(self.y_test, predictions_test, average='macro')

        self.results['recall_train'] = recall_score(self.y_train, predictions_train, average='macro')
        self.results['recall_test'] = recall_score(self.y_test, predictions_test, average='macro')

    # Getters
    def get_results(self):
        return self.results







