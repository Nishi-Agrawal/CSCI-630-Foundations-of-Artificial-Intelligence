"""
@author: Nishi Pawan Agrawal
"""

from PIL import Image
import sys
import os
import math
from queue import PriorityQueue

a_dict = {(248,148,18,255): (20, "Open Land"), (255,192,0,255) : (30,"Rough Meadow"),  (255,255,255,255): (40,"Easy movement forest"), (2,208,60,255): (50, "Slow run forest"), (2,136,40,255): (60,"Walk forest"),(5,73,24,255): (float('inf'),"Impassible vegetation"), (0,0,255,255): (float('inf'), "Lake"), (71,51,3,255): (1, "Paved road"), (0,0,0,255): (10, "Footpath"), (205,0,101,255): (float('inf'), "Out of bounds") }


class Node:
    """
    The node class consists of multiple slots
    """
    slots = 'rows', 'columns', 'elevation', 'color', 'parent', 'f', 'g'

    def __init__(self, rows, columns, elevation, color):
        self.rows = rows
        self.columns = columns
        self.elevation = elevation
        self.color = color
        self.parent = None
        self.f = 0
        self.g = float('inf')

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        return str(self.rows) + " " + str(self.columns)+" "+str(self.color)

def getInput():
    """
    This function is used to get the input from the system argyuments
    :return: All the arguments that are reveived from the user
    """

    terrain_image = sys.argv[1]
    elevation_file = sys.argv[2]
    path_file = sys.argv[3]
    season = sys.argv[4]
    output_image_filename = sys.argv[5]

    return terrain_image, elevation_file, path_file, season, output_image_filename

def process_image(terrain_image, elevation_file):
    """
    This is basically used to process the image.
    :param terrain_image: The image
    :param elevation_file: z axis for 3D distance
    :return:
    """

    map = []
    with Image.open(terrain_image) as the_image:
        px = the_image.load()
        columns, rows = the_image.size
        elevation = []

        with open(elevation_file) as file:
            for line in file:
                line = line.split()
                elevation.append(line[:columns])

        for row in range(rows):
            inner_list = []
            for column in range(columns):
                n = Node(row, column, elevation[row][column], a_dict[px[column, row]])
                inner_list.append(n)

            map.append(inner_list)

    return map

def reset(map):
    """
    This function is used to reset the map for each iteration
    :param map:
    :return:
    """
    rows = len(map)
    columns = len(map[1])

    for x in range(rows):
        for y in range(columns):
            map[x][y].parent = None
            map[x][y].f = 0
            map[x][y].g = float('inf')

def calculate_g(current_vertex, neighbor):
    """
    used to calculate the value of g
    :param current_vertex: the current vertex
    :param neighbor: the neighbor
    :return: int value of g(n)
    """
    euc_dist = calculate_heuristic(current_vertex, neighbor)
    get_pixel = (current_vertex.color[0] * (euc_dist/ 2)) + (neighbor.color[0] * ( euc_dist/ 2))
    return get_pixel

def calculate_heuristic(start_node, end_node):
    """
    This function is used to calculate the heuristic
    :param start_node: the starting node
    :param end_node: the ending node
    :return:
    """
    val_of_x = 10.29*(start_node.rows - end_node.rows)
    val_of_y = 7.55*(start_node.columns - end_node.columns)
    val_of_z = float(start_node.elevation) - float(end_node.elevation)
    return math.sqrt((val_of_x ** 2) + (val_of_y ** 2) + (val_of_z ** 2))

def call_a_star(path_file, map):
    """
    It is used to call a star multiple times
    :param path_file: the path file
    :param map: the graph
    :return: final path calculated
    """
    a_list = []
    with open(path_file) as file:
        for line in file:
            a_list.append(line.split())

    final_path = []
    for i in range(len(a_list) - 1):
        path = a_star(int(a_list[i][1]), int(a_list[i][0]), int(a_list[i+1][1]), int(a_list[i+1][0]), map)
        reset(map)
        final_path = final_path + path

    return final_path


def a_star(startx, starty, targetx, targety, map):
    open_list = PriorityQueue()
    closed = set()

    current_vertex = map[startx][starty]
    target = map[targetx][targety]
    h_start = calculate_heuristic(current_vertex, target)
    current_vertex.g = 0
    current_vertex.f = current_vertex.g + h_start

    while current_vertex.rows != target.rows or current_vertex.columns != target.columns:
        the_neighbors = generate_neigh(map, current_vertex.rows, current_vertex.columns)
        for i in range(len(the_neighbors)):
            if the_neighbors[i] not in closed :
                gn = current_vertex.g + calculate_g(current_vertex, the_neighbors[i])
                hn = calculate_heuristic(the_neighbors[i], target)
                fn = gn + hn
                if fn < the_neighbors[i].f or the_neighbors[i].f == 0:
                    the_neighbors[i].f = fn
                    the_neighbors[i].g = gn
                    the_neighbors[i].parent = current_vertex
                    open_list.put(the_neighbors[i])

        closed.add(current_vertex)
        current_vertex = open_list.get()

    path = []
    while current_vertex.parent is not None:
        path.append(current_vertex)
        current_vertex = current_vertex.parent
    path.append(current_vertex)
    path.reverse()
    return path

def generate_neigh(map, row, column):
    the_neighbors = []

    if row == 0:
        if column == 0:
            the_neighbors.append(map[row][column+1])
            the_neighbors.append(map[row+1][column])
            return the_neighbors

        elif column == 394:
            the_neighbors.append(map[row][column-1])
            the_neighbors.append(map[row+1][column])
            return the_neighbors

        else:
            the_neighbors.append(map[row][column-1])
            the_neighbors.append(map[row][column+1])
            the_neighbors.append(map[row+1][column])
            return the_neighbors

    elif row == 499:
        if column == 0:
            the_neighbors.append(map[row][column+1])
            the_neighbors.append(map[row-1][column])
            return the_neighbors

        elif column == 394:
            the_neighbors.append(map[row][column-1])
            the_neighbors.append(map[row-1][column])
            return the_neighbors

        else:
            the_neighbors.append(map[row][column-1])
            the_neighbors.append(map[row][column+1])
            the_neighbors.append(map[row-1][column])
            return the_neighbors

    elif column == 0 and (row != 0 or row != 499):
        the_neighbors.append(map[row-1][column])
        the_neighbors.append(map[row+1][column])
        the_neighbors.append(map[row][column+1])
        return the_neighbors

    elif column == 394 and (row != 0 or row != 499):
        the_neighbors.append(map[row-1][column])
        the_neighbors.append(map[row+1][column])
        the_neighbors.append(map[row][column-1])
        return the_neighbors

    else:
        the_neighbors.append(map[row][column+1])
        the_neighbors.append(map[row][column-1])
        the_neighbors.append(map[row-1][column])
        the_neighbors.append(map[row+1][column])
        return the_neighbors

def for_fall(map, terrain_image):
    for row in range(500):
        for column in range(395):
            if map[row][column].color[1] == "Easy movement forest":
                neighbors = generate_neigh(map, row, column)
                for n in neighbors:
                    if n.color[1] == "Paved road" or n.color[1] == "Footpath":
                        n.color = (15, "Leafy road")
                        with Image.open(terrain_image) as the_image:
                            the_image.putpixel((n.columns, n.rows), (255,0,0))

def water_edge_nodes(map):
    #iterate over graph, if terrain is lake, get all neighbors, if any one neighbor is not lake
    #then add that node to a list
    the_list = []
    for row in range(500):
        for column in range(395):
            if map[row][column].color[1] == "Lake":
                neighbors = generate_neigh(map, row, column)
                for n in neighbors:
                    if n.color[1] != "Lake":
                        the_list.append(map[row][column])
                        break

    return the_list

def get_2d_distance(start, current):
    x = current.rows - start.rows
    y = current.columns - start.columns

    return math.sqrt((x ** 2) + (y ** 2))

def findShortestPath(start, map):
    """
    Find the shortest path, if one exists, between a start and end vertex
    :param start (Vertex): the start vertex
    :param end (Vertex): the destination vertex
    :return: A list of Vertex objects from start to end, if a path exists,
        otherwise None
    """
    queue = []
    ice = []
    visited = set()
    queue.append(start)         # prime the queue with the start vertex
    current = start

    # Loop until either the queue is empty, or the end vertex is encountered
    while len(queue) > 0 and get_2d_distance(start, current) <= 7:
        current = queue.pop(0)
        neighbors = generate_neigh(map, current.rows, current.columns)
        for neighbor in neighbors:
            if neighbor.color[1] == "Lake" and neighbor not in visited:
                ice.append(neighbor)
                queue.append(neighbor)
                visited.add(neighbor)

    return ice

def findShortestPathSpring(start, map):
    """
    Find the shortest path, if one exists, between a start and end vertex
    :param start (Vertex): the start vertex
    :param end (Vertex): the destination vertex
    :return: A list of Vertex objects from start to end, if a path exists,
        otherwise None
    """
    queue = []
    mud = []
    visited = set()
    queue.append(start)         # prime the queue with the start vertex
    current = start

    # Loop until either the queue is empty, or the end vertex is encountered
    while len(queue) > 0 and get_2d_distance(start, current) <= 15:

        current = queue.pop(0)
        neighbors = generate_neigh(map, current.rows, current.columns)
        for neighbor in neighbors:
            if neighbor not in visited and abs((float(current.elevation)) - (float(neighbor.elevation))) <= 1:
                mud.append(neighbor)
                queue.append(neighbor)
                visited.add(neighbor)

    return mud


def calc_path(the_path):
    the_cost = 0
    for i in range(len(the_path)-1):
        the_cost = the_cost + calculate_heuristic(the_path[i], the_path[i+1])

    print("The path: ", the_cost)

def work_for_season(season, map, terrain_image, im):

    if season == "winter":

        water_edge_list = water_edge_nodes(map)
        ice = []
        for i in range(len(water_edge_list)):
            ice += findShortestPath(water_edge_list[i], map)

        for a_node in ice:
            a_node.color = (15, "Ice")
            im.putpixel((ice[i].columns, ice[i].rows), (23, 221, 235))

    elif season == "fall":
        for_fall(map, terrain_image)

    elif season == "spring":
        mud_list = water_edge_nodes(map)
        mud= []
        for i in range(len(mud_list)):
            mud += findShortestPathSpring(mud_list[i], map)
            im.putpixel((mud_list[i].columns, mud_list[i].rows), (23,221,235))

        for a_node in mud:
            a_node.color = (1000, "Mud")


    else:
        pass

def main():
    terrain_image, elevation_file, path_file, season, output_image_filename = getInput()
    map = process_image(terrain_image, elevation_file)
    im = Image.open(terrain_image)
    work_for_season(season, map, terrain_image, im)
    the_path = call_a_star(path_file, map)
    calc_path(the_path)

    for i in the_path:
        im.putpixel((i.columns, i.rows), (255, 0, 0))
    im.save(output_image_filename)


if __name__ == '__main__':
    main()