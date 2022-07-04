import csv

import joblib
from sklearn.metrics import precision_score, recall_score, accuracy_score, confusion_matrix

from ic.models.common import process_row


def evaluate_v2(model, test_csv, process_f=process_row):
    y_test = []
    y_pred = []
    error_count = 0
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
                error_count += 1

    conf_matrix = confusion_matrix(y_test, y_pred)
    (true_negative_count, false_positive_count), (false_negative_count, true_positive_count) = conf_matrix

    return {
        "recall": recall_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "accuracy": accuracy_score(y_test, y_pred),
        "false_alarm_rate": false_positive_count/(false_positive_count+true_negative_count),
        "confusion_matrix": conf_matrix,
        "lines_errored": error_count
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

                    
                    
                
