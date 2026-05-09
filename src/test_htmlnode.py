import unittest
from htmlnode import HTMLNode

class Test_HTMLNode(unittest.TestCase):
    def test_none(self):
        node = HTMLNode()
        expect = "HTMLNode(None, None, None, None)"
        self.assertEqual(str(node), expect)
    
    def test_set(self):
        node = HTMLNode('p', '1234', [], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        expect = "HTMLNode(p, 1234, [], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(str(node), expect)
    
    def test_props(self):
        node = HTMLNode('p', '1234', [], {
                "href": "https://www.google.com",
                "target": "_blank",
            })
        test = node.props_to_html()
        expect = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(test, expect)
    
    def test_tohtml(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)