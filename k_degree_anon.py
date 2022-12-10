import random
import time

from pydriller import Repository, Commit
from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError
from pandas import DataFrame
import datetime
from time import sleep
from NodeMaker import NodeMaker
from Utils import Utils
from neo.Neo4jConnection import Neo4jConnection

from pprint import pprint
from github import Github
import pandas as pd
import datetime
from dateutil import parser
from time import sleep
from dateutil import parser
import sys

if __name__ == '__main__':
    conn = Neo4jConnection(uri="bolt://localhost:11010",
                           user="neo4j",
                           pwd="password",
                           db="wildfly2015")
    node_maker = NodeMaker(conn)

    start = 0
    jump = 300

    k_degree = int(sys.argv[1])

    entity_type = [(node_maker.COMMIT, node_maker.MOD_FILES, node_maker.LINK_MODIFYIED)]

    for main_node, anony_node, link_type in entity_type:
        m_time = time.time()
        commit_nodes = node_maker.find_nodes(main_node, start, jump)

        degree_log = {}
        extra_nodes_degree = []

        while len(commit_nodes) != 0:
            l_s_time = time.time()
            commit_nodes = node_maker.find_nodes(main_node, start, jump)
            start += jump

            for commit in commit_nodes:
                s_time = time.time()

                mod_files = node_maker.find_node_with_relation(main_node, commit['id'], link_type)



                val = degree_log.get(len(mod_files), [])
                val.append({"x": commit['id'], 'y': [x['b'] for x in mod_files]})
                degree_log[len(mod_files)] = val




                e_time = time.time()
                print(f"commit - {commit['id']} time - {e_time - s_time}")

            # pprint(degree_log)
            l_e_time = time.time()
            print(f"time x - {l_e_time - l_s_time}")


        for key in degree_log.keys():
            print(f"degree {key} num {len(degree_log[key])}")

            if len(degree_log[key]) > k_degree:
                extra_nodes_degree.append(key)


        for key in degree_log.keys():
            print(f"degree {key} num {len(degree_log[key])}")

            if len(degree_log[key]) < k_degree:

                diff = k_degree - len(degree_log[key])
                count = 0
                r_deduct_node = None
                while count < len(extra_nodes_degree):
                    count += 1
                    r_deduct_node = random.choice(extra_nodes_degree)

                    if len(degree_log[r_deduct_node]) - diff > k_degree:
                        break

                # take this r, take diff number of nodes,
                for _ in range(diff):

                    if r_deduct_node != None:
                        random.shuffle(degree_log[r_deduct_node])
                        random_element = degree_log[r_deduct_node].pop()
                    if r_deduct_node == None:
                        raise Exception()
                        # create random element,
                        # of r degree
                        # create random_element of random r_deduct_node degree
                        r_deduct_node = random.choice(extra_nodes_degree)

                        # create random hash
                        # find random r_deduct_node nodes
                        # link them




                    print(f"key {key} radom {r_deduct_node}")

                    if r_deduct_node > key:
                        remove_nodes = r_deduct_node - key
                        print(f"Removing nodes {remove_nodes}")

                        for _ in range(remove_nodes):
                            removal_link_entity = random_element["y"][0]
                            print(f"remove id - {removal_link_entity['id']}")
                            # node_maker.delete_link_of_id(main_node, anony_node, link_type, removal_link_entity['id'])


                    elif r_deduct_node < key:
                        add_nodes =  key - r_deduct_node
                        print(f"adding nodes {add_nodes}")
                        total_node = node_maker.count_node(anony_node)
                        skipping_anony = random.randrange(0+add_nodes, total_node-add_nodes)
                        anony_nodes_set = node_maker.find_nodes(anony_node, skipping_anony, add_nodes)
                        for n in anony_nodes_set:
                            # node_maker.link_nodes(main_node, random_element['x'], link_type, anony_node, n['id'])
                            print(f"addding n {n}")

                        val = degree_log.get(key, [])
                        val.append(random_element)
                        degree_log[key] = val


        for key in degree_log.keys():
            print(f"degree {key} num {len(degree_log[key])}")

        m_e_time = time.time()
        print(f"entity {main_node} type - {anony_node} time - {m_e_time - m_time}")


    # this is outer loop level


# if node has more link than k,
# add them to extra pool
# remove them from current node links

# if node has less than k links, take from extra pool and then work ahead
# if extra pool is left