from train_model import TrainModel
from sklearn.metrics import accuracy_score, fbeta_score, precision_score, recall_score, make_scorer
from sklearn.model_selection import GridSearchCV
from time import time

class KNNModel(TrainModel):

    def __init__(self, sample_size, learner, X_train, y_train, X_test, y_test, k):
        #TrainModel.__init__(self, sample_size, learner, X_train, y_train, X_test, y_test)
        super(KNNModel, self).__init__(sample_size, learner, X_train, y_train, X_test, y_test)
        self.k = k
        self.best_clf = learner

    def grid_search(self):
        parameters = {'n_neighbors': self.k}

        start = time()
        grid_obj = GridSearchCV(self.learner, parameters)
        grid_fit = grid_obj.fit(self.X_train, self.y_train.values.ravel())
        end = time()
        self.results['train_time'] = end - start

        self.best_clf = grid_fit.best_estimator_

        start = time()
        predictions_train = self.best_clf.predict(self.X_train)
        predictions_test = self.best_clf.predict(self.X_test)
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
