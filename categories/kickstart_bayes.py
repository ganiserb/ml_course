import json
import sys

from collections import Counter
from decimal import Decimal


def build_prediction(train, test):
    """
    Edit here. Should return one prediction for each element in test.
    """
    data = dict()  # We use this to get statistics
                   # key is a category name, value is a list
                   # of all the words encountered in that category
                   # The sum of the data.values() dict
                   # is a list of all the words in the training set

    for thing in train:
        # With each thing published build statistics

        category_name = thing['top_level_category']
        title = thing['title']

        category_data = data.get(category_name)
        if not category_data:
            # First time we see it we initialize the word list
            data[category_name] = []

        data[category_name] += title.split()

    global_count = Counter(sum(data.values(), []))
    category_count = dict()  # key is a category, value a Counter dict
    category_word_prob = dict()

    for name, word_list in data.iteritems():
        category_count[name] = Counter(word_list)
        category_word_prob[name] = dict()
        for word, count in category_count[name].iteritems():
            category_word_prob[name][word] = Decimal(count) / Decimal(len(data[name]))

    # this is just the probability of choosing a random category
    category_prob = Decimal(1) / Decimal(len(data.keys()))

    # Now calculate the probability of occurrence of each word, per category
    # print category_word_prob
    # print category_count[data.keys()[0]]

    # Find the category with the most similar words present in the test title
    result = []
    for thing in test:
        title_words = thing['title'].split()

        for word in title_words:
            for category_name in data.keys():
                # Calculate the probability of this category being the
                # correct one given this word in the title
                # P(c|w) = (P(w|c) * P(c)) / P(w)
                word_prob = Decimal(1) / Decimal(len(data[category_name]))
                prob = (category_word_prob[category_name][word] * category_prob) / word_prob
                # TODO


    #     coincidences = dict()
    #     words = thing['title'].split()
    #     long_words = set([word for word in words if len(word) > 3])
    #
    #     for category, words in categories.iteritems():
    #         word_set = set(words)
    #         word_set.intersection(long_words)
    #         coincidences[category] = len(word_set)
    #
    #     most = 0
    #     cat = coincidences.keys()[0]
    #     for category, coincidences in coincidences.iteritems():
    #         if coincidences > most:
    #             most = coincidences
    #             cat = category
    #
    #     # the chosen prediction
    #     result.append(cat)

    return result


def load_data(path):
    return [json.loads(line) for line in open(path)]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit('Incorrect parameters. Only outfile needs to be provided')
    train = load_data("mlm_items_train.jsonlines")
    test = load_data("mlm_items_test.jsonlines")
    prediction = build_prediction(train, test)
    with open(sys.argv[1], "wt") as out:
        for x, label in zip(test, prediction):
            d = {
                "id": x["id"],
                "prediction": label
            }
            out.write(json.dumps(d))
            out.write("\n")
