import random

from pydriller import Repository, Commit
from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError
from pandas import DataFrame
import datetime
from time import sleep
from NodeMaker import NodeMaker
from Utils import Utils
from neo.Neo4jConnection import Neo4jConnection

from github import Github
import pandas as pd
import datetime
from dateutil import parser
from time import sleep
from dateutil import parser

if __name__ == '__main__':
    conn = Neo4jConnection(uri="bolt://localhost:11010",
                           user="neo4j",
                           pwd="password",
                           db="wildfly2015")
    node_maker = NodeMaker(conn)

    ANONYMITY_PERCENT = 20
    ANONYMOUS_NODE = [node_maker.PERSON]
    LEFT_TO_RIGHT = "left_to_right"
    RIGHT_TO_LEFT = "right_to_left"

    LINK_DEFINITION = {
        # write all the links that are present in the graph
        node_maker.PERSON: [
                            (node_maker.LINK_WAS_AUTHORED_BY, node_maker.COMMIT, RIGHT_TO_LEFT),
                            (node_maker.LINK_COMMITTED, node_maker.COMMIT, LEFT_TO_RIGHT),
                            (node_maker.LINK_WRITTEN_BY, node_maker.COMMIT, LEFT_TO_RIGHT),

                            (node_maker.LINK_REVIEWER, node_maker.PR, RIGHT_TO_LEFT),
                            (node_maker.LINK_APPROVER, node_maker.PR, RIGHT_TO_LEFT),]
    }

    total_people_nodes = node_maker.count_node(ANONYMOUS_NODE[0])
    number_to_change = int(ANONYMITY_PERCENT * total_people_nodes / 100)

    print(f"Total people {total_people_nodes} and random {number_to_change}")

    people_nodes = node_maker.find_nodes(ANONYMOUS_NODE[0], 0, 10000)
    people_nodes = [x['id'] for x in people_nodes]

    # make sure this is even
    random_select = random.sample(people_nodes, number_to_change)
    if len(random_select) % 2 == 1:
        random_select.append(random.sample(people_nodes, 1))

    # random_select = ["psotirop@redhat.com", "stefano.maestri@javalinux.it"]

    for i in range(0, len(random_select), 2):

        first_node_id = random_select[i]
        second_node_id = random_select[i+1]

        print(f"{first_node_id} to {second_node_id}")

        for el in LINK_DEFINITION[ANONYMOUS_NODE[0]]:
            link_type = el[0]
            link_entity = el[1]
            direction = el[2]


            # save links that first node has
            d_first_info = node_maker.find_node_with_relation(ANONYMOUS_NODE[0], first_node_id, link_type)

            # save links that second node has
            d_second_info = node_maker.find_node_with_relation(ANONYMOUS_NODE[0], second_node_id, link_type)

            # delte links both nodes have
            node_maker.delete_link(ANONYMOUS_NODE[0], first_node_id, link_type)
            node_maker.delete_link(ANONYMOUS_NODE[0], second_node_id, link_type)

            # assign first, second links
            for d_links in d_first_info:

                if direction == LEFT_TO_RIGHT:
                    type_1 = node_maker.PERSON
                    id_1 = second_node_id
                    type_2 = link_entity
                    id_2 = d_links['b']['id']
                else:
                    type_1 = link_entity
                    id_1 = d_links['b']['id']
                    type_2 = node_maker.PERSON
                    id_2 = second_node_id

                node_maker.link_nodes(type_1, id_1, link_type, type_2, id_2)


            # assign second, first links
            for d_links in d_second_info:

                if direction == LEFT_TO_RIGHT:
                    type_1 = node_maker.PERSON
                    id_1 = first_node_id
                    type_2 = link_entity
                    id_2 = d_links['b']['id']
                else:
                    type_1 = link_entity
                    id_1 = d_links['b']['id']
                    type_2 = node_maker.PERSON
                    id_2 = first_node_id

                node_maker.link_nodes(type_1, id_1, link_type, type_2, id_2)





