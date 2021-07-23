"""
Author: Nishi Pawan Agrawal
Program to change any single letter in the word to any other letter, provided
that the result is a word in the doctionary
"""

import sys
#list of words that are taken from the dictionary
words = []

#graph to iterate over
graph = dict()

#list pf wprds that are remaining to be added to the dictionary'
remaining_words = []

def find_matches(start_word):
    """
    if the word is not in the graph, then add it to the graph
    then find other words that the priginal word can be morphed into
    Keep appending the nodes to the list
    :param start_word: the start word
    :return: None
    """

    if start_word not in graph:
        graph[start_word] = list()
        for i in range(len(start_word)):
            for j in range(26):
                copy_start_word = start_word
                copy_start_word = copy_start_word[:i] + chr(97+j) + \
                                  copy_start_word[i+1:]
                if copy_start_word in words and copy_start_word not in graph[start_word]\
                        and copy_start_word != start_word and copy_start_word not in \
                        remaining_words and copy_start_word not in graph:
                    graph[start_word].append(copy_start_word)
                    remaining_words.append(copy_start_word)

    else:
        print("Word not found! i.e. no solution")

def findShortestPath(start, end):
    """
    Find the shortest path, if one exists, between a start and end vertex
    :param start (Vertex): the start vertex
    :param end (Vertex): the destination vertex
    :return: A list of Vertex objects from start to end, if a path exists,
        otherwise None
    """

    queue = []
    queue.append(start)         # prime the queue with the start vertex

    predecessors = {}
    predecessors[start] = None  # add the start vertex with no predecessor

    # Loop until either the queue is empty, or the end vertex is encountered
    while len(queue) > 0:
        current = queue.pop(0)
        if current == end:
            break
        for neighbor in graph[current]:
            if neighbor not in predecessors:        # if neighbor unvisited
                predecessors[neighbor] = current    # map neighbor to current
                queue.append(neighbor)              # enqueue the neighbor

    # If the end vertex is in predecessors a path was found
    if end in predecessors:
        path = []
        current = end
        while current != start:              # loop backwards from end to start
            path.insert(0, current)          # prepend current to the path list
            current = predecessors[current]  # move to the predecessor
        path.insert(0, start)
        return path
    else:
        return "No solution"

def takeInput():
    """
    Get the file from arguments and read it. Then call
    the find_matches function for the remaining words that are left.
    :return: None
    """

    file_name = str(sys.argv[1])
    start_word = str(sys.argv[2])
    end_word = str(sys.argv[3])
    if len(start_word) == len(end_word):
        with open(file_name) as reader:
            line = reader.readlines()
            for single_line in line:
                single_line = single_line.strip("\n")
                if len(single_line) == len(start_word):
                    words.append(single_line)

        find_matches(start_word)
        while len(remaining_words) != 0:
            the_word = remaining_words.pop(0)
            find_matches(the_word)

        value = findShortestPath(start_word, end_word)
        if value != "No solution":
            for i in range(len(value)):
                print(value[i])

        else:
            print(value)

    else:
        print("No solution")

def main():
    takeInput()

if __name__ == '__main__':
    main()
