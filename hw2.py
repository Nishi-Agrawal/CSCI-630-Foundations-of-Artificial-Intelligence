import random
import time

"""
Author: Nishi Pawan Agrawal
Program to implement a random-restart hill climbing algorithm that attempts to
find the expression that is as close as possible to the target. 
"""

def add_the_operators(list_of_expressions, the_list, target):
    """
    :param list_of_expressions: The expressions
    :param the_list: list of numbers
    :param target: the number that is required
    :return: difference from the target and the sum

    It finds the sum of the list of numbers that is provided
    and the distance of it from the target.
    """
    the_sum = 0
    number_at_one = the_list[1]

    if(number_at_one != 0):
        if (list_of_expressions[0] == 0):
            the_sum = the_list[0] + the_list[1]
        elif (list_of_expressions[0] == 1):
            the_sum = the_list[0] * the_list[1]
        elif (list_of_expressions[0] == 2):
            the_sum = the_list[0] / the_list[1]
        else:
            the_sum = the_list[0] - the_list[1]

    else:
        if(list_of_expressions[0] == 0):
            the_sum = the_list[0] + the_list[1]
        elif (list_of_expressions[0] == 1):
            the_sum = the_list[0] * the_list[1]
        else:
            the_sum = the_list[0] - the_list[1]

    for i in range(98):
        the_number = the_list[i+2]
        if(the_number != 0 and the_sum != 0):
            if (list_of_expressions[i+1] == 0):
                the_sum = the_sum + the_list[i+2]
            elif (list_of_expressions[i+1] == 1):
                the_sum = the_sum * the_list[i+2]
            elif (list_of_expressions[i+1] == 2):
                the_sum = the_sum / the_list[i+2]
            else:
                the_sum = the_sum - the_list[i+2]

        else:
            if(list_of_expressions[i+1] == 0):
                the_sum = the_sum + the_list[i + 2]
            elif (list_of_expressions[i+1] == 1):
                the_sum = the_sum * the_list[i+2]
            else:
                the_sum = the_sum - the_list[i + 2]

    difference_from_target = abs(target - the_sum)

    return difference_from_target, the_sum


def swap(the_list, list_of_expressions, difference_from_target, target):
    """

    :param the_list: the list of numbers
    :param list_of_expressions: the list of expressions
    :param difference_from_target: the distance from the target
    :param target: the target that is to be achieved
    :return: the difference from the target and the least sum

    It finds a value whose difference is less than the previous difference value
    up to 12 iterations and also prints the result.
    """
    least_sum = 0
    for i in range(len(the_list)):
        for j in range(len(the_list)):
            the_list[i], the_list[j] = the_list[j], the_list[i]
            new_difference, the_sum = add_the_operators(list_of_expressions, the_list, target)
            count1 = 0
            if count1 < 12:
                if(new_difference < difference_from_target):
                    difference_from_target = new_difference
                    least_sum = the_sum
                    count1 += 1
                    new_list = []
                    for i in range(len(the_list) - 1):
                        new_list.append(str(the_list[i]))
                        if (list_of_expressions[i] == 0):
                            new_list.append("+")
                        elif (list_of_expressions[i] == 1):
                            new_list.append("*")
                        elif (list_of_expressions[i] == 2):
                            new_list.append("/")
                        else:
                            new_list.append("-")
                        #new_list.append(list_of_expressions[i])
                    new_list.append(str(the_list[i+1]))
                    print("Best State")
                    print("".join(new_list))
                    print("Distance from target", difference_from_target)
                    print("")
                # print(str(new_list))

    return difference_from_target, least_sum

def init():
    """
    It runs for up to 3 durations. The duration has been set to 5
    seconds for each iteration. It is also used to find the list of numbers
    and expressions and also keeps track of the least value that is calculated.
    :return: None
    """
    for _ in range(3):
        the_list = [random.randrange(0, 10) for _ in range(100)]
        list_of_expressions = [random.randrange(0, 4) for _ in range(99)]
        target = 4350
        print("Number Set: ", the_list )
        print("Target: ", target)
        start = time.time()
        count = 0
        least_distance = float('inf')
        while(time.time() - start <= 5):
            print("Iteration: ", count)
            difference_from_target, the_sum = add_the_operators(list_of_expressions, the_list, target)
            new_list = []
            for i in range(len(the_list) - 1):
                new_list.append(str(the_list[i]))
                if (list_of_expressions[i] == 0):
                    new_list.append("+")
                elif (list_of_expressions[i] == 1):
                    new_list.append("*")
                elif (list_of_expressions[i] == 2):
                    new_list.append("/")
                else:
                    new_list.append("-")
            new_list.append(str(the_list[i + 1]))
            print("S0")
            print("".join(new_list))
            print("Distance from target", difference_from_target)
            print("")
            new_difference, new_sum = swap(the_list, list_of_expressions, difference_from_target, target)
            if new_difference < least_distance:
                least_distance = new_difference
            print("Overall Best: ", least_distance)
            count = count + 1

if __name__ == '__main__':
    """
    The main program.
    """
    init()