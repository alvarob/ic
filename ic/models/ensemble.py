import sys

import joblib

class Ensemble:
    def __init__(self, joblib_paths):
        self.models = [
            joblib.load(file_path) for file_path in joblib_paths
        ]

    def predict(self, vector):
        for model in self.models:
            try:
                if model.predict(vector)[0]:
                    return [1]
            except:
                pass

        return [0]
