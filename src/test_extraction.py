import unittest
from extraction import split_nodes_delimiter, extract_markdown_links, extract_markdown_images
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


class Test_ExtractMarkdown(unittest.TestCase):
    def test_no_link(self):
        matches = extract_markdown_links(
            "This is text with an [link]https://i.imgur.com/zjjcJKZ.png"
        )
        self.assertListEqual([], matches)

    def test_one_link(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_two_links(self):
        matches = extract_markdown_links(
            "This is text with an [link1](https://i.imgur.com/zjjcJKZ.png) and [link2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link1", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_no_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image]https://i.imgur.com/zjjcJKZ.png"
        )
        self.assertListEqual([], matches)

    def test_one_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_two_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)