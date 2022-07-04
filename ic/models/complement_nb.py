from sklearn.naive_bayes import ComplementNB

from ic.models.common import main, train_and_save as ts


if __name__ == "__main__":
    main(ComplementNB(), [0, 1])

def train_and_save(training_csv_path, out_model_path):
    ts(ComplementNB(), [0,1], training_csv_path, out_model_path)
