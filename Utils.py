from github.PullRequest import PullRequest
from pydriller import Commit, ModifiedFile
import os


class Utils:

    @staticmethod
    def make_commit_dict(commit: Commit):
        return {
            "author_date": commit.author_date,
            "sha": commit.hash,
            "la": commit.insertions,
            "ld": commit.deletions
        }

    @staticmethod
    def make_mod_file_dict(file: ModifiedFile):
        return {

            "old_path": file.old_path,
            "new_path": file.new_path,
            "filename": file.filename,

            "directory": os.path.dirname(file.new_path) if file.new_path is not None else None,
            "subsystem": os.path.normpath(file.new_path).split(os.path.sep)[0] if file.new_path is not None else None

        }

    @staticmethod
    def make_file_change_dict(mod_file: ModifiedFile):
        return {
            "la": mod_file.added_lines,
            "ld": mod_file.deleted_lines
        }

    @staticmethod
    def make_pr_dict(pr: PullRequest):

        # TODO: Add comments made to the PR
        # TODO: Add nrev

        approval_date = None
        for review in pr.get_reviews():
            if review.state == "APPROVED":
                approval_date = review.submitted_at

        review_count = pr.get_reviews().totalCount
        review_count += pr.get_issue_comments().totalCount

        return {
            "created_at": pr.created_at,
            "merged_at": pr.merged_at,
            "approval_date": approval_date,
            "comments": review_count,
            "nrev": pr.get_commits().totalCount
        }

    @staticmethod
    def get_pr_reviewers_and_approvers(pull: PullRequest):



        reviewers = set()
        for reviews in pull.get_reviews():
            reviewers.add(reviews.user.email if reviews.user.email is not None else reviews.user.login)

        for reviews in pull.get_issue_comments():
            reviewers.add(reviews.user.email if reviews.user.email is not None else reviews.user.login)

        approvers = set()
        for reviewer in pull.get_reviews():
            if reviewer.state == "APPROVED":
                approvers.add(reviewer.user.email)
        
        return list(reviewers), list(approvers)
