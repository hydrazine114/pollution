import lightgbm as lgb
from sklearn.preprocessing import OrdinalEncoder
import warnings
import joblib
warnings.filterwarnings("ignore")
from tqdm import tqdm
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class GbCV:
    def __init__(self, 
                frozen_parameters = None, 
                searched_parameters = None,
                num_search = 100):
        """_summary_

        Args:
            frozen_parameters (_type_, optional): _description_. Defaults to None.
            searched_parameters (_type_, optional): _description_. Defaults to None.
            num_search (int, optional): _description_. Defaults to 100.
        """
        
        if frozen_parameters is None:
            self.frozen_parameters = {'objective':'regression',
                                     'metric': 'rmse',
                                     'num_boost_round': 4096, 'verbose':-1}
        else:
            self.frozen_parameters = frozen_parameters
        
        if searched_parameters is None:
            self.searched_parameters = {'subsample': [0.4, 0.5, 0.6, 0.7], 'reg_lambda':[0, 1, 30, 50, 75, 100], 
                                    'reg_alpha': [0, 1, 10, 30, 50, 100], 'num_leaves': [63, 127, 511, 1023, 2047], 
                                    'min_child_weight': [1e-2, 1e-1, 1, 10], 'min_child_samples': [50], 
                                    'max_depth': [8, 12, 16, 20], 'learning_rate': [0.1, 0.25, 0.5, 1], 
                                    'colsample_bytree': [0.4, 0.5, 0.6]}
        else:
            self.searched_parameters = searched_parameters
        
        self.test_parameters = None
        self.random_parametres = None
        self.num_search = num_search
        self.results = []

    def _union_dict(self):
        self.test_parameters = dict()

        for key, value in self.frozen_parameters.items():
            self.test_parameters[key] = value

        for key, value in self.random_parametres.items():
            self.test_parameters[key] = value


    def _gen_random_parametres(self):
        self.random_parametres = dict()
        for i, j in self.searched_parameters.items():
            self.random_parametres[i] = np.random.choice(j)
    

    def _search_best_parametres(self):
        train_data = lgb.Dataset(self.X, self.y)
        for cnt in tqdm(range(self.num_search)):
            self._gen_random_parametres()
            self._union_dict()
            info = lgb.cv(self.test_parameters, train_data, stratified=False, 
                          callbacks = [lgb.early_stopping(stopping_rounds=10, verbose=False)])
            
            dft = pd.DataFrame([self.test_parameters], index=[cnt])
            dft['rmse'] = min(info['rmse-mean'])
            self.results.append(dft)

        self.results = pd.concat(self.results)
        self.results = self.results.sort_values('rmse', ascending=True)

    def fit(self, X, y, n_models=10):
        self.X = X
        self.y = y

        self._search_best_parametres()
        kf = KFold(n_splits=n_models)
        kf.get_n_splits(self.X)

        self.models = []
        self.rmse = []
        for i, (train_index, test_index) in enumerate(kf.split(self.X)):
            X_train = self.X.iloc[train_index, :]
            X_test = self.X.iloc[test_index, :]
            y_train = self.y.values[train_index]
            y_test = self.y.values[test_index]

            X_train, X_valid, y_train, y_valid = train_test_split(
                    X_train, y_train, test_size=0.1, random_state=42)

            train_data = lgb.Dataset(X_train, y_train)
            valid_data = lgb.Dataset(X_valid, y_valid, reference=train_data)

            params = dict(self.results.iloc[i, 1:-1])
            bst = lgb.train(params, train_data, valid_sets=[valid_data], 
            callbacks = [lgb.early_stopping(stopping_rounds=10)])
            predictions = bst.predict(X_test)
            self.rmse.append(mean_squared_error(y_test, predictions, squared=False))
            self.models.append(bst)
    
    
    def predict(self, X):
        predictions = []
        for bst in self.models:
            prediction = bst.predict(X)
            predictions.append(prediction)
        return np.mean(predictions, axis=0)
