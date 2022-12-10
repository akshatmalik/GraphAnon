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
import json
import sys

from dateutil import  parser
if __name__ == '__main__':
    conn = Neo4jConnection(uri="bolt://localhost:11010",
                           user="neo4j",
                           pwd="password",
                           db="wildfly2015")
    node_maker = NodeMaker(conn)

    file_prefix = str(sys.argv[1])

    df = pd.DataFrame()

    # df = pd.read_csv("data/interm_data-2022-12-05 10:44:21.097306.csv")

    start = 0
    jump = 300

    limit = 1000000
    end = start + limit
    while end > start:

        df.to_csv(f"data/interm_data-{datetime.datetime.now()}.csv")

        commit_nodes = node_maker.find_nodes(node_maker.COMMIT, start, jump)
        start += jump

        for commit in commit_nodes:

            # sleep(1)
            print(f"{start} - {commit['id']}")


            data_dict = {}


            data_dict["commit_id"] = commit["id"]
            data_dict["tcmt"] = 0
            data_dict["bugcount"] = 0
            data_dict["fixcount"] = 0
            data_dict["author_date"] = commit["author_date"]
            data_dict["la"] = int(commit["la"])
            data_dict["ld"] = int(commit["ld"])

            date_list = node_maker.find_node_with_relation(node_maker.COMMIT, data_dict["commit_id"],
                                                           node_maker.LINK_MODIFYIED)

            unique_file_list = set()
            unique_directory_list = set()
            unique_subsystem_list = set()

            for item in date_list:
                unique_file_list.add(item["b"]['new_path'])
                unique_directory_list.add(item["b"]['directory'])
                unique_subsystem_list.add(item["b"]['subsystem'])

            data_dict["nf"] = len(unique_file_list)
            data_dict["nd"] = len(unique_directory_list)
            data_dict["ns"] = len(unique_subsystem_list)
            data_dict["ent"] = (data_dict["la"] + data_dict["ld"]) / data_dict["nf"] if data_dict["nf"] != 0 else 0

            pulls = node_maker.find_node_with_relation(node_maker.COMMIT, data_dict["commit_id"],
                                                       node_maker.LINK_PART_OF)

            reviewers = None
            author = None
            if len(pulls) != 0:
                pull_request = pulls[0]["b"]

                reviewers = node_maker.find_node_with_relation(node_maker.PR, pull_request['id'],
                                                               node_maker.LINK_REVIEWER)

                data_dict['app'] = len(reviewers)
                print(pull_request)
                if pull_request["approval_date"] not in ['None', None] and pull_request["created_at"] not in ['None', None]:
                    data_dict['rtime'] = (
                            parser.parse(pull_request["approval_date"]) - parser.parse(pull_request["created_at"])).seconds
                else:
                    data_dict['rtime'] = 0
                data_dict['hcmt'] = pull_request["comments"]

                # TODO: FIXME
                try:
                    author = node_maker.find_node_with_relation(node_maker.COMMIT, data_dict["commit_id"], node_maker.LINK_WAS_AUTHORED_BY)[0]["b"]["id"]
                except Exception:
                    author = None

                approver = None
                if pull_request["approval_date"] not in ['None', None]:
                    approver = node_maker.find_node_with_relation(node_maker.PR, pull_request['id'], node_maker.LINK_APPROVER)[0]["b"]["id"]

                    data_dict['self'] = author == approver
                else:
                    data_dict['self'] = False
                data_dict["nrev"] = pull_request["nrev"]

            else:
                data_dict['app'] = 0
                data_dict['rtime'] = 0
                data_dict['self'] = False
                data_dict['hcmt'] = 0
                data_dict["nrev"] = 0

            data_dict["revd"] = not data_dict["self"]

            # we compute the number of unique changes that have impacted the modified files
            # in the past and the number of developers who have changed the modified files in the pas
            # find all modifying commits
            total_number_of_devs = 0
            total_number_of_commits = 0

            for file in unique_file_list:

                file_changing_commits = node_maker.find_node_with_relation(node_maker.MOD_FILES, file,
                                                                           node_maker.LINK_MODIFYIED)
                total_number_of_commits += len(file_changing_commits)

                unique_authors = set()
                for mod_commits in file_changing_commits:
                    authors = node_maker.find_node_with_relation(node_maker.COMMIT, mod_commits["b"]["id"],
                                                                 node_maker.LINK_WAS_AUTHORED_BY)
                    for authored in authors:
                        unique_authors.add(authored["b"]["id"])

                total_number_of_devs = len(unique_authors)

            data_dict["nuc"] = total_number_of_commits
            data_dict["ndev"] = total_number_of_devs

            parent_commit = node_maker.find_node_with_relation(node_maker.COMMIT, data_dict["commit_id"], node_maker.LINK_PARENT)

            if len(parent_commit) != 0:

                data_dict["age"] = (parser.parse(data_dict["author_date"]) - parser.parse(
                parent_commit[0]['b']['author_date'])).seconds
            else:
                data_dict["age"] = 0

                # author commits
            authors_experience = None
            if author != None:
                authors_experience = node_maker.find_node_with_relation(node_maker.PERSON, author,
                                                                        node_maker.LINK_WRITTEN_BY)
                data_dict["aexp"] = len(authors_experience)
            else:
                data_dict["aexp"] = 0

            # reviewer commits
            reviewer_commit_totals = 0
            all_reviewers = dict()
            if reviewers is not None:
                for rev in reviewers:
                    reviewers_experience = node_maker.find_node_with_relation(node_maker.PERSON, rev["b"]["id"],
                                                                              node_maker.LINK_REVIEWER)
                    all_reviewers[rev["b"]["id"]] = reviewers_experience
                    reviewer_commit_totals += len(reviewers_experience)
                    data_dict["rexp"] = reviewer_commit_totals
            else:
                data_dict["rexp"] = 0


            data_dict["oexp"] = data_dict.get("aexp", 0) + data_dict.get("rexp", 0)

            # Finally, we propose author awareness—a new expertise
            # property that measures the proportion of past changes that
            # were made to a subsystem that the author of the change in
            # question has authored or reviewed

            # experience = 1 / 1 + age  in years

            experience = 0
            if authors_experience != None:
                current_commit_date = parser.parse(data_dict["author_date"])
                for a_commits in authors_experience:
                    a_commit_date = parser.parse(a_commits["b"]["author_date"])
                    year = (1 + (current_commit_date.year - a_commit_date.year))
                    if year <= 0:
                        continue
                    experience += 1 / year

            data_dict["arexp"] = experience

            r_experience = 0
            for a_reviewer in all_reviewers:
                a_a_commits = node_maker.find_node_with_relation(node_maker.PERSON, a_reviewer,
                                                                 node_maker.LINK_REVIEWER)
                for a_commits in a_a_commits:
                    a_commit_date = parser.parse(a_commits["b"]["merged_at"])
                    r_experience += 1 / (1 + a_commit_date.year - a_commit_date.year)

            data_dict["rrexp"] = r_experience
            data_dict["orexp"] = data_dict.get("arexp", 0) + data_dict.get("rrexp", 0)

            # subsytem changes made

            # get the authors commits files
            # from files get subsystems uniqueness
            author_set_of_subsystem = list()
            if authors_experience != None:
                for c in authors_experience:
                    files = node_maker.find_node_with_relation(node_maker.COMMIT, c["b"]["id"], node_maker.LINK_MODIFYIED)
                    for file in files:
                        author_set_of_subsystem.append(file["b"]["subsystem"])
            data_dict["asexp"] = len(author_set_of_subsystem)

            reviewers_subsystem_experience = list()
            for rev in all_reviewers:
                rev_prs = node_maker.find_node_with_relation(node_maker.PERSON, rev, node_maker.LINK_REVIEWER)
                for rev_pr in rev_prs:
                    comss = node_maker.find_node_with_relation(node_maker.PR, rev_pr["b"]["id"],
                                                               node_maker.LINK_PART_OF)
                    # coms experience
                    for c in comss:
                        files = node_maker.find_node_with_relation(node_maker.COMMIT, c["b"]["id"],
                                                                   node_maker.LINK_MODIFYIED)
                        for file in files:
                            reviewers_subsystem_experience.append(file["b"]["subsystem"])

            data_dict["rsexp"] = len(reviewers_subsystem_experience)
            data_dict["osexp"] = data_dict["rsexp"] + data_dict["asexp"]

            # TODO: change this awareness
            data_dict["asawr"] = data_dict["asexp"] + data_dict["arexp"]
            data_dict["rsawr"] = data_dict["rsexp"] + data_dict["asexp"]
            data_dict["osawr"] = data_dict["asawr"] + data_dict["rsawr"]

            print(data_dict)
            df = df.append(data_dict, ignore_index=True)

            # data_dict["bugcount"] = commit["bugcount"]
            # data_dict["fixcount"] = commit["fixcount"]
            # data_dict["revd"] = commit["revd"]
            # data_dict["tcmt"] = commit["tcmt"]
            # data_dict["bugcount"] = commit["bugcount"]
            # data_dict["bugcount"] = commit["bugcount"]
            # data_dict["bugcount"] = commit["bugcount"]
            # data_dict["bugcount"] = commit["bugcount"]
            # data_dict["bugcount"] = commit["bugcount"]
            # data_dict["bugcount"] = commit["bugcount"]
            # data_dict["bugcount"] = commit["bugcount"]
            # data_dict["bugcount"] = commit["bugcount"]

    final_file_name = f"data/data-{datetime.datetime.now()}.csv"
    df.to_csv(final_file_name)

    df = pd.read_csv(final_file_name)
    df["bugcount"] = 0
    df["fixcount"] = 0
    df["tcmt"] = 0

    json_file_path = "/Users/maalik/Library/CloudStorage/OneDrive-Queen'sUniversity/Study/Research/data_sets/wifdfly_fix_and_introducers_pairs.json"
    repo_path = "/Users/maalik/OneDrive - Queen's University/Study/Research/Demo Project/wildfly"
    repo_name = repo_path.split("""/""")[-1]

    json_text = json.load(open(json_file_path))

    for fix_defect_pair in json_text:

        fix_commit_sha = fix_defect_pair[0]
        defect_commit_sha = fix_defect_pair[1]

        if fix_commit_sha in df["commit_id"].values:
            df.loc[df["commit_id"] == fix_commit_sha , "fixcount"] += 1


        if defect_commit_sha in df["commit_id"].values:
            df.loc[df["commit_id"] == defect_commit_sha , "bugcount"] += 1



    print(f"fix_count - {df['fixcount'].sum()}  bug_count - {df['bugcount'].sum()}")
    df["author_date"] = df["author_date"].apply(lambda x: int(parser.parse(x).timestamp()))
    df.to_csv(f"{file_prefix}_bug_annonted-{datetime.datetime.now()}.csv")
