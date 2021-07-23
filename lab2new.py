"""
@author: Nishi Pawan Agrawal
"""

import math
import random
import pickle
import sys

INPUT = []

class DecisionNode:
    __slots__ = 'leftTree', 'rightTree', 'words_en', 'words_nl', 'count', 'position'

    def __init__(self, leftTree, rightTree, column, position):
        self.leftTree = leftTree
        self.rightTree = rightTree
        self.count = get_label_count(column)
        self.words_en = self.count[0]
        self.words_nl = self.count[1]
        self.position = position

class Leaf:
    __slots__ = 'the_count'

    def __init__(self, column):
        self.the_count = get_label_count(column)

def getInput(datafile):
    with open(datafile) as file:
        for line in file:
            the_list = []
            line = line.split("|")
            the_list.append(feature_letter_q(line[1]))
            the_list.append(feature_letter_x(line[1]))
            the_list.append(feature_word_length(line[1]))
            the_list.append(feature_word_van(line[1]))
            the_list.append(feature_check_prepositions(line[1]))
            the_list.append(feature_conj_and(line[1]))
            the_list.append(feature_check_de_het(line[1]))
            the_list.append(line[0])

            INPUT.append(the_list)

def calculate_entropy(inputs, column):
    val_true = 0
    val_false = 0
    count = 0

    for i in range(len(inputs)):
        if inputs[i][column] is True or inputs[i][column] == "en":
            val_true += 1
            count += 1
        else:
            val_false += 1
            count += 1

    probability_true = val_true / count
    probability_false = val_false / count

    entropy = 0
    if probability_true > 0:
        entropy += probability_true * math.log(probability_true, 2)

    if probability_false > 0:
        entropy += probability_false * math.log(probability_false, 2)

    return -entropy

def information_gain(inputs, column):
    """
    inputs is the matrix and columns is the position
    :param inputs:
    :param column:
    :return:
    """
    left_true = []
    right_false = []

    for i in range(len(inputs)):
        if inputs[i][column] is True:
            left_true.append(inputs[i])
        else:
            right_false.append(inputs[i])

    probability_left = len(left_true) / (len(left_true) + len(right_false))
    probability_right = len(right_false) / (len(left_true) + len(right_false))

    entropy_target = calculate_entropy(inputs, 7)
    remainder = 0

    if len(left_true) != 0:
        entropy_left = calculate_entropy(left_true, 7)
    else:
        entropy_left = 0

    if len(right_false) != 0:
        entropy_right = calculate_entropy(right_false, 7)
    else:
        entropy_right = 0

    remainder += probability_left * entropy_left
    remainder += probability_right * entropy_right

    return (entropy_target - remainder)

def get_max_gain(inputs):
    gain = []

    for i in range(7):
        gain.append(information_gain(inputs, i))

    position = 0
    max = gain[0]
    for i in range(len(gain)):
        if gain[i] > max:
            max = gain[i]
            position = i

    return position, max

def dec_tree_helper(inputs):
    position, max = get_max_gain(inputs)

    column = []
    for i in range(len(inputs)):
        column.append(inputs[i][7])

    left_tree_true = []
    right_tree_false = []

    if max == 0:
        return Leaf(column)

    for i in range(len(inputs)):
        if inputs[i][position] is True:
            left_tree_true.append(inputs[i])
        else:
            right_tree_false.append(inputs[i])

    left_tree = dec_tree_helper(left_tree_true)
    right_tree = dec_tree_helper(right_tree_false)

    return DecisionNode(left_tree, right_tree, column, position)


def decision_tree():
    return dec_tree_helper(INPUT)

def get_label_count(a_list):

    """
    the count[0] has the count of 'en'
    and count[1] has the count of 'nl'
    :param a_list:
    :return:
    """

    count = []

    count_en = 0
    count_nl = 0

    for i in range(len(a_list)):
        if a_list[i] == "en":
            count_en += 1

        else:
            count_nl += 1

    count.append(count_en)
    count.append(count_nl)

    return count

def feature_letter_q(sentence):
    """
    returns true if the sentence is in English
    :param the_sentence:
    :return:
    """
    the_sentence = sentence.lower()
    q = "q"

    if q in the_sentence:
        return True
    return False


def feature_letter_x(sentence):
    """
    returns true if the sentence is in English
    :param the_sentence:
    :return:
    """
    the_sentence = sentence.lower()
    x = "x"

    if x in the_sentence:
        return True
    return False

def feature_word_length(the_sentence):
    """
    Average word length for a sentence in English is greater than
    5.
    :param the_sentence:
    :return: True if the average word length is greater than 5(English), false otherwise
    """

    words = the_sentence.split()
    average = sum(len(word) for word in words) / len(words)
    if average >= 5:
        return True
    return False

def feature_word_van(sentence):
    """
    The English script doesn’t have a word ‘van’ in most of the cases.
    But, in Dutch we use that word at a better frequency.
    :param the_sentence:
    :return:
    """

    the_sentence = sentence.lower().split()
    x = "van"

    if x in the_sentence:
        return True
    return False

def feature_check_prepositions(sentence):
    """
    The Dutch script doesn’t have a words 'a', 'an', 'the' in most of the cases.
    But, in English we use that word at a better frequency.
    :param the_sentence:
    :return:
    """
    the_sentence = sentence.lower().split()
    if "a" in the_sentence or "an" in the_sentence or "the" in the_sentence:
        return True
    return False

def feature_conj_and(sentence):
    """
    Here, we are looking for conjunctions in English like ‘and’ which doesn’t appear
    in the Dutch language.
    :param the_sentence:
    :return:
    """

    the_sentence = sentence.lower().split()

    if "and" in the_sentence:
        return True
    return False

def feature_check_de_het(sentence):
    """
    The English script doesn’t have words ‘de’, ‘het’ in most of the cases.
     But, in Dutch we use that words at a better frequency.
    :param the_sentence:
    :return:
    """
    the_sentence = sentence.lower().split()
    if "de" in the_sentence or "het" in the_sentence:
        return True
    return False

def adaboost():

    the_outputs = []

    for i in range(7):
        z = []
        INPUT_ADA, SAMPLE_WEIGHT, position = learn()
        target = []
        for k in range(len(INPUT_ADA)):
            target.append(INPUT_ADA[k][7])

        error = 0
        for j in range(len(INPUT_ADA)):
            if INPUT_ADA[j][i] != target[j]:
                error += SAMPLE_WEIGHT[j]
        for j in range(len(INPUT_ADA)):
            if INPUT_ADA[j][i] == target[j]:
                SAMPLE_WEIGHT[j] = SAMPLE_WEIGHT[j] * (error/ (1-error))
        normalize(SAMPLE_WEIGHT)
        if error == 0:
            z.append(float('inf'))
        elif error == 1:
            z.append(0)
        else:
            z.append(math.log(error/ (1-error)))
        the_outputs.append((INPUT_ADA, z, position))

    return the_outputs

def learn():
    INPUT_ADA = []
    SAMPLE_WEIGHT = []

    for i in range(len(INPUT)):
        SAMPLE_WEIGHT.append(1 / len(INPUT))

    temp_mat = []

    for i in range(len(SAMPLE_WEIGHT)):
        if i == 0:
            temp_mat.append(SAMPLE_WEIGHT[0])
        else:
            temp_mat.append(SAMPLE_WEIGHT[i] + temp_mat[i-1])

    for i in range(len(SAMPLE_WEIGHT)):
        temp = random.uniform(0, 1)
        j = 0
        while(temp_mat[j] < temp):
            j += 1
        INPUT_ADA.append(INPUT[j])

    position, max = get_max_gain(INPUT_ADA)

    return INPUT_ADA, SAMPLE_WEIGHT, position

def normalize(SAMPLE_WEIGHT):
    temp = 0
    for i in range(len(SAMPLE_WEIGHT)):
        temp = temp + SAMPLE_WEIGHT[i]

    for i in range(len(SAMPLE_WEIGHT)):
        SAMPLE_WEIGHT[i] = SAMPLE_WEIGHT[i] / temp

def classify(tuple, node):
    if isinstance(node, list):
        return ada_classify(tuple, node)
    else:
        if isinstance(node, Leaf):
            z = node.the_count
            if z[0] > z[1]:
                return 'en'
            else:
                return 'nl'
        else:
            if tuple[node.position] == True:
                return classify(tuple, node.leftTree)

            else:
                return classify(tuple, node.rightTree)

def ada_classify(tuple, node):
    nl_weight = 0
    en_weight = 0

    i = 0
    for val in node:
        if tuple[val[2]] == True:
            nl_weight += val[1][0]
            i += 1
        else:
            en_weight += val[1][0]
            i += 1

    if nl_weight < en_weight:
        return 'en'

    else:
        return 'nl'

def getOutput(data):
    testdata = []
    with open(data) as file:
        for line in file:
            the_list = []
            the_list.append(feature_letter_q(line))
            the_list.append(feature_letter_x(line))
            the_list.append(feature_word_length(line))
            the_list.append(feature_word_van(line))
            the_list.append(feature_check_prepositions(line))
            the_list.append(feature_conj_and(line))
            the_list.append(feature_check_de_het(line))
            testdata.append(the_list)

    return testdata


def main():
    val = input("Enter training data file name")
    getInput(val)
    the_type = input("Enter dt or ada")
    if the_type == 'dt':
        x = decision_tree()
        print("Decision Tree implementation successful!")
    else:
        x = adaboost()
        print("Adaboost implementation successful")

    output_file = input("Enter the name of the output file")
    objectFile = open(output_file, 'wb')
    pickle.dump(x, objectFile)

    test_file = input("Enter the name of the Testfile")
    test_data = getOutput(test_file)

    i = 1
    for tuple in test_data:
        print("line", i, "=", classify(tuple, x))
        i += 1

if __name__ == '__main__':
    main()