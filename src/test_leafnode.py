import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_url(self):
        node = LeafNode("a", "click me", props={"href":"https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">click me</a>')
    
    def test_h1(self):
        node = LeafNode("h1", "Header Title")
        self.assertEqual(node.to_html(), '<h1>Header Title</h1>')
    
    def test_repr(self):
        node = LeafNode("a", "click me", props={"href":"https://google.com"})
        self.assertEqual(str(node), "LeafNode(a, click me, {'href': 'https://google.com'})")
    
    def test_notag_to_html(self):
        node = LeafNode("", "click me", props={"href":"https://google.com"})
        self.assertEqual(node.to_html(), "click me")