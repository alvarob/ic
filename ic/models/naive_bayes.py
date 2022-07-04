from sklearn.naive_bayes import GaussianNB

from ic.models.common import main, train_and_save as ts

if __name__ == "__main__":
    main(GaussianNB(), [0, 1])


def train_and_save(training_csv_path, out_model_path):
    ts(GaussianNB(), [0,1], training_csv_path, out_model_path)

