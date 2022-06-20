from skmultiflow.trees import HoeffdingTreeClassifier

from ic.models import common

if __name__ == "__main__":
    common.main(HoeffdingTreeClassifier(), [0, 1])
