import pydriller
import json
import pandas as pd
from datetime import datetime

from pydriller import Repository

if __name__ == "__main__":

    data = json.load(open("/Users/maalik/Library/CloudStorage/OneDrive-Queen'sUniversity/Study/Research/data_sets/wifdfly_fix_and_introducers_pairs.json"))
    # print(len(data))

    data1 = json.load(open("issue_list.json"))
    # print(data1)
    data2 = json.load(open("issue_list_jenkins.json"))
    # print(data2)

    itroducer = set()
    for i in data:
        itroducer.add(i[1])

    print(len(list(itroducer)))