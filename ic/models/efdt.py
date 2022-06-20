import csv, sys

import joblib
from skmultiflow.trees import ExtremelyFastDecisionTreeClassifier

from ic.models.common import process_row


def train(training_csv_path):
    model = ExtremelyFastDecisionTreeClassifier()
    error_set = set()
    line_count = 0
    error_count = 0
    
    with open(training_csv_path) as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip header
        
        for row in csv_reader:
            line_count += 1
            try:
                (x, y) = process_row(row)
                model.partial_fit([x], y, [0, 1])
            except ValueError as e:
                error_count += 1
                error_set.add(str(e))
    print(error_count, "out of", line_count, "lines errored")
    print("errors:", error_set)
    return model


def main():
    training_csv_path = sys.argv[1]
    out_model_path = sys.argv[2]
    print(training_csv_path, out_model_path)

    model = train(training_csv_path)
    joblib.dump(model, out_model_path)

if __name__ == "__main__":
    main()
