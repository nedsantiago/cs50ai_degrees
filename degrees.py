# Project: CS50AI - Degrees
# Description:
# This project finds the degrees of separation between any two celebrities.
# Updates:
# * Add a heuristic to improve the speed of the algorithm
# * Update algorithm to an A* algorithm by considering the distance of each
#   node from the source

import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def goal_test(node, target):
    """This function checks if the current node is the target node"""

    return node.state == target


def heuristic(name: str):
    """This function serves as the heuristic function of this algorithm. Its heuristic
    compares the number of connections each person has and will prefer better connected
    people"""

    pass


def g(node):
    """This function calculates the cost fucnction. This goes hand-in-hand with the
    heuristic function as part of the A* algorithm."""

    pass


def list_path(node):
    """This function takes the current node and moves to the parent
    node until the action is None (which would mean the current node is the source). 
    It returns a list of tuples that show the actions taken to get to get from 
    source to target"""
    
    print(f"node.parent: {node.parent}")
    # initialize the list of paths with an empty path
    ls_path = []
    # while parent is not None (node is not source)
    while (node.action != None):
        # append the node's action to the list of path
        # print(f"current node: {node.state}")
        # print(f"current node action: {node.action}")
        # print(f"Current ls_path: {ls_path}")
        ls_path.append(node.action)
        # update the current node to the parent's node
        node = node.parent
        # print(f"Changed the node, now ls_path: {ls_path}")
    # when the source is found
    # reverse the list
    ls_path.reverse()
    # return the list of actions
    return ls_path


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.

    Breadth-First will be implemented first for simplicity
    """

    # inititalize node
    node = Node(state=source, parent=None, action=None)
    # initialize a queue frontier for a breadth-first search (BFS)
    frontier_queue = QueueFrontier()
    frontier_queue.add(node)
    # initialize an explored set
    explored_set = set()
    # begin an infinite loop
    while True:
        # if the frontier is empty
        if frontier_queue.empty():
            # then no connection, return None (as per CS50 specs)
            print(f"Frontier was empty, returning None")
            return None
        # remove node from frontier
        node = frontier_queue.remove()
        # if the current state is the goal
        if goal_test(node=node, target=target):
            # begin collecting the path to goal
            print(f"Found the goal, beginning path lister")
            return list_path(node)
        else:  # it is not the goal and need to look for possibilities
            # Expand Frontier: loop through possible nodes
            for person_id in neighbors_for_person(node.state):
                # if the connection is not a refernce to self
                if (person_id != node.state):
                    # add connection (node) to frontier
                    frontier_queue.add(Node(
                        state=person_id[1], 
                        parent=node,
                        action=person_id))
            # add node to explored set
            explored_set.add(node)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
