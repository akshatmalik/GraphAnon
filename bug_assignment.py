import json

import  pandas as pd
from dateutil import  parser

if __name__ == "__main__":

    df = pd.read_csv("data/data-2022-11-16 19:45:19.334003.csv")
    df["bugcount"] = 0
    df["fixcount"] = 0

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
    df.to_csv("bug_annonted.csv")


