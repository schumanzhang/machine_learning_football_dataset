from train_model import TrainModel
from sklearn.metrics import accuracy_score, fbeta_score, precision_score, recall_score, make_scorer
from sklearn.model_selection import GridSearchCV

class SVMModel(TrainModel):

    def __init__(self, sample_size, learner, X_train, y_train, X_test, y_test, Cs, gammas, kernel):
        #TrainModel.__init__(self, sample_size, learner, X_train, y_train, X_test, y_test)
        super(SVMModel, self).__init__(sample_size, learner, X_train, y_train, X_test, y_test)
        self.Cs = Cs
        self.gammas = gammas
        self.kernel = kernel
        self.best_clf = learner

    def grid_search():
        parameters = [{'kernel': [self.kernel], 'C': self.Cs, 'gamma': self.gammas}]

        start = time()
        grid_obj = GridSearchCV(self.learner, parameters)
        grid_fit = grid_obj.fit(self.X_train, self.y_train)
        end = time()
        self.results['train_time'] = end - start

        self.best_clf = grid_fit.best_estimator_

        start = time()
        predictions_train = self.best_clf.predict(self.X_train)
        predictions_test = self.best_clf.predict(self.X_test)
        end = time()
        self.results['pred_time'] = end - start

        self.results['acc_training'] = accuracy_score(y_train, predictions_train)
        self.results['acc_test'] = accuracy_score(y_test, predictions_test)

        self.results['f_train'] = fbeta_score(y_train, predictions_train, average='macro', beta=0.5)
        self.results['f_test'] = fbeta_score(y_test, predictions_test, average='macro', beta=0.5)

        self.results['precision_train'] = precision_score(y_train, predictions_train, average='macro')
        self.results['precision_test'] = precision_score(y_test, predictions_test, average='macro')

        self.results['recall_train'] = recall_score(y_train, predictions_train, average='macro')
        self.results['recall_test'] = recall_score(y_test, predictions_test, average='macro')


