# #!/usr/bin/env python
# # coding: utf-8
#
# # # Get the repo
#
# # # Commit
# # - l author (Developer): commit author (name, email)
# # - l committer (Developer): commit committer (name, email)
# # - l branches (List[str]): List of branches that contain this commit
# # - l modified_files (List[ModifiedFile]): list of modified files in the commit (see ModifiedFile)
# #     - p filename
# #     - p old_path: old path of the file (can be _None_ if the file is added)
# #     - p new_path: new path of the file (can be _None_ if the file is deleted)
# #     - p filename: return only the filename (e.g., given a path-like-string such as “/Users/dspadini/pydriller/myfile.py” returns “myfile.py”)
# #     - r change_type: type of the change: can be Added, Deleted, Modified, or Renamed.
# #     - p diff: diff of the file as Git presents it (e.g., starting with @@ xx,xx @@).
# #     - p diff_parsed: diff parsed in a dictionary containing the added and deleted lines. The dictionary has 2 keys: “added” and “deleted”, each containing a list of Tuple (int, str) corresponding to (number of line in the file, actual line).
# #     - r added_lines: number of lines added
# #     - r deleted_lines: number of lines removed
# #     - / source_code: source code of the file (can be _None_ if the file is deleted or only renamed)
# #     - / source_code_before: source code of the file before the change (can be _None_ if the file is added or only renamed)
# #     - l methods: list of methods of the file. The list might be empty if the programming language is not supported or if the file is not a source code file. These are the methods after the change.
# #     - / methods_before: list of methods of the file before the change (e.g., before the commit.)
# #     - / changed_methods: subset of _methods_ containing only the changed methods.
# #     - / nloc: Lines Of Code (LOC) of the file
# #     - / complexity: Cyclomatic Complexity of the file
# #     - / token_count: Number of Tokens of the file
# # - l parents (List[str]): list of the commit parents
# # - l project_name (str): project name
# # - p author_date (datetime): authored date
# # - p author_timezone (int): author timezone (expressed in seconds from epoch)
# # - p committer_date (datetime): commit date
# # - p committer_timezone (int): commit timezone (expressed in seconds from epoch)
# # - p project_path (str): project path
# # - p hash (str): hash of the commit
# # - p msg (str): commit message
# # - p deletions (int): number of deleted lines in the commit (as shown from –shortstat).
# # - p insertions (int): number of added lines in the commit (as shown from –shortstat).
# # - p lines (int): total number of added + deleted lines in the commit (as shown from –shortstat).
# # - p files (int): number of files changed in the commit (as shown from –shortstat).
# # - / dmm_unit_size (float): DMM metric value for the unit size property.
# # - / dmm_unit_complexity (float): DMM metric value for the unit complexity property.
# # - / dmm_unit_interfacing (float): DMM metric value for the unit interfacing property.
# # - / in_main_branch (Bool): True if the commit is in the main branch
# # - / merge (Bool): True if the commit is a merge commit
#
# # # Commit Refined
# # - l author (Developer): commit author (name, email)
# # - l committer (Developer): commit committer (name, email)
# # - l branches (List[str]): List of branches that contain this commit
# # - l modified_files (List[ModifiedFile]): list of modified files in the commit (see ModifiedFile)
# #     - p filename
# #     - p old_path: old path of the file (can be _None_ if the file is added)
# #     - p new_path: new path of the file (can be _None_ if the file is deleted)
# #     - p filename: return only the filename (e.g., given a path-like-string such as “/Users/dspadini/pydriller/myfile.py” returns “myfile.py”)
# #     - r change_type: type of the change: can be Added, Deleted, Modified, or Renamed.
# #     - p diff: diff of the file as Git presents it (e.g., starting with @@ xx,xx @@).
# #     - p diff_parsed: diff parsed in a dictionary containing the added and deleted lines. The dictionary has 2 keys: “added” and “deleted”, each containing a list of Tuple (int, str) corresponding to (number of line in the file, actual line).
# #     - r added_lines: number of lines added
# #     - r deleted_lines: number of lines removed
# #     - l methods: list of methods of the file. The list might be empty if the programming language is not supported or if the file is not a source code file. These are the methods after the change.
# # - l parents (List[str]): list of the commit parents
# # - l project_name (str): project name
# # - p author_date (datetime): authored date
# # - p author_timezone (int): author timezone (expressed in seconds from epoch)
# # - p committer_date (datetime): commit date
# # - p committer_timezone (int): commit timezone (expressed in seconds from epoch)
# # - p project_path (str): project path
# # - p hash (str): hash of the commit
# # - p msg (str): commit message
# # - p deletions (int): number of deleted lines in the commit (as shown from –shortstat).
# # - p insertions (int): number of added lines in the commit (as shown from –shortstat).
# # - p lines (int): total number of added + deleted lines in the commit (as shown from –shortstat).
# # - p files (int): number of files changed in the commit (as shown from –shortstat).
#
# # In[526]:
#
#
# class Neo4jConnection:
#
#     def __init__(self, uri, user, pwd):
#         self.__uri = uri
#         self.__user = user
#         self.__pwd = pwd
#         self.driver = None
#         try:
#             self.driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
#         except Exception as e:
#             print("Failed to create the driver:", e)
#
#     def close(self):
#         if self.driver is not None:
#             self.driver.close()
#
#     def query(self, query, parameters=None, db=None):
#         assert self.driver is not None, "Driver not initialized!"
#         session = None
#         response = None
#         try:
#             session = self.driver.session(database=db) if db is not None else self.driver.session()
#             response = list(session.run(query, parameters))
#         except Exception as e:
#             print("Query failed:", e)
#         finally:
#             if session is not None:
#                 session.close()
#         return response
#
#
# # conn = Neo4jConnection(uri="bolt://35.172.119.131:7687",
# #                        user="neo4j",
# #                        pwd="passages-instructions-efficiencies")
#
#
# # conn = Neo4jConnection(uri="bolt://localhost:11006",
# #                        user="neo4j",
# #                        pwd="password")
#
#
# conn = Neo4jConnection(uri="bolt://localhost:11010",
#                        user="neo4j",
#                        pwd="password")
#
# # In[511]:
#
#
# from pydriller import Repository, Commit
# from neo4j import GraphDatabase
# from neo4j.exceptions import ConstraintError
# from pandas import DataFrame
# import datetime
#
# COMMIT = "Commit"
# PERSON = "Person"
# BRANCH = "Branch"
# MOD_FILES = "ModFiles"
#
#
# # Create contraint
#
# # In[512]:
#
#
# def make_contraint():
#     conn.query('CREATE CONSTRAINT commit IF NOT EXISTS ON (a:Commit) ASSERT a.id IS UNIQUE')
#     conn.query('CREATE CONSTRAINT person IF NOT EXISTS ON (a:Person) ASSERT a.id IS UNIQUE')
#     conn.query('CREATE CONSTRAINT branch IF NOT EXISTS ON (a:Branch) ASSERT a.id IS UNIQUE')
#     conn.query('CREATE CONSTRAINT modfil IF NOT EXISTS ON (a:ModFiles) ASSERT a.id IS UNIQUE')
#
#
# # In[513]:
#
#
# def make_node(node_type, node_id):
#     try:
#         conn.query(f"""create (a:{node_type}) set a.id = '{node_id}' """)
#     except ConstraintError as e:
#         print("Node already exists " + node_id)
#         pass
#
#
# # In[514]:
#
#
# def make_commit_node(commit: str):
#     make_node(COMMIT, commit)
#
#
# # In[515]:
#
#
# def make_person_node(name: str):
#     make_node(PERSON, name)
#
#
# # In[516]:
#
#
# def make_branch(name: str):
#     make_node(BRANCH, name)
#
#
# # In[517]:
#
#
# def make_mod_files(name: str):
#     make_node(MOD_FILES, name)
#
#
# # In[518]:
#
#
# def link_nodes(node_type_1, node_type_1_id, link_name, node_type_2, node_type_2_id):
#     conn.query(
#         f"""match (a:{node_type_1}), (b:{node_type_2})
#     where a.id = '{node_type_1_id}' and b.id = '{node_type_2_id}'
#     create (a)-[r:{link_name}]->(b)""")
#
#
# # In[519]:
#
#
# def link_nodes_bidirectional(node_type_1, node_type_1_id, link_name_1, node_type_2, node_type_2_id, link_name_2):
#     link_nodes(node_type_1, node_type_1_id, link_name_1, node_type_2, node_type_2_id)
#     link_nodes(node_type_2, node_type_2_id, link_name_2, node_type_1, node_type_1_id)
#
#
# # In[520]:
#
#
# LINK_WAS_AUTHORED_BY = "WAS_AUTHORED_BY"
# LINK_WRITTEN_BY = "WRITTEN_BY"
# LINK_COMMITTED = "COMMITED"
# LINK_BRANCH = "IN_BRANCH"
# LINK_MODIFYIED = "MODIFYED"
# LINK_CHILD = "CHILD"
# LINK_PARENT = "PARENT"
#
# # In[522]:
#
#
# start = 0
# limit = 300
# end = start + limit
#
# make_contraint()
# for commit in Repository('tensorflow/', order='reverse').traverse_commits():
#     start += 1
#     if start > end:
#         break
#
#     make_commit_node(commit.hash)
#
#     make_person_node(commit.author.email)
#     link_nodes_bidirectional(COMMIT, commit.hash, LINK_WAS_AUTHORED_BY,
#                              PERSON, commit.author.email, LINK_WRITTEN_BY)
#
#     make_person_node(commit.committer.email)
#     link_nodes(PERSON, commit.committer.email, LINK_COMMITTED,
#                COMMIT, commit.hash)
#
#     for branch in commit.branches:
#         make_branch(branch)
#
#         link_nodes(COMMIT, commit.hash, LINK_BRANCH,
#                    BRANCH, branch)
#
#     for mod_file in commit.modified_files:
#         make_mod_files(mod_file.new_path)
#         link_nodes(COMMIT, commit.hash, LINK_MODIFYIED,
#                    MOD_FILES, mod_file.new_path)
#
#     for parent in commit.parents:
#         make_commit_node(parent)
#         link_nodes_bidirectional(COMMIT, commit.hash, LINK_CHILD,
#                                  COMMIT, parent, LINK_PARENT)
#
#     print(f"{start} - {commit.hash}")
#     sleep(1)
#
# # In[523]:
#
#
# print("done")
#
# # In[527]:
#
#
# number_of_commits = []
# number_of_commits = conn.query(f'''match (n:Person)-[r:WRITTEN_BY]-(b)  return n, count(r)''')
#
# # In[528]:
#
#
# number_of_commits
#
# # In[476]:
#
#
# number_of_commits[0]
#
# # In[581]:
#
#
# list_id = []
# for i in number_of_commits:
#     list_id.append(i.data()["n"]["id"])
#
# # In[582]:
#
#
# list_r = []
# for i in number_of_commits:
#     list_r.append(i.data()["count(r)"])
#
# # In[583]:
#
#
# name_changes = DataFrame(list(zip(list_id, list_r)),
#                          columns=['Name', 'Change'])
#
# # In[584]:
#
#
# name_changes.to_csv(f"anon_{datetime.datetime.today().timestamp()}.csv")
#
# # In[585]:
#
#
# name_changes["Change"].sum()
#
# # In[586]:
#
#
# len(list_id)
#
#
# # In[587]:
#
#
# def get_links_csv():
#     number_of_commits = []
#     number_of_commits = conn.query(f'''match (n:Person)-[r:WRITTEN_BY]-(b)  return n, count(r)''')
#     list_id = []
#     for i in number_of_commits:
#         list_id.append(i.data()["n"]["id"])
#     list_r = []
#     for i in number_of_commits:
#         list_r.append(i.data()["count(r)"])
#     name_changes = DataFrame(list(zip(list_id, list_r)),
#                              columns=['Name', 'Change'])
#     name_of_file = f"anon_{datetime.datetime.today().timestamp()}.csv"
#     name_changes.to_csv(name_of_file)
#     return name_of_file
#
#
# # In[597]:
#
#
# # delete x nodes
#
# ## find x nodes to delete
# ## find x nodes to replace
# ## change links
# ## delete nodes
#
# def delete_x_nodes(id_1, id_2):
#     related_commits_1 = get_linked_entities(PERSON, id_1, LINK_WRITTEN_BY, COMMIT)
#     related_commits_1_list = []
#     for commit in related_commits_1:
#         related_commits_1_list.append(commit.data()["b"]["id"])
#     delete_relation(PERSON, id_1, LINK_WRITTEN_BY, COMMIT)
#     delete_relation(PERSON, id_1, LINK_WAS_AUTHORED_BY, COMMIT)
#
#     for c in related_commits_1_list:
#         link_nodes_bidirectional(COMMIT, c, LINK_WAS_AUTHORED_BY,
#                                  PERSON, id_2, LINK_WRITTEN_BY)
#
#
# # In[589]:
#
#
# all_names = conn.query(f"""match (p:Person) return p""")
#
# # In[590]:
#
#
# len(all_names)
#
#
# # In[556]:
#
#
# def get_node(category):
#     things = conn.query(f"""match (p:{category}) return p""")
#     things_list = []
#     for thing in things:
#         things_list.append(thing.data()["p"]["id"])
#     return things_list
#
#
# # In[549]:
#
#
# # change links of x nodes
#
# ## find x1 nodes to find
# ## find x2 nodes to swap
# ## store link for x1 and delete them
# ## store link for x2 and delete them
# ## assign link of x2 to x1
# ## assign link of x1 to x2
#
#
# # In[ ]:
#
#
# def get_node(category):
#     things = conn.query(f"""match (p:{category}) return p""")
#     things_list = []
#     for thing in things:
#         things_list.append(thing.data()["p"]["id"])
#     return things_list
#
#
# # In[558]:
#
#
# all_person = get_node(PERSON)
#
# # In[559]:
#
#
# SWAP_NUMBER_OF_PEOPLE = 10
#
#
# # In[560]:
#
#
# def get_n_random(list_of_things, number):
#     random_set = []
#     while len(random_set) < number:
#         random_select = random.choice(list_of_things)
#         if random_select not in random_set:
#             random_set.append(random_select)
#     return random_set
#
#
# # In[563]:
#
#
# swap_candidates = get_n_random(all_person, SWAP_NUMBER_OF_PEOPLE * 2)
#
#
# # In[566]:
#
#
# def get_linked_entities(type_entity, id_1, relation_type, relation_entity):
#     related_commits_1 = conn.query(
#         f""" match (p:{type_entity} {{ id : '{id_1}' }} ) -[r:{relation_type}]-(b:{relation_entity})  return b""")
#     return related_commits_1
#
#
# # In[568]:
#
#
# def delete_relation(type_entity, id_1, alter_entity_relation, alter_entity_type):
#     conn.query(
#         f""" match (p:{type_entity} {{ id : '{id_1}' }} ) -[r:{alter_entity_relation}]-(b:{alter_entity_type}) delete r """)
#
#
# # In[576]:
#
#
# def swap_links(type_entity, id_1, id_2, alter_entity_relation, alter_entity_type):
#     related_commits_1 = get_linked_entities(type_entity, id_1, alter_entity_relation, alter_entity_type)
#     related_commits_1_list = []
#     for commit in related_commits_1:
#         related_commits_1_list.append(commit.data()["b"]["id"])
#     related_commits_2 = get_linked_entities(type_entity, id_2, alter_entity_relation, alter_entity_type)
#     related_commits_2_list = []
#     for commit in related_commits_2:
#         related_commits_2_list.append(commit.data()["b"]["id"])
#     delete_relation(type_entity, id_1, alter_entity_relation, alter_entity_type)
#     delete_relation(type_entity, id_1, LINK_WAS_AUTHORED_BY, alter_entity_type)
#     delete_relation(type_entity, id_2, alter_entity_relation, alter_entity_type)
#     delete_relation(type_entity, id_2, LINK_WAS_AUTHORED_BY, alter_entity_type)
#     for c in related_commits_1_list:
#         link_nodes_bidirectional(COMMIT, c, LINK_WAS_AUTHORED_BY,
#                                  PERSON, id_2, LINK_WRITTEN_BY)
#     for c in related_commits_2_list:
#         link_nodes_bidirectional(COMMIT, c, LINK_WAS_AUTHORED_BY,
#                                  PERSON, id_1, LINK_WRITTEN_BY)
#
#
# # In[580]:
#
#
# for i in range(0, SWAP_NUMBER_OF_PEOPLE * 2, 2):
#     print(i)
#
# # In[598]:
#
#
# for i in range(3):
#
#     print(f"{i} iteration")
#     print(get_links_csv())
#
#     swap_candidates = get_n_random(all_person, SWAP_NUMBER_OF_PEOPLE * 2)
#     for i in range(0, SWAP_NUMBER_OF_PEOPLE * 2, 2):
#         swap_links(PERSON, swap_candidates[i], swap_candidates[i + 1], LINK_WRITTEN_BY, COMMIT)
#
#     swap_candidates = get_n_random(all_person, SWAP_NUMBER_OF_PEOPLE * 2)
#     for i in range(0, SWAP_NUMBER_OF_PEOPLE * 2, 2):
#         delete_x_nodes(swap_candidates[i], swap_candidates[i + 1])
#
# # In[599]:
#
#
# print(get_links_csv())
#
# # In[ ]:
#
#
# # In[ ]:
#
#
# # In[572]:
#
#
# swap_candidates[0]
#
# # In[573]:
#
#
# swap_candidates[1]
#
# # In[578]:
#
#
# swap_links(PERSON, swap_candidates[0], swap_candidates[1], LINK_WRITTEN_BY, COMMIT)
#
# # In[ ]:
#
#
# # In[431]:
#
#
# # remove 1 random node, assign those links to someone else
#
#
# # In[432]:
#
#
# all_names = conn.query(f"""match (p:Person) return p""")
#
# # In[438]:
#
#
# all_names[0].data()["p"]["id"]
#
# # In[440]:
#
#
# all_names_list = []
# for name in all_names:
#     all_names_list.append(name.data()["p"]["id"])
#
# # In[441]:
#
#
# all_names_list
#
# # In[442]:
#
#
# import random
#
# # In[443]:
#
#
# random_delete = random.choice(all_names_list)
#
# # In[444]:
#
#
# random_assignee = random.choice(all_names_list)
#
# # In[445]:
#
#
# print(random_delete + " -> " + random_assignee)
#
# # In[451]:
#
#
# related_commits = conn.query(f""" match (p:Person {{ id : '{random_delete}' }} ) -[r:WRITTEN_BY]-(b)  return b""")
#
# # In[454]:
#
#
# related_commits[0].data()["b"]["id"]
#
# # In[456]:
#
#
# related_commits_list = []
# for commit in related_commits:
#     related_commits_list.append(commit.data()["b"]["id"])
#
# # In[457]:
#
#
# related_commits_list
#
# # In[458]:
#
#
# conn.query(f""" match (p:Person {{ id : '{random_delete}' }} ) -[r:WRITTEN_BY]-(b) detach delete p""")
#
# # In[459]:
#
#
# for commit in related_commits_list:
#     link_nodes_bidirectional(COMMIT, commit, LINK_WAS_AUTHORED_BY,
#                              PERSON, random_assignee, LINK_WRITTEN_BY)
#
# # In[ ]:
#
#
# # In[ ]:
#
#
# # In[428]:
#
#
# # chane links for two nodes
#
#
# # In[461]:
#
#
# random_node_1 = random.choice(all_names_list)
#
# # In[464]:
#
#
# random_node_2 = random.choice(all_names_list)
#
# # In[465]:
#
#
# print(random_node_1 + " " + random_node_2)
#
# # In[467]:
#
#
# related_commits_1 = conn.query(f""" match (p:Person {{ id : '{random_node_1}' }} ) -[r:WRITTEN_BY]-(b)  return b""")
# related_commits_1_list = []
# for commit in related_commits_1:
#     related_commits_1_list.append(commit.data()["b"]["id"])
# related_commits_1_list
#
# # In[468]:
#
#
# related_commits_2 = conn.query(f""" match (p:Person {{ id : '{random_node_2}' }} ) -[r:WRITTEN_BY]-(b)  return b""")
# related_commits_2_list = []
# for commit in related_commits_2:
#     related_commits_2_list.append(commit.data()["b"]["id"])
# related_commits_2_list
#
# # In[470]:
#
#
# conn.query(f""" match (p:Person {{ id : '{random_node_1}' }} ) -[r:WRITTEN_BY]-(b) delete r """)
#
# # In[471]:
#
#
# conn.query(f""" match (p:Person {{ id : '{random_node_2}' }} ) -[r:WRITTEN_BY]-(b) delete r """)
#
# # In[472]:
#
#
# for c in related_commits_1_list:
#     link_nodes_bidirectional(COMMIT, c, LINK_WAS_AUTHORED_BY,
#                              PERSON, random_node_2, LINK_WRITTEN_BY)
#
# # In[473]:
#
#
# for c in related_commits_2_list:
#     link_nodes_bidirectional(COMMIT, c, LINK_WAS_AUTHORED_BY,
#                              PERSON, random_node_1, LINK_WRITTEN_BY)
#
# # In[ ]:
#
#
# # In[ ]:
#
#
# # In[425]:
#
#
# x = DataFrame(list(zip(list_id, list_r)),
#               columns=['Name', 'Change'])
#
# # In[426]:
#
#
# x.to_csv("anon.csv")
#
# # In[ ]:
#
#
# # In[ ]:
#
#
# # In[325]:
#
#
# make_commit_node(commit.hash)
#
# # In[ ]:
#
#
#
#
