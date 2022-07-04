import collections, sys

import joblib


def any_pred(predictions):
    return [int(any(predictions))]


def majority(predictions):
    return [
        collections.Counter(predictions).most_common()[0][0]
    ]


class Ensemble:
    def __init__(self, joblib_paths, strategy=any_pred):
        self.models = [
            joblib.load(file_path) for file_path in joblib_paths
        ]
        self.strategy = strategy

    def predict(self, vector):
        predictions = []
        
        for model in self.models:
            predictions.append(model.predict(vector)[0])

        return self.strategy(predictions)
