from common.numeratedkb import KbRelation
from common.numeratedkb import NumerationMap
from common.numeratedkb import NumeratedKb
from ExtractMap import parseYagoEntity
from ExtractMap import parseYagoRelation
import os

def getMeta():
    kb = NumeratedKb("yago", "/Users/renhaotian/实验室/KBRedundancies/KBRedundancies/2-Open-domainExtraction/data")
    # get relation num
    relation_num = kb.totalRelations()
    # get entity num
    entity_num = kb.totalMappings() - relation_num
    # get type num
    type_re = kb.getRelationByName("type")
    records = type_re.getRecordSet()
    types = set()
    for record in records:
        times = 0
        # we just need the second key
        for num in record:
            if times == 1:
                types.add(num)
            times = times + 1
    r_relations = kb.getRelationSet()
    # construct degree dict extract degree
    degrees = dict()
    for relation in r_relations:
        for record in relation.getRecordSet():
            for num in record:
                if degrees.get(num) is not None:
                    degrees[num] = degrees[num] + 1
                else:
                    degrees[num] = 1
    total = 0
    for value in degrees.values():
        total = total + value
    print(total / entity_num)
    print(entity_num)
    print(relation_num)
    print(len(types))


if __name__ == '__main__':
    getMeta()
