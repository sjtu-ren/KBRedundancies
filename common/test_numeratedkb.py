import unittest
import uuid
from numeratedkb import *
import shutil

MEM_DIR = "/dev/shm"
KB_NAME = None
KB_PATH = None
TMP_PATHS = []
TMP_FILES = []

def createTestMapFiles(kbPath: str) -> None:
    """
    Create map files for test.
    """
    with open(getMapFilePath(kbPath, 1), 'w') as ofd:
        ofd.write("family\t1\n")
        ofd.write("mother\t2\n")
        ofd.write("father\t3\n")

    with open(getMapFilePath(kbPath, 2), 'w') as ofd:
        ofd.write("alice\t4\n")
        ofd.write("bob\t5\n")
        ofd.write("catherine\t6\n")
        ofd.write("diana\t7\n")
        ofd.write("erick\t8\n")
        ofd.write("frederick\t9\n")

    with open(getMapFilePath(kbPath, 3), 'w') as ofd:
        ofd.write("gabby\ta\n")
        ofd.write("harry\tb\n")
        ofd.write("isaac\tc\n")
        ofd.write("jena\td\n")
        ofd.write("kyle\te\n")
        ofd.write("lily\tf\n")
    
    with open(getMapFilePath(kbPath, 4), 'w') as ofd:
        ofd.write("marvin\t10\n")
        ofd.write("nataly\t11\n")

def createTestRelFiles(kbPath: str) -> None:
    with open(getRelFilePath(kbPath, "family", 3, 4), 'wb') as ofd:
        ofd.write(struct.pack("<iii", 4, 5, 6))
        ofd.write(struct.pack("<iii", 7, 8, 9))
        ofd.write(struct.pack("<iii", 0xa, 0xb, 0xc))
        ofd.write(struct.pack("<iii", 0xd, 0xe, 0xf))

    with open(getRelFilePath(kbPath, "mother", 2, 4), 'wb') as ofd:
        ofd.write(struct.pack("<ii", 4, 6))
        ofd.write(struct.pack("<ii", 7, 9))
        ofd.write(struct.pack("<ii", 0xa, 0xc))
        ofd.write(struct.pack("<ii", 0xd, 0xf))

    with open(getRelFilePath(kbPath, "father", 2, 4), 'wb') as ofd:
        ofd.write(struct.pack("<ii", 5, 6))
        ofd.write(struct.pack("<ii", 8, 9))
        ofd.write(struct.pack("<ii", 0xb, 0xc))
        ofd.write(struct.pack("<ii", 0x10, 0x11))

def createTestKb() -> str:
    """
    Returns:
        The path for the KB
    """
    kb_name = str(uuid.uuid4())
    kb_path = os.path.join(MEM_DIR, kb_name)
    os.mkdir(kb_path)
    createTestMapFiles(kb_path)
    createTestRelFiles(kb_path)
    return (kb_name, kb_path)

def deleteTestKb(kbPath: str) -> None:
    shutil.rmtree(kbPath)

def setUpModule():
    global KB_PATH
    global KB_NAME
    KB_NAME, KB_PATH = createTestKb()

def tearDownModule():
    global KB_PATH
    global TMP_PATHS
    global TMP_FILES
    deleteTestKb(KB_PATH)
    for tmp_path in TMP_PATHS:
        shutil.rmtree(tmp_path)
    for tmp_file in TMP_FILES:
        os.remove(tmp_file)

class RelFilePathTest(unittest.TestCase):
    
    def testAbsolutePath1(self):
        kb_path = "/root/home/dir"
        rel_name = "relation"
        arity = 3
        records = 15
        rel_file_path = getRelFilePath(kb_path, rel_name, arity, records)

        self.assertEqual("/root/home/dir/relation_3_15.rel", rel_file_path)
        self.assertEqual((rel_name, arity, records), parseRelFilePath(rel_file_path))

    def testAbsolutePath2(self):
        kb_path = "/root/home/dir/"
        rel_name = "relation"
        arity = 3
        records = 15
        rel_file_path = getRelFilePath(kb_path, rel_name, arity, records)

        self.assertEqual("/root/home/dir/relation_3_15.rel", rel_file_path)
        self.assertEqual((rel_name, arity, records), parseRelFilePath(rel_file_path))

    def test_relativePath1(self):
        kb_path = "./dir"
        rel_name = "relation"
        arity = 3
        records = 15
        rel_file_path = getRelFilePath(kb_path, rel_name, arity, records)

        self.assertEqual("./dir/relation_3_15.rel", rel_file_path)
        self.assertEqual((rel_name, arity, records), parseRelFilePath(rel_file_path))

    def test_relativePath2(self):
        kb_path = "dir"
        rel_name = "relation"
        arity = 3
        records = 15
        rel_file_path = getRelFilePath(kb_path, rel_name, arity, records)

        self.assertEqual("dir/relation_3_15.rel", rel_file_path)
        self.assertEqual((rel_name, arity, records), parseRelFilePath(rel_file_path))

class MapFileTest(unittest.TestCase):

    def testAbsolutePath1(self):
        kb_path = "/root/home/dir"
        num = 201
        map_file_path = getMapFilePath(kb_path, num)

        self.assertEqual("/root/home/dir/map201.tsv", map_file_path)

    def testAbsolutePath2(self):
        kb_path = "/root/home/dir/"
        num = 201
        map_file_path = getMapFilePath(kb_path, num)

        self.assertEqual("/root/home/dir/map201.tsv", map_file_path)

    def testRelativePath1(self):
        kb_path = "./dir"
        num = 201
        map_file_path = getMapFilePath(kb_path, num)

        self.assertEqual("./dir/map201.tsv", map_file_path)

    def testRelativePath2(self):
        kb_path = "dir"
        num = 201
        map_file_path = getMapFilePath(kb_path, num)

        self.assertEqual("dir/map201.tsv", map_file_path)

class NumerationMapTest(unittest.TestCase):

    global KB_PATH
    global TMP_PATHS

    def testCreateEmpty(self):
        num_map = NumerationMap()

        self.assertEqual(0, num_map.totalMappings())
        self.assertEqual(0, len(num_map._numMap))
        self.assertEqual(1, len(num_map._numArray))
        self.assertEqual(0, len(num_map._freeNums))
        
        self.assertEqual(None, num_map.unmapName('a'))
        self.assertEqual(None, num_map.unmapNumeration(0))
        self.assertEqual(None, num_map.unmapNumeration(1))

        self.assertEqual(1, num_map.mapName('a'))
        self.assertEqual(2, num_map.mapName('b'))
        self.assertEqual(3, num_map.mapName('c'))

        self.assertEqual(3, num_map.totalMappings())
        self.assertEqual(3, len(num_map._numMap))
        self.assertEqual(4, len(num_map._numArray))
        self.assertEqual(0, len(num_map._freeNums))

    def testRead(self):
        num_map = NumerationMap(KB_PATH)

        self.assertEqual(17, num_map.totalMappings())
        self.assertEqual(17, len(num_map._numMap))
        self.assertEqual(18, len(num_map._numArray))
        self.assertEqual(0, len(num_map._freeNums))

        self.assertEqual("family", num_map.num2Name(0x1))
        self.assertEqual("mother", num_map.num2Name(0x2))
        self.assertEqual("father", num_map.num2Name(0x3))
        self.assertEqual("alice", num_map.num2Name(0x4))
        self.assertEqual("bob", num_map.num2Name(0x5))
        self.assertEqual("catherine", num_map.num2Name(0x6))
        self.assertEqual("diana", num_map.num2Name(0x7))
        self.assertEqual("erick", num_map.num2Name(0x8))
        self.assertEqual("frederick", num_map.num2Name(0x9))
        self.assertEqual("gabby", num_map.num2Name(0xa))
        self.assertEqual("harry", num_map.num2Name(0xb))
        self.assertEqual("isaac", num_map.num2Name(0xc))
        self.assertEqual("jena", num_map.num2Name(0xd))
        self.assertEqual("kyle", num_map.num2Name(0xe))
        self.assertEqual("lily", num_map.num2Name(0xf))
        self.assertEqual("marvin", num_map.num2Name(0x10))
        self.assertEqual("nataly", num_map.num2Name(0x11))

        self.assertEqual(0x1, num_map.name2Num("family"))
        self.assertEqual(0x2, num_map.name2Num("mother"))
        self.assertEqual(0x3, num_map.name2Num("father"))
        self.assertEqual(0x4, num_map.name2Num("alice"))
        self.assertEqual(0x5, num_map.name2Num("bob"))
        self.assertEqual(0x6, num_map.name2Num("catherine"))
        self.assertEqual(0x7, num_map.name2Num("diana"))
        self.assertEqual(0x8, num_map.name2Num("erick"))
        self.assertEqual(0x9, num_map.name2Num("frederick"))
        self.assertEqual(0xa, num_map.name2Num("gabby"))
        self.assertEqual(0xb, num_map.name2Num("harry"))
        self.assertEqual(0xc, num_map.name2Num("isaac"))
        self.assertEqual(0xd, num_map.name2Num("jena"))
        self.assertEqual(0xe, num_map.name2Num("kyle"))
        self.assertEqual(0xf, num_map.name2Num("lily"))
        self.assertEqual(0x10, num_map.name2Num("marvin"))
        self.assertEqual(0x11, num_map.name2Num("nataly"))

    def testWrite(self):
        num_map = NumerationMap(KB_PATH)
        tmp_dir = str(uuid.uuid4())
        tmp_path = os.path.join(MEM_DIR, tmp_dir)
        os.mkdir(tmp_path)
        TMP_PATHS.append(tmp_path)
        original_value = NumerationMap._MAX_MAP_ENTRIES
        NumerationMap._MAX_MAP_ENTRIES = 2
        num_map.dump(tmp_path)
        NumerationMap._MAX_MAP_ENTRIES = original_value
        num_map2 = NumerationMap(tmp_path)

        self.assertEqual(num_map._numMap, num_map2._numMap)
        self.assertEqual(num_map._numArray, num_map2._numArray)
        self.assertEqual(num_map._freeNums, num_map2._freeNums)

        self.assertEqual(set(['map%d.tsv' % i for i in range(1, 10)]), set(os.listdir(tmp_path)))
        for i in range(1, 9):
            with open(os.path.join(tmp_path, "map%d.tsv" % i), 'r') as ifd:
                self.assertEqual(2, len(ifd.readlines()))
        with open(os.path.join(tmp_path, "map9.tsv"), 'r') as ifd:
            self.assertEqual(1, len(ifd.readlines()))

    def testMappingName(self):
        num_map = NumerationMap(KB_PATH)

        self.assertEqual(1, num_map.mapName('family'))
        self.assertEqual(4, num_map.mapName('alice'))
        self.assertEqual(17, num_map.mapName('nataly'))

        self.assertEqual(18, num_map.mapName('a'))
        self.assertEqual(19, num_map.mapName('b'))
        self.assertEqual(20, num_map.mapName('c'))

        self.assertEqual(20, num_map.totalMappings())
        self.assertEqual(20, len(num_map._numMap))
        self.assertEqual(21, len(num_map._numArray))
        self.assertEqual(0, len(num_map._freeNums))

    def testUnMappingName(self):
        num_map = NumerationMap(KB_PATH)

        self.assertEqual(None, num_map.unmapName('a'))
        self.assertEqual(1, num_map.unmapName('family'))
        self.assertEqual(4, num_map.unmapName('alice'))
        self.assertEqual(17, num_map.unmapName('nataly'))
        self.assertEqual(None, num_map.unmapName('family'))
        self.assertEqual(None, num_map.unmapName('alice'))
        self.assertEqual(None, num_map.unmapName('nataly'))

        self.assertEqual(14, num_map.totalMappings())
        self.assertEqual(14, len(num_map._numMap))
        self.assertEqual(18, len(num_map._numArray))
        self.assertEqual(3, len(num_map._freeNums))

    def testUnMappingNum(self):
        num_map = NumerationMap(KB_PATH)

        self.assertEqual(None, num_map.unmapNumeration(0))
        self.assertEqual(None, num_map.unmapNumeration(18))
        self.assertEqual('family', num_map.unmapNumeration(1))
        self.assertEqual('alice', num_map.unmapNumeration(4))
        self.assertEqual('nataly', num_map.unmapNumeration(17))
        self.assertEqual(None, num_map.unmapNumeration(1))
        self.assertEqual(None, num_map.unmapNumeration(4))
        self.assertEqual(None, num_map.unmapNumeration(17))

        self.assertEqual(14, num_map.totalMappings())
        self.assertEqual(14, len(num_map._numMap))
        self.assertEqual(18, len(num_map._numArray))
        self.assertEqual(3, len(num_map._freeNums))

    def testMappingWithUnmapping(self):
        num_map = NumerationMap(KB_PATH)

        self.assertEqual(1, num_map.unmapName('family'))
        self.assertEqual(4, num_map.unmapName('alice'))
        self.assertEqual(17, num_map.unmapName('nataly'))
        self.assertEqual(1, num_map.mapName('FAMILY'))
        self.assertEqual(4, num_map.mapName('ALICE'))
        self.assertEqual(17, num_map.mapName('NATALY'))

        self.assertEqual(18, num_map.mapName('a'))
        self.assertEqual(19, num_map.mapName('b'))
        self.assertEqual(20, num_map.mapName('c'))
        self.assertEqual('a', num_map.unmapNumeration(18))
        self.assertEqual('b', num_map.unmapNumeration(19))
        self.assertEqual('c', num_map.unmapNumeration(20))

        self.assertEqual(17, num_map.totalMappings())
        self.assertEqual(17, len(num_map._numMap))
        self.assertEqual(21, len(num_map._numArray))
        self.assertEqual(3, len(num_map._freeNums))

class KbRelationTest(unittest.TestCase):
    
    global KB_PATH
    global TMP_PATHS

    def checkRecordSet(self, records: set, rel: KbRelation) -> None:
        self.assertEqual(len(records), rel.totalRecords())
        self.assertEqual(records, rel.getRecordSet())
        for record in rel:
            self.assertTrue(record in records)
        for record in records:
            self.assertTrue(rel.hasRecord(record))

    def testCreateEmpty(self):
        rel = KbRelation("relation", 0, 4, 0)

        self.assertEqual("relation", rel.getName())
        self.assertEqual(4, rel.getArity())
        self.assertEqual(0, rel.totalRecords())
        self.assertEqual(set(), rel.getRecordSet())

        rel.addRecord((1, 2 , 3, 4))
        rel.addRecords([(5, 6, 7, 8), (11, 22, 33, 44)])
        rel.addRecord((11, 22, 33, 44))

        self.assertEqual(4, rel.getArity())
        self.checkRecordSet(set([(1, 2, 3, 4), (5, 6, 7, 8), (11, 22, 33, 44)]), rel)

        rel.addRecord((55, 66, 77, 88))
        rel.removeRecord((5, 6, 7, 8))
        rel.removeRecord((55, 66, 77, 88))

        self.assertEqual(4, rel.getArity())
        self.checkRecordSet(set([(1, 2, 3, 4), (11, 22, 33, 44)]), rel)

    def testRead1(self):
        rel = KbRelation("family", 0, 3, 4, KB_PATH)

        self.assertEqual("family", rel.getName())
        self.assertEqual(3, rel.getArity())
        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xa, 0xb, 0xc), (0xd, 0xe, 0xf)]), rel)

    def testRead2(self):
        rel = KbRelation("mother", 0, 2, 4, KB_PATH)

        self.assertEqual("mother", rel.getName())
        self.assertEqual(2, rel.getArity())
        self.checkRecordSet(set([(4, 6), (7, 9), (0xa, 0xc), (0xd, 0xf)]), rel)

    def testRead3(self):
        rel = KbRelation("father", 0, 2, 4, KB_PATH)

        self.assertEqual("father", rel.getName())
        self.assertEqual(2, rel.getArity())
        self.checkRecordSet(set([(5, 6), (8, 9), (0xb, 0xc), (0x10, 0x11)]), rel)

    def testWrite(self):
        rel = KbRelation("family", 0, 3, 4, KB_PATH)
        tmp_dir = str(uuid.uuid4())
        tmp_path = os.path.join(MEM_DIR, tmp_dir)
        os.mkdir(tmp_path)
        TMP_PATHS.append(tmp_path)
        rel.dump(tmp_path)
        rel2 = KbRelation("family", 0, 3, 4, tmp_path)

        self.assertEqual("family", rel2.getName())
        self.assertEqual(3, rel2.getArity())
        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xa, 0xb, 0xc), (0xd, 0xe, 0xf)]), rel2)

    def testAddRecord(self):
        rel = KbRelation("family", 0, 3, 4, KB_PATH)
        rel.addRecord((4, 4, 4))
        rel.addRecord((5, 5, 5))

        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xa, 0xb, 0xc), (0xd, 0xe, 0xf), (4, 4, 4), (5, 5, 5)]), rel)

        rel.addRecord((4, 5, 6))
        with self.assertRaises(KbException):
            rel.addRecord((4, 4))
        with self.assertRaises(KbException):
            rel.addRecord((4, 4, 5, 5))

        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xa, 0xb, 0xc), (0xd, 0xe, 0xf), (4, 4, 4), (5, 5, 5)]), rel)

    def testAddRecords(self):
        rel = KbRelation("family", 0, 3, 4, KB_PATH)
        rel.addRecords([(4, 4, 4), (5, 5, 5)])

        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xa, 0xb, 0xc), (0xd, 0xe, 0xf), (4, 4, 4), (5, 5, 5)]), rel)

        rel.addRecords([(4, 5, 6)])
        with self.assertRaises(KbException):
            rel.addRecords([(6, 6, 6), (4, 4)])
        with self.assertRaises(KbException):
            rel.addRecords([(4, 4, 5, 5)])

        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xa, 0xb, 0xc), (0xd, 0xe, 0xf), (4, 4, 4), (5, 5, 5)]), rel)

    def testRemoveRecord(self):
        rel = KbRelation("family", 0, 3, 4, KB_PATH)
        rel.removeRecord((4, 4, 4))
        rel.removeRecord((4, 7, 10))

        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xa, 0xb, 0xc), (0xd, 0xe, 0xf)]), rel)

        rel.removeRecord((4, 5, 6))
        rel.removeRecord((0xa, 0xb, 0xc))

        self.checkRecordSet(set([(7, 8, 9), (0xd, 0xe, 0xf)]), rel)

        rel.removeRecord((4, 5, 6))
        rel.removeRecord((0xa, 0xb, 0xc))

        self.checkRecordSet(set([(7, 8, 9), (0xd, 0xe, 0xf)]), rel)

        rel.removeRecord((7, 8, 9))
        rel.removeRecord((0xd, 0xe, 0xf))

        self.checkRecordSet(set(), rel)

    def testAddWithRemoveRecord(self):
        rel = KbRelation("family", 0, 3, 4, KB_PATH)
        rel.removeRecord((4, 4, 4))
        rel.removeRecord((4, 7, 10))
        rel.addRecord((4, 4, 4))
        rel.addRecord((5, 5, 5))

        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xa, 0xb, 0xc), (0xd, 0xe, 0xf), (4, 4, 4), (5, 5, 5)]), rel)

        rel.removeRecord((4, 5, 6))
        rel.removeRecord((0xa, 0xb, 0xc))

        self.checkRecordSet(set([(7, 8, 9), (0xd, 0xe, 0xf), (4, 4, 4), (5, 5, 5)]), rel)

        rel.addRecords([(4, 5, 6)])
        with self.assertRaises(KbException):
            rel.addRecords([(6, 6, 6), (4, 4)])
        with self.assertRaises(KbException):
            rel.addRecords([(4, 4, 5, 5)])

        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xd, 0xe, 0xf), (4, 4, 4), (5, 5, 5)]), rel)

        rel.addRecords([(4, 5, 6), (4, 5, 6), (4, 5, 6), (6, 6, 6)])

        self.checkRecordSet(set([(4, 5, 6), (7, 8, 9), (0xd, 0xe, 0xf), (4, 4, 4), (5, 5, 5), (6, 6, 6)]), rel)

        rel.removeRecord((4, 5, 6))
        rel.removeRecord((0xa, 0xb, 0xc))

        self.checkRecordSet(set([(7, 8, 9), (0xd, 0xe, 0xf), (4, 4, 4), (5, 5, 5), (6, 6, 6)]), rel)

class NumeratedKbTest(unittest.TestCase):

    global KB_PATH
    global KB_NAME
    global TMP_PATHS
    global MEM_DIR

    def testCreateEmpty(self):
        kb = NumeratedKb("test")

        self.assertEqual("test", kb.getName())
        self.assertEqual(0, kb.getNumerationMap().totalMappings())
        self.assertEqual(0, len(kb.getRelationSet()))
        self.assertEqual(0, kb.totalRecords())

        kb.addNamedRecord2RelationByName("family", ("alice", "bob", "catherine"))
        self.assertEqual(1, kb.getRelationByName("family").getNumeration())
        kb.addNamedRecord2RelationByNumeration(1, ("diana", "erick", "frederick"))
        self.assertEqual(8, kb.mapName("gabby"))
        self.assertEqual(9, kb.mapName("harry"))
        self.assertEqual(10, kb.mapName("isaac"))
        self.assertEqual(11, kb.mapName("jena"))
        self.assertEqual(12, kb.mapName("kyle"))
        self.assertEqual(13, kb.mapName("lily"))
        kb.addNumeratedRecord2RelationByName("family", (8, 9, 10))
        kb.addNumeratedRecord2RelationByNumeration(1, (11, 12, 13))
    
        self.assertEqual(13, kb.getNumerationMap().totalMappings())
        self.assertEqual(1, len(kb.getRelationSet()))
        self.assertEqual(4, kb.totalRecords())
        self.assertTrue(kb.hasNamedRecordInRelationByName("family", ("alice", "bob", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("family", ("diana", "erick", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("family", ("gabby", "harry", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("family", ("jena", "kyle", "lily")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(1, ("alice", "bob", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(1, ("diana", "erick", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(1, ("gabby", "harry", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(1, ("jena", "kyle", "lily")))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("family", (2, 3, 4)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("family", (5, 6, 7)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("family", (8, 9, 10)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("family", (11, 12, 13)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(1, (2, 3, 4)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(1, (5, 6, 7)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(1, (8, 9, 10)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(1, (11, 12, 13)))

    def testRead(self):
        kb = NumeratedKb(KB_NAME, MEM_DIR)

        self.assertEqual(KB_NAME, kb.getName())
        self.assertEqual(17, kb.getNumerationMap().totalMappings())
        self.assertEqual(3, len(kb.getRelationSet()))
        self.assertEqual(12, kb.totalRecords())

        self.assertTrue(kb.hasNamedRecordInRelationByName("family", ("alice", "bob", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("family", ("diana", "erick", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("family", ("gabby", "harry", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("family", ("jena", "kyle", "lily")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(1, ("alice", "bob", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(1, ("diana", "erick", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(1, ("gabby", "harry", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(1, ("jena", "kyle", "lily")))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("family", (4, 5, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("family", (7, 8, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("family", (10, 11, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("family", (13, 14, 15)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(1, (4, 5, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(1, (7, 8, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(1, (10, 11, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(1, (13, 14, 15)))

        self.assertTrue(kb.hasNamedRecordInRelationByName("mother", ("alice", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("mother", ("diana", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("mother", ("gabby", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("mother", ("jena", "lily")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(2, ("alice","catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(2, ("diana", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(2, ("gabby", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(2, ("jena", "lily")))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("mother", (4, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("mother", (7, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("mother", (10, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("mother", (13, 15)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(2, (4, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(2, (7, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(2, (10, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(2, (13, 15)))

        self.assertTrue(kb.hasNamedRecordInRelationByName("father", ("bob", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("father", ("erick", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("father", ("harry", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("father", ("marvin", "nataly")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(3, ("bob", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(3, ("erick", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(3, ("harry", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(3, ("marvin", "nataly")))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("father", (5, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("father", (8, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("father", (11, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("father", (16, 17)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(3, (5, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(3, (8, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(3, (11, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(3, (16, 17)))

    def testWrite(self):
        kb = NumeratedKb(KB_NAME, MEM_DIR)
        tmp_dir = str(uuid.uuid4())
        tmp_path = os.path.join(MEM_DIR, tmp_dir)
        os.mkdir(tmp_path)
        TMP_PATHS.append(tmp_path)
        kb.dump(tmp_path)
        kb2 = NumeratedKb(KB_NAME, tmp_path)

        self.assertEqual(KB_NAME, kb2.getName())
        self.assertEqual(17, kb2.getNumerationMap().totalMappings())
        self.assertEqual(3, kb2.totalRelations())
        self.assertEqual(12, kb2.totalRecords())

        self.assertTrue(kb2.hasNamedRecordInRelationByName("family", ("alice", "bob", "catherine")))
        self.assertTrue(kb2.hasNamedRecordInRelationByName("family", ("diana", "erick", "frederick")))
        self.assertTrue(kb2.hasNamedRecordInRelationByName("family", ("gabby", "harry", "isaac")))
        self.assertTrue(kb2.hasNamedRecordInRelationByName("family", ("jena", "kyle", "lily")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(1, ("alice", "bob", "catherine")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(1, ("diana", "erick", "frederick")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(1, ("gabby", "harry", "isaac")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(1, ("jena", "kyle", "lily")))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("family", (4, 5, 6)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("family", (7, 8, 9)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("family", (10, 11, 12)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("family", (13, 14, 15)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(1, (4, 5, 6)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(1, (7, 8, 9)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(1, (10, 11, 12)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(1, (13, 14, 15)))

        self.assertTrue(kb2.hasNamedRecordInRelationByName("mother", ("alice", "catherine")))
        self.assertTrue(kb2.hasNamedRecordInRelationByName("mother", ("diana", "frederick")))
        self.assertTrue(kb2.hasNamedRecordInRelationByName("mother", ("gabby", "isaac")))
        self.assertTrue(kb2.hasNamedRecordInRelationByName("mother", ("jena", "lily")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(2, ("alice","catherine")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(2, ("diana", "frederick")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(2, ("gabby", "isaac")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(2, ("jena", "lily")))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("mother", (4, 6)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("mother", (7, 9)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("mother", (10, 12)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("mother", (13, 15)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(2, (4, 6)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(2, (7, 9)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(2, (10, 12)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(2, (13, 15)))

        self.assertTrue(kb2.hasNamedRecordInRelationByName("father", ("bob", "catherine")))
        self.assertTrue(kb2.hasNamedRecordInRelationByName("father", ("erick", "frederick")))
        self.assertTrue(kb2.hasNamedRecordInRelationByName("father", ("harry", "isaac")))
        self.assertTrue(kb2.hasNamedRecordInRelationByName("father", ("marvin", "nataly")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(3, ("bob", "catherine")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(3, ("erick", "frederick")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(3, ("harry", "isaac")))
        self.assertTrue(kb2.hasNamedRecordInRelationByNumeration(3, ("marvin", "nataly")))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("father", (5, 6)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("father", (8, 9)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("father", (11, 12)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByName("father", (16, 17)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(3, (5, 6)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(3, (8, 9)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(3, (11, 12)))
        self.assertTrue(kb2.hasNumeratedRecordInRelationByNumeration(3, (16, 17)))

    def testCreateRelation(self):
        kb = NumeratedKb(KB_NAME, MEM_DIR)
        relation = kb.createRelation("rel", 2)

        self.assertEqual(18, kb.getNumerationMap().totalMappings())
        self.assertEqual(4, kb.totalRelations())
        self.assertEqual(12, kb.totalRecords())
        self.assertEqual("rel", relation.getName())
        self.assertEqual(2, relation.getArity())
        self.assertEqual(18, relation.getNumeration())
        self.assertEqual(0, relation.totalRecords())
        self.assertTrue(relation is kb.getRelationByName('rel'))
        self.assertTrue(relation is kb.getRelationByNumeration(18))

        kb.addNamedRecord2RelationByName("rel2", ('a', 'b', 'c'))
        kb.addNumeratedRecord2RelationByName('rel2', (4, 5, 6))

        self.assertEqual(22, kb.getNumerationMap().totalMappings())
        self.assertEqual(5, kb.totalRelations())
        self.assertEqual(14, kb.totalRecords())
        self.assertIsNotNone(kb.getRelationByName('rel2'))
        self.assertIsNotNone(kb.getRelationByNumeration(19))

    def testLoadRelation(self):
        kb = NumeratedKb(KB_NAME, MEM_DIR)
        tmp_file = getRelFilePath(MEM_DIR, "reflex", 2, 3)
        with open(tmp_file, 'wb') as ofd:
            ofd.write(struct.pack("<ii", 4, 4))
            ofd.write(struct.pack("<ii", 5, 5))
            ofd.write(struct.pack("<ii", 6, 6))
        TMP_FILES.append(tmp_file)
        relation = kb.loadRelation(MEM_DIR, "reflex", 2, 3)

        self.assertEqual(18, kb.getNumerationMap().totalMappings())
        self.assertEqual(4, kb.totalRelations())
        self.assertEqual(15, kb.totalRecords())
        self.assertEqual("reflex", relation.getName())
        self.assertEqual(2, relation.getArity())
        self.assertEqual(18, relation.getNumeration())
        self.assertEqual(3, relation.totalRecords())
        self.assertTrue(relation is kb.getRelationByName('reflex'))
        self.assertTrue(relation is kb.getRelationByNumeration(18))

        self.assertTrue(kb.hasNumeratedRecordInRelationByName("reflex", (4, 4)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("reflex", (5, 5)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("reflex", (6, 6)))

        tmp_file = getRelFilePath(MEM_DIR, "reflex2", 2, 3)
        with open(tmp_file, 'wb') as ofd:
            ofd.write(struct.pack("<ii", 7, 7))
            ofd.write(struct.pack("<ii", 99, 99))
            ofd.write(struct.pack("<ii", 8, 8))
        TMP_FILES.append(tmp_file)
        with self.assertRaises(KbException):
            relation = kb.loadRelation(MEM_DIR, "reflex2", 2, 3, True)

    def testDeleteRelation(self):
        kb = NumeratedKb(KB_NAME, MEM_DIR)

        kb.deleteRelation(1)

        self.assertEqual(KB_NAME, kb.getName())
        self.assertEqual(17, kb.getNumerationMap().totalMappings())
        self.assertEqual(2, len(kb.getRelationSet()))
        self.assertEqual(8, kb.totalRecords())

        self.assertFalse(kb.hasNamedRecordInRelationByName("family", ("alice", "bob", "catherine")))
        self.assertFalse(kb.hasNamedRecordInRelationByName("family", ("diana", "erick", "frederick")))
        self.assertFalse(kb.hasNamedRecordInRelationByName("family", ("gabby", "harry", "isaac")))
        self.assertFalse(kb.hasNamedRecordInRelationByName("family", ("jena", "kyle", "lily")))
        self.assertFalse(kb.hasNamedRecordInRelationByNumeration(1, ("alice", "bob", "catherine")))
        self.assertFalse(kb.hasNamedRecordInRelationByNumeration(1, ("diana", "erick", "frederick")))
        self.assertFalse(kb.hasNamedRecordInRelationByNumeration(1, ("gabby", "harry", "isaac")))
        self.assertFalse(kb.hasNamedRecordInRelationByNumeration(1, ("jena", "kyle", "lily")))
        self.assertFalse(kb.hasNumeratedRecordInRelationByName("family", (4, 5, 6)))
        self.assertFalse(kb.hasNumeratedRecordInRelationByName("family", (7, 8, 9)))
        self.assertFalse(kb.hasNumeratedRecordInRelationByName("family", (10, 11, 12)))
        self.assertFalse(kb.hasNumeratedRecordInRelationByName("family", (13, 14, 15)))
        self.assertFalse(kb.hasNumeratedRecordInRelationByNumeration(1, (4, 5, 6)))
        self.assertFalse(kb.hasNumeratedRecordInRelationByNumeration(1, (7, 8, 9)))
        self.assertFalse(kb.hasNumeratedRecordInRelationByNumeration(1, (10, 11, 12)))
        self.assertFalse(kb.hasNumeratedRecordInRelationByNumeration(1, (13, 14, 15)))

        self.assertTrue(kb.hasNamedRecordInRelationByName("mother", ("alice", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("mother", ("diana", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("mother", ("gabby", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("mother", ("jena", "lily")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(2, ("alice","catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(2, ("diana", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(2, ("gabby", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(2, ("jena", "lily")))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("mother", (4, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("mother", (7, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("mother", (10, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("mother", (13, 15)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(2, (4, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(2, (7, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(2, (10, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(2, (13, 15)))

        self.assertTrue(kb.hasNamedRecordInRelationByName("father", ("bob", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("father", ("erick", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("father", ("harry", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByName("father", ("marvin", "nataly")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(3, ("bob", "catherine")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(3, ("erick", "frederick")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(3, ("harry", "isaac")))
        self.assertTrue(kb.hasNamedRecordInRelationByNumeration(3, ("marvin", "nataly")))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("father", (5, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("father", (8, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("father", (11, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByName("father", (16, 17)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(3, (5, 6)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(3, (8, 9)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(3, (11, 12)))
        self.assertTrue(kb.hasNumeratedRecordInRelationByNumeration(3, (16, 17)))

    def testAddRecord(self):
        kb = NumeratedKb(KB_NAME, MEM_DIR)

        kb.addNamedRecord2RelationByName("family", ("o", "p", "q"))
        kb.addNamedRecord2RelationByNumeration(1, ("o", "o", "o"))
        self.assertEqual(19, kb.mapName("p"))
        kb.addNumeratedRecord2RelationByName("family", (19, 19, 19))
        self.assertEqual(20, kb.mapName("q"))
        kb.addNumeratedRecord2RelationByNumeration(1, (20, 20, 20))

        self.assertEqual(20, kb.getNumerationMap().totalMappings())
        self.assertEqual(3, kb.totalRelations())
        self.assertEqual(16, kb.totalRecords())
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('o', 'p', 'q')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('o', 'o', 'o')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('p', 'p', 'p')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('q', 'q', 'q')))

        kb.addNamedRecord2RelationByName("family", ("o", "o", "o"))
        with self.assertRaises(KbException):
            kb.addNamedRecord2RelationByName("family", ("o",))
        with self.assertRaises(KbException):
            kb.addNamedRecord2RelationByNumeration(1, ("o",))
        with self.assertRaises(KbException):
            kb.addNumeratedRecord2RelationByName("family", (18,))
        with self.assertRaises(KbException):
            kb.addNumeratedRecord2RelationByNumeration(1, (18,))
        with self.assertRaises(KbException):
            kb.addNumeratedRecord2RelationByNumeration(1, (200, 20, 20))

        self.assertEqual(20, kb.getNumerationMap().totalMappings())
        self.assertEqual(3, kb.totalRelations())
        self.assertEqual(16, kb.totalRecords())

    def testAddRecords(self):
        kb = NumeratedKb(KB_NAME, MEM_DIR)

        kb.addNamedRecords2RelationByName("family", [("o", "o", "o"), ("oo", "oo", "oo")])
        kb.addNamedRecords2RelationByNumeration(1, [("p", "p", "p"), ("pp", "pp", "pp")])
        self.assertEqual(22, kb.mapName("q"))
        self.assertEqual(23, kb.mapName("qq"))
        kb.addNumeratedRecords2RelationByName("family", [(22, 22, 22), (23, 23, 23)])
        self.assertEqual(24, kb.mapName("r"))
        self.assertEqual(25, kb.mapName("rr"))
        kb.addNumeratedRecords2RelationByNumeration(1, [(24, 24, 24), (25, 25, 25)])

        self.assertEqual(25, kb.getNumerationMap().totalMappings())
        self.assertEqual(3, kb.totalRelations())
        self.assertEqual(20, kb.totalRecords())
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('o', 'o', 'o')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('p', 'p', 'p')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('q', 'q', 'q')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('r', 'r', 'r')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('oo', 'oo', 'oo')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('pp', 'pp', 'pp')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('qq', 'qq', 'qq')))
        self.assertTrue(kb.hasNamedRecordInRelationByName('family', ('rr', 'rr', 'rr')))

        kb.addNamedRecords2RelationByName("family", [("o", "o", "o")])
        with self.assertRaises(KbException):
            kb.addNamedRecords2RelationByName("family", [("o",)])
        with self.assertRaises(KbException):
            kb.addNamedRecords2RelationByNumeration(1, [("o",)])
        with self.assertRaises(KbException):
            kb.addNumeratedRecords2RelationByName("family", [(18,)])
        with self.assertRaises(KbException):
            kb.addNumeratedRecords2RelationByNumeration(1, [(18,)])
        with self.assertRaises(KbException):
            kb.addNumeratedRecords2RelationByNumeration(1, [(200, 20, 20)])

        self.assertEqual(25, kb.getNumerationMap().totalMappings())
        self.assertEqual(3, kb.totalRelations())
        self.assertEqual(20, kb.totalRecords())

    def testRemoveRecord(self):
        kb = NumeratedKb(KB_NAME, MEM_DIR)

        kb.removeNamedRecordFromRelationByName("mother", ("alice", "catherine"))
        kb.removeNamedRecordFromRelationByNumeration(2, ("diana", "frederick"))
        kb.removeNumeratedRecordFromRelationByName("father", (0xb, 0xc))
        kb.removeNumeratedRecordFromRelationByNumeration(3, (0x10, 0x11))

        self.assertEqual(17, kb.getNumerationMap().totalMappings())
        self.assertEqual(3, kb.totalRelations())
        self.assertEqual(8, kb.totalRecords())

        kb.removeNamedRecordFromRelationByName("mother", ("alice", "catherine"))
        kb.removeNamedRecordFromRelationByNumeration(2, ("diana", "frederick"))
        kb.removeNumeratedRecordFromRelationByName("father", (0xb, 0xc))
        kb.removeNumeratedRecordFromRelationByNumeration(3, (0x10, 0x11))

        self.assertEqual(17, kb.getNumerationMap().totalMappings())
        self.assertEqual(3, kb.totalRelations())
        self.assertEqual(8, kb.totalRecords())

        kb.removeNamedRecordFromRelationByName("rel", ("alice", "catherine"))
        kb.removeNamedRecordFromRelationByNumeration(5, ("diana", "frederick"))
        kb.removeNumeratedRecordFromRelationByName("father", (0xafa, 0xc))
        kb.removeNumeratedRecordFromRelationByNumeration(28, (0x11, 0x123))

        self.assertEqual(17, kb.getNumerationMap().totalMappings())
        self.assertEqual(3, kb.totalRelations())
        self.assertEqual(8, kb.totalRecords())

if __name__ == '__main__':
    unittest.main()