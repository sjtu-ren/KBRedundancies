from common.numeratedkb import NumerationMap
import os

"""
    yago map in memory
"""

def parseYagoEntity(yagoMap: NumerationMap):
    path = "../data/yago-1.0.0-native/entities"
    path_list = os.listdir(path)
    for file in path_list:
        pathname = os.path.join(path, file)
        f = open(pathname, 'r')
        for line in f.readlines():
            name, isConcept = line.strip().split('\t')
            yagoMap.mapName(name)
        print(yagoMap.totalMappings())
        f.close()


def parseYagoRelation(yagoMap: NumerationMap):
    path = "../data/yago-1.0.0-native/facts"
    path_list = os.listdir(path)
    print(path_list)
    for dir in path_list:
        if dir == ".DS_Store":
            continue
        yagoMap.mapName(dir)
        dpath = os.path.join(path, dir)
        file_list = os.listdir(dpath)
        print(file_list)
        for file in file_list:
            fpath = os.path.join(dpath, file)
            f = open(fpath, 'r')
            for line in f.readlines():
                index, arg1, arg2, possibility = line.strip().split('\t')
                yagoMap.mapName(arg1)
                yagoMap.mapName(arg2)
    print(yagoMap.totalMappings())


def parseYago():
    mpath = "/Users/renhaotian/实验室/KBRedundancies/KBRedundancies/2-Open-domainExtraction/data/map"
    yagoMap = NumerationMap()
    parseYagoEntity(yagoMap)
    parseYagoRelation(yagoMap)
    yagoMap.dump(mpath)


if __name__ == '__main__':
    parseYago()

