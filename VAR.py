import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.stattools import adfuller

class VARModel:
    def __init__(self, data):
        self.data = data
        self.model = None
        self.results = None

    def check_stationarity(self, threshold=0.05):
        result = {}
        for name, column in self.data.items():  # Corrected from iteritems() to items()
            test_result = adfuller(column.dropna())  # Ensure column has no NaN values
            result[name] = {'ADF Statistic': test_result[0], 'p-value': test_result[1]}
        return result

    def fit(self, maxlags=None, ic='aic'):
        self.model = VAR(self.data)
        self.results = self.model.fit(maxlags=maxlags, ic=ic)
        return self.results

    def forecast(self, steps):
        lag_order = self.results.k_ar
        return self.results.forecast(self.data.values[-lag_order:], steps=steps)

    def summary(self):
        return self.results.summary()

