import json
import sys
from itertools import islice
from statistics import mean
from random import shuffle


def draw_ascii_image(image):
    lines = []
    it = iter(image)
    for _ in range(28):
        line = []
        for b in islice(it, 28):
            if b < 80:
                c = "."
            elif b < 160:
                c = "*"
            else:
                c = "#"
            line.append(c * 2)
        lines.append("".join(line) + '|')
    return lines

def build_prediction(train, test):
    """
    Edit here. Should return one prediction for each element in test.
    """
    shuffle(train)
    total = len(train)
    test_size = int(0.1 * total)
    train_size = total - test_size
    test = train[train_size:]
    train = train[0:train_size]

    digits = {}
    average_digits = {}

    # Pack all the arrays of each digit into a dict
    # for number in range(10):
    #     digits[number] = [digit['image'] for digit in train if digit['label'] == str(number)]
    #
    # # Calculate an average matrix for each digit
    # for number in range(10):
    #     average_digits[number] = []
    #     # Put all bytes of the same position into one list for each
    #     for bytes in zip(*digits[number]):
    #         # value = 255 if mean(bytes) > 160 else 0  # Make this sort of black and white
    #         value = mean(bytes)
    #         average_digits[number].append(value)
    #
    # with open('average_digits.json', 'w') as file:
    #     json.dump(average_digits, file)

    with open('average_digits.json', 'r') as file:
        average_digits = json.load(file)
    # print(average_digits)

    result = []
    corrects = 0
    for sample in test:

        # Compute the differences between the sample and the average numbers
        digit_differences = dict()
        for number in range(10):
            # The following list comprehension computes the difference for all bytes
            differences = [abs(sample_byte - average)
                           for sample_byte, average in zip(sample['image'], average_digits[str(number)])]
            # At this point we have an array of differences for each byte
            # Now store the total difference for this number:
            # This represents how different the sample is from the average representation of the number
            digit_differences[number] = sum(differences)

        # Get the representation that is least different
        guess = str(min(digit_differences, key=digit_differences.get))
        if sample['label'] == str(guess):
            corrects += 1

        result.append(guess)

        # sample_image = draw_ascii_image(sample['image'])
        # average_image = draw_ascii_image(average_digits[guess])
        #
        # for sample_line, average_line in zip(sample_image, average_image):
        #     print(sample_line + average_line)

    print(corrects / len(test))

    return result


def load_data(path):
    return [json.loads(line) for line in open(path)]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit('Incorrect parameters. Only outfile needs to be provided')
    train = load_data("digits_train.jsonlines")
    test = None # load_data("digits_test.jsonlines")
    prediction = build_prediction(train, test)
    with open(sys.argv[1], "wt") as out:
        for x, label in zip(test, prediction):
            d = {
                "id": x["id"],
                "prediction": label
            }
            out.write(json.dumps(d))
            out.write("\n")
