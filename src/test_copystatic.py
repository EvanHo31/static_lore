import unittest
from copystatic import get_treemap

class Test_CopyStatic(unittest.TestCase):
    def test_get_treemap(self):
        treemap = get_treemap("static")
        expect = {"images":{"tolkien.png":None}, "index.css":None}
        self.assertEqual(treemap, expect)