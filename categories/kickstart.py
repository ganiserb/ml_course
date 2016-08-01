import json
import sys

from collections import Counter


def build_prediction(train, test):
    """
    Edit here. Should return one prediction for each element in test.
    """
    categories = dict()
    for thing in train:
        # For each thing published
        category_name = thing['top_level_category']
        category_data = categories.get(category_name)

        if not category_data:
            # First time we see it we initialize the counter
            categories[category_name] = Counter()

        title = thing['title']

        # Get a list of words in the title that are more than 3 chars long
        # and count them
        words = title.split()
        long_words = [word for word in words if len(word) > 3]
        word_count = Counter(long_words)

        # Update the count of each word in the category
        # with the ones on this thing
        categories[category_name].update(word_count)

    print len(categories.keys())

    # Leave only the 50 most common words of each category
    clean_categories = dict()
    for category_name, value in categories.iteritems():
        clean_categories[category_name] = value.most_common(50)

    # Find the category with the most similar words present in the test title
    result = []
    for thing in test:
        coincidences = dict()
        words = thing['title'].split()
        long_words = set([word for word in words if len(word) > 3])

        for category, words in categories.iteritems():
            word_set = set(words)
            word_set.intersection(long_words)
            coincidences[category] = len(word_set)

        most = 0
        cat = coincidences.keys()[0]
        for category, coincidences in coincidences.iteritems():
            if coincidences > most:
                most = coincidences
                cat = category

        # the chosen prediction
        result.append(cat)

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
