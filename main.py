from pydriller import Repository, Commit
from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError
from pandas import DataFrame
import datetime
from time import sleep
from NodeMaker import NodeMaker
from Utils import Utils
from neo.Neo4jConnection import Neo4jConnection

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = 0
    limit = 300
    end = start + limit

    conn = Neo4jConnection(uri="bolt://localhost:11010",
                           user="neo4j",
                           pwd="password",
                           db="testingDatabase")
    node_maker = NodeMaker(conn)

    node_maker.make_contraint()
    for commit in Repository('tensorflow/', order='reverse').traverse_commits():
        start += 1
        if start > end:
            break

        node_maker.make_commit_node(commit)graph

        node_maker.make_person_node(commit.author.email)
        node_maker.link_nodes_bidirectional(node_maker.COMMIT, commit.hash, node_maker.LINK_WAS_AUTHORED_BY,
                                            node_maker.PERSON, commit.author.email, node_maker.LINK_WRITTEN_BY)

        node_maker.make_person_node(commit.committer.email)
        node_maker.link_nodes(node_maker.PERSON, commit.committer.email, node_maker.LINK_COMMITTED,
                              node_maker.COMMIT, commit.hash)

        for branch in commit.branches:
            node_maker.make_branch(branch)

            node_maker.link_nodes(node_maker.COMMIT, commit.hash, node_maker.LINK_BRANCH,
                                  node_maker.BRANCH, branch)

        for mod_file in commit.modified_files:
            node_maker.make_mod_files(mod_file.new_path)
            node_maker.link_nodes(node_maker.COMMIT, commit.hash, node_maker.LINK_MODIFYIED,
                                  node_maker.MOD_FILES, mod_file.new_path)

        for parent in commit.parents:
            node_maker.make_commit_node(parent)
            node_maker.link_nodes_bidirectional(node_maker.COMMIT, commit.hash, node_maker.LINK_CHILD,
                                                node_maker.COMMIT, parent, node_maker.LINK_PARENT)

        print(f"{start} - {commit.hash}")
        sleep(1)

        break