import csv
import time

import joblib
import pandas as pd
import river
from sklearn.metrics import precision_score, recall_score, accuracy_score, confusion_matrix

from ic.models.common import process_row
from ic import util

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

def step_to_dataframe(evaluation_step):
    return pd.DataFrame({
        'accuracy': evaluation_step['Accuracy'].get(),
        'recall': evaluation_step['Recall'].get(),
        'precision': evaluation_step['Precision'].get(),
        'f1': evaluation_step['F1'].get(),
    }, index=[evaluation_step['Step']])


def evaluate_prequential_delayed(
    model, stream, delay=500, eval_step=500
):
    metrics = river.metrics.base.Metrics(
        metrics=[
            river.metrics.Accuracy(),
            river.metrics.Recall(),
            river.metrics.Precision(),
            river.metrics.F1()
        ]
    )

    step_iterator = river.evaluate.iter_progressive_val_score(
        model=model,
        dataset=stream,
        metric=metrics,
        step=eval_step,
        delay=delay
    )

    metrics_df = pd.DataFrame()

    for step in step_iterator:
        metrics_df = pd.concat([metrics_df, step_to_dataframe(step)])

    return metrics_df


def metrics_to_dataframe(step, metrics):
    return pd.DataFrame(dict(
        zip(
            ['accuracy', 'recall', 'precision', 'f1'],
            [ [ m.get() ] for m in metrics ]
        )
    ), index=[step])


def warm_up_and_evaluate(model, stream, n_warm_up_rows=1000):
    for _ in range(n_warm_up_rows):
        X, y = next(stream)
        model.learn_one(X, y)

    return evaluate_prequential_delayed(model, stream)


def process_evaluation(
    model,
    label,
    file_path,
    out_data_prefix='2022_08_01'
):
    out_path = f'../../data/{out_data_prefix}/metrics/{util.basename(file_path)}.{label}.metrics.csv'
    stream = util.yield_dataset(file_path, target='Label')

    start_time = time.time()
    h_m = time.strftime('%H:%M')
    print(f'Starting {label} - {h_m}')

    metrics = warm_up_and_evaluate(model, stream)
    metrics.to_csv(out_path, index_label='step')

    print(f'Took {int((time.time()-start_time)/60)} mins\n')

    model_out_path = f'../../trained_models/{out_data_prefix}/{label}_{util.basename(file_path)}.joblib'
    joblib.dump(model, model_out_path)
