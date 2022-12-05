import github.GithubException
from pydriller import Repository, Commit, Git
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_commit = 0
    limit_commit = 30
    end_commit = start_commit + limit_commit

    conn = Neo4jConnection(uri="bolt://localhost:11010",
                           user="neo4j",
                           pwd="password",
                           db="wildfly2015")
    node_maker = NodeMaker(conn)

    node_maker.make_contraint()

    repository_path = "wildfly/"
    github_url = "wildfly/wildfly"

    from_date = datetime.datetime(2015, 1, 1, 17, 0, 0)
    to_date = datetime.datetime(2015, 12, 30, 17, 59, 0)

    git_repo = Git(repository_path)

    if True:

        print("DOING COMMITS")

        for commit in Repository(repository_path, order='reverse', since=from_date, to=to_date).traverse_commits():

            print(f"{start_commit} - {commit.hash}")

            # start_commit += 1
            # if start_commit > end_commit:
            #     break

            node_maker.make_commit_node(commit)

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
                if mod_file is not None:
                    node_maker.make_mod_files(mod_file)

                # link relations

                node_maker.link_nodes(node_maker.COMMIT, commit.hash, node_maker.LINK_MODIFYIED,
                                      node_maker.MOD_FILES, mod_file.new_path,
                                      Utils.make_file_change_dict(mod_file))

            for parent_commit in Repository(repository_path, only_commits=commit.parents,
                                            order='reverse').traverse_commits():
                node_maker.make_commit_node(parent_commit)
                node_maker.link_nodes_bidirectional(node_maker.COMMIT, commit.hash, node_maker.LINK_CHILD,
                                                    node_maker.COMMIT, parent_commit.hash, node_maker.LINK_PARENT)

            sleep(1)

    if True:

        print("DOING PULLS")

        start_pull = 0
        limit_pull = 10
        end_pull = start_pull + limit_pull

        # using an access token
        g = Github("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")
        user = g.get_user()
        print(user.login)

        ## Enter your repo here:
        repo = g.get_repo(github_url)
        print(repo)
        details_list = []

        # start_pull_number = 8531
        # start_pull_number = 8391
        start_pull_number = 7507



        pull = repo.get_pull(start_pull_number)

        while from_date <= pull.created_at <= to_date:

            sleep(10)

            print(f"{start_pull} -- PULL WITH ID {start_pull_number} ")

            try:
                pull = repo.get_pull(start_pull_number)
            except Exception as e:
                print("NOT FOUND")
                start_pull_number += -1
                continue

            # todo: add condition for pull request fetch

            if not pull.is_merged():
                start_pull_number += -1
                continue



            node_maker.make_pr_node(pull)
            reviewers, approvers = Utils.get_pr_reviewers_and_approvers(pull)

            for reviewer in reviewers:
                node_maker.make_person_node(reviewer)
                node_maker.link_nodes(node_maker.PR, pull.number, node_maker.LINK_REVIEWER,
                                      node_maker.PERSON, reviewer)

            for approver in approvers:
                node_maker.make_person_node(approver)
                node_maker.link_nodes(node_maker.PR, pull.number, node_maker.LINK_APPROVER,
                                      node_maker.PERSON, approver)

            commit = None

            try:

                commit = git_repo.get_commit(pull.merge_commit_sha)
            except Exception:

                for i in pull.get_commits():
                    try:
                        commit = git_repo.get_commit(i.sha)
                        break
                    except Exception:
                        pass

            if commit is None:
                print(f"NOT FOUND COMMIT ID - {pull.merge_commit_sha}")
                start_pull_number += -1
                continue

            # commit_dict = {
            #     "author_date": commit.author.created_at,
            #     "sha": commit.sha,
            #     "la": commit.stats.additions,
            #     "ld": commit.stats.deletions
            # }

            commit_dict = {
                "author_date": commit.author_date,
                "sha": commit.hash,
                "la": commit.insertions,
                "ld": commit.deletions
            }


            node_maker.make_commit_node(commit, commit_dict)
            node_maker.link_nodes(node_maker.COMMIT, commit_dict["sha"], node_maker.LINK_PART_OF,
                                  node_maker.PR, pull.number)

            start_pull_number += -1

            # start_pull += 1
            # if start_pull > end_pull:
            #     break