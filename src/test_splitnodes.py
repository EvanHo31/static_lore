import unittest
from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType

class Test_SplitNodes(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expect = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expect)
    
    def test_split_start_block(self):
        node = TextNode("`code block` exists in this node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expect = [
            TextNode("code block", TextType.CODE),
            TextNode(" exists in this node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expect)
    
    def test_split_end_block(self):
        node = TextNode("This is text with a `code block word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expect = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block word", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expect)
    
    def test_split_more_code(self):
        node = TextNode("This is text with a `code block` word, and a `second code block` too.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expect = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word, and a ", TextType.TEXT),
            TextNode("second code block", TextType.CODE),
            TextNode(" too.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expect)
    
    def test_split_multiple_nodes(self):
        node1 = TextNode("This is text with a `code block 1` word", TextType.TEXT)
        node2 = TextNode("This is text with a `code block 2` word", TextType.TEXT)
        node3 = TextNode("This is text with a `code block 3` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        expect = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block 1", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block 2", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block 3", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expect)
    
    def test_split_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
        expect = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.TEXT),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expect)
    
    def test_split_non_textnode(self):
        node = TextNode("This is text with a code block word", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expect = [
            TextNode("This is text with a code block word", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expect)
    
    def test_no_input_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        def test_func():
            split_nodes_delimiter([node], "", TextType.CODE)
        self.assertRaises(ValueError, test_func)
    
    def test_no_closing_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        def test_func():
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertRaises(ValueError, test_func)
    
    def test_no_delimiter(self):
        node = TextNode("This is text with a code block word", TextType.TEXT)
        def test_func():
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertRaises(ValueError, test_func)
    