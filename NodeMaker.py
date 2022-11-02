from neo4j.exceptions import ConstraintError
from pydriller import Commit

from Utils import Utils


class NodeMaker:
    LINK_WAS_AUTHORED_BY = "WAS_AUTHORED_BY"
    LINK_WRITTEN_BY = "WRITTEN_BY"
    LINK_COMMITTED = "COMMITED"
    LINK_BRANCH = "IN_BRANCH"
    LINK_MODIFYIED = "MODIFYED"
    LINK_CHILD = "CHILD"
    LINK_PARENT = "PARENT"

    COMMIT = "Commit"
    PERSON = "Person"
    BRANCH = "Branch"
    MOD_FILES = "ModFiles"

    def __init__(self, conn):
        self.__conn = conn

    def make_contraint(self):
        self.__conn.query('CREATE CONSTRAINT commit IF NOT EXISTS ON (a:Commit) ASSERT a.id IS UNIQUE')
        self.__conn.query('CREATE CONSTRAINT person IF NOT EXISTS ON (a:Person) ASSERT a.id IS UNIQUE')
        self.__conn.query('CREATE CONSTRAINT branch IF NOT EXISTS ON (a:Branch) ASSERT a.id IS UNIQUE')
        self.__conn.query('CREATE CONSTRAINT modfil IF NOT EXISTS ON (a:ModFiles) ASSERT a.id IS UNIQUE')

    def make_props_string(self, props: dict):
        if props is None:
            return ""

        props_string = " { "
        key = list(props.keys())[0]
        props_string += f"{key}: \"{props.get(key)}\""

        for i in range(1, len(props.keys())):
            key = list(props.keys())[i]
            props_string += f" , {key}: \"{props.get(key)}\""

        props_string += " } "
        return props_string

    def make_node(self, node_type, node_id, props=None):
        props_string = self.make_props_string(props)
        try:
            if props is None:
                self.__conn.query(f"""create (a:{node_type}) set a.id = '{node_id}' """)
            else:
                self.__conn.query(f"""create (a:{node_type} {props_string}) set a.id = '{node_id}' """)
        except ConstraintError as e:
            print("Node already exists " + node_id)
            pass

    def make_commit_node(self, commit: Commit):
        commit_dict = Utils.make_commit_dict(commit)
        self.make_node(self.COMMIT, commit.hash, commit_dict)

    def make_person_node(self, name: str):
        self.make_node(self.PERSON, name)

    def make_branch(self, name: str):
        self.make_node(self.BRANCH, name)

    def make_mod_files(self, name: str):
        self.make_node(self.MOD_FILES, name)

    def link_nodes(self, node_type_1, node_type_1_id, link_name, node_type_2, node_type_2_id):
        self.__conn.query(
            f"""match (a:{node_type_1}), (b:{node_type_2}) 
        where a.id = '{node_type_1_id}' and b.id = '{node_type_2_id}' 
        create (a)-[r:{link_name}]->(b)""")

    def link_nodes_bidirectional(self, node_type_1, node_type_1_id, link_name_1, node_type_2, node_type_2_id,
                                 link_name_2):
        self.link_nodes(node_type_1, node_type_1_id, link_name_1, node_type_2, node_type_2_id)
        self.link_nodes(node_type_2, node_type_2_id, link_name_2, node_type_1, node_type_1_id)
