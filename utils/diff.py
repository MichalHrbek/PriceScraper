import json, argparse
from deepdiff import DeepDiff

if __name__== "__main__":
    parser = argparse.ArgumentParser("PricceDiff")
    parser.add_argument('file1')
    parser.add_argument('file2')
    args = parser.parse_args()

    df1 = {i["id"]: i for i in json.loads(open(args.file1).read())}
    df2 = {i["id"]: i for i in json.loads(open(args.file2).read())}

    for i in df1:
        if i in df2:
            d = DeepDiff(df1[i], df2[i])
            if(len(d) != 0):
                print(df1[i]["id"], d)
        else:
            print("[-]", df1[i]["id"])
    
    for i in df2:
        if i not in df1:
            print("[+]", df2[i]["id"])