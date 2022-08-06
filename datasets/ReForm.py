import os
import sys

sys.path.append("..")
from common.numeratedkb import NumeratedKb, NumerationMap, KbRelation

def ReForm():
    dlist = os.listdir(".")
    for dataset in dlist:
        if dataset == "ReForm.py" or dataset == "datasets.7z" or dataset == "newsets" or dataset == "test.py":
            continue
        fpath = os.path.join(".", dataset)
        dataset = dataset[:-1]
        dataset = dataset[:-1]
        dataset = dataset[:-1]
        dataset = dataset[:-1]
        f = open(fpath, "r")
        relations = dict()
        map = NumerationMap()
        for line in f.readlines():
            contents = line.strip().split('\t')
            arity = len(contents) - 1
            for content in contents:
                map.mapName(content)
            i = 0
            record = list()
            for content in contents:
                if i == 0:
                    i = i + 1
                    continue
                record.append(map.name2Num(content))
            if relations.get(contents[0]) is None:
                relations[contents[0]] = KbRelation(contents[0], map.name2Num(contents[0]), arity)
                if arity != relations[contents[0]].getArity():
                    print(dataset)
                    print(contents)
                    continue
                relations[contents[0]].addRecord(tuple(record))
            else:
                if arity != relations[contents[0]].getArity():
                    print(dataset)
                    print(contents)
                    continue
                relations[contents[0]].addRecord(tuple(record))
        dpath = os.path.join("./newsets", dataset)
        print(dpath)
        os.mkdir(dpath)
        map.dump(dpath)
        for key in relations:
            relations[key].dump(dpath)
            

if __name__ == '__main__':
    ReForm()