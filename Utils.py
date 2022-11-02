from pydriller import Commit


class Utils:

    @staticmethod
    def make_commit_dict(commit: Commit):
        return {
            "author_date": commit.author_date,
            "sha": commit.hash,
            "la": commit.insertions,
            "ld": commit.deletions
        }
