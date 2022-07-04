from skmultiflow.trees import HoeffdingTreeClassifier

from ic.models import common


if __name__ == "__main__":
    common.main(HoeffdingTreeClassifier(), [0, 1])

    
def train_and_save(training_csv_path, out_model_path):
    common.train_and_save(
        HoeffdingTreeClassifier(), [0,1], training_csv_path, out_model_path
    )
