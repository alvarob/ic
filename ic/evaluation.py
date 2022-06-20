import csv

import joblib
from sklearn.metrics import precision_score, recall_score, accuracy_score

from ic.models.common import process_row


def evaluate2(model_file, test_csv, process_f=process_row):
    model = joblib.load(model_file)

    y_test = []
    y_pred = []

    with open(test_csv, 'r', errors='ignore') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip header

        for row in csv_reader:
            try:
                (x, y) = process_f(row)

                prediction = model.predict([x])
                y_pred.append(prediction)
                y_test.append(y)
            except ValueError:
                pass

    return {
        "recall": recall_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "accuracy": accuracy_score(y_test, y_pred)
    }

def evaluate(model, test_csv, process_f=process_row):
    with open(test_csv, 'r', errors='ignore') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        true_positive_count = 0
        false_positive_count = 0
        true_negative_count = 0
        false_negative_count = 0
        total_count = 0
        correct_predictions = 0

        for row in csv_reader:
            try:
                (x, y) = process_f(row)
                prediction = model.predict([x])
                
                total_count += 1

                if y[0] != 0 and prediction[0] != 0:
                    correct_predictions += 1
                    true_positive_count += 1

                if y[0] == 0 and prediction[0] != 0:
                    false_positive_count += 1

                if y[0] == 0 and prediction[0] == 0:
                    correct_predictions += 1
                    true_negative_count += 1

                if y[0] != 0 and prediction[0] == 0:
                    false_negative_count += 1
            except:
                pass

        recall = 0
        try:
            recall = true_positive_count/(true_positive_count+false_negative_count)
        except ZeroDivisionError:
            pass

        precision = 0
        try:
            precision = true_positive_count/(true_positive_count+false_positive_count)
        except ZeroDivisionError:
            pass

        false_alarm_rate = 0
        try:
            false_alarm_rate = false_positive_count/(false_positive_count+true_negative_count)
        except ZeroDivisionError:
            pass

        return {
            "total_analyzed": total_count,
            "accuracy": correct_predictions/total_count,
            "recall": recall,
            "precision": precision,
            "false_alarm_rate": false_alarm_rate
        }

                    
                    
                
