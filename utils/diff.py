import json, argparse
from deepdiff import DeepDiff

IDS = {"billa": "slug", "albert": "url", "tesco": "id"}

if __name__== "__main__":
    parser = argparse.ArgumentParser("PricceDiff")
    parser.add_argument('file1')
    parser.add_argument('file2')
    args = parser.parse_args()

    df1 = {i[IDS[i["store"]]]: i for i in json.loads(open(args.file1).read())}
    df2 = {i[IDS[i["store"]]]: i for i in json.loads(open(args.file2).read())}

    for i in df1:
        if i in df2:
            d = DeepDiff(df1[i], df2[i])
            if(len(d) != 0):
                print(df1[i][IDS[df1[i]["store"]]], d)
        else:
            print("Item from 1st file not in 2nd file", df1[i][IDS[df1[i]["store"]]])
    
    for i in df2:
        if i not in df1:
            print("Item from 2nd file not in 1st file", df2[i][IDS[df2[i]["store"]]])