import csv, sys

import joblib

def process_row(row):
  y = [0 if row[-1] == "BENIGN" else 1]
  x = [ float(val) for val in
        [ row[5], *row[7:-1] ]
      ]
  return (x, y)

def train(
    training_csv_path, model, classes, process_f=process_row
):
    error_set = set()
    line_count = 0
    error_count = 0
    
    with open(training_csv_path) as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip header
        
        for row in csv_reader:
            line_count += 1
            try:
                (x, y) = process_f(row)
                model.partial_fit([x], y, classes)
            except ValueError as e:
                error_count += 1
                error_set.add(str(e))

    print(error_count, "out of", line_count, "lines errored")
    if len(error_set):
        print("errors:", error_set)

    return model


def main(model, classes, process_f=process_row):
    training_csv_path = sys.argv[1]
    out_model_path = sys.argv[2]
    print(training_csv_path, out_model_path)

    trained_model = train(training_csv_path, model, classes, process_f)
    joblib.dump(model, out_model_path)
