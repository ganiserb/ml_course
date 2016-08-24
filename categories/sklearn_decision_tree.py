import json
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline


def load_data(path):
    return [json.loads(line) for line in open(path)]


if __name__ == "__main__":
    train = load_data("mlm_items_train.jsonlines")
    test = load_data("mlm_items_test.jsonlines")

    vectorizer = CountVectorizer()

    X = vectorizer.fit_transform([item['title'] for item in train])
    y = np.array([item['top_level_category'] for item in train])

    c = DecisionTreeClassifier()

    row_count, _ = X.shape

    kfold = cross_validation.KFold(row_count, n_folds=3, shuffle=True)
    a = [c.fit(X[train], y[train]).score(X[test], y[test])
         for train, test in kfold]

    print(a)

