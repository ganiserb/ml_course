import json
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation


def load_data(path):
    return [json.loads(line) for line in open(path)]


if __name__ == "__main__":
    train = load_data("digits_train.jsonlines")
    test = load_data("digits_test.jsonlines")

    X_train = np.array([sample["image"] for sample in train])
    y_train = np.array([sample["label"] for sample in train])

    c = DecisionTreeClassifier()

    kfold = cross_validation.KFold(len(X_train), n_folds=3, shuffle=True)
    a = [c.fit(X_train[train], y_train[train]).score(X_train[test], y_train[test])
         for train, test in kfold]

    print(a)

