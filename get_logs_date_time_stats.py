import pydriller
import json
import pandas as pd
from datetime import datetime

if __name__ == "__main__":

    json_file_path = "/Users/maalik/Library/CloudStorage/OneDrive-Queen'sUniversity/Study/Research/data_sets" \
                     "/wifdfly_fix_and_introducers_pairs.json "
    repo_path = "/Users/maalik/OneDrive - Queen's University/Study/Research/Demo Project/wildfly"
    repo_name = repo_path.split("""/""")[-1]

    json_text = json.load(open(json_file_path))

    df = pd.DataFrame()

    repo = pydriller.Git(repo_path)

    for fix_defect_pair in json_text:
        data_dict = {}

        fix_commit_sha = fix_defect_pair[0]
        defect_commit_sha = fix_defect_pair[1]

        fix_commit = repo.get_commit(fix_commit_sha)
        data_dict["commit"] = fix_commit
        data_dict["type"] = "FIX"
        data_dict["date"] = fix_commit.author_date
        data_dict["year"] = fix_commit.author_date.year
        data_dict["month"] = fix_commit.author_date.month
        df = df.append(data_dict, ignore_index=True)

        fix_commit = repo.get_commit(defect_commit_sha)
        data_dict["commit"] = fix_commit
        data_dict["type"] = "INTRO"
        data_dict["date"] = fix_commit.author_date
        data_dict["year"] = fix_commit.author_date.year
        data_dict["month"] = fix_commit.author_date.month
        df = df.append(data_dict, ignore_index=True)


    df.to_csv(f"git_log_distribution-{repo_name}-{datetime.now()}.csv")
    # print(json_text)
