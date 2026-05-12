import unittest
from extraction import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link
from extraction import extract_title
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
        new_nodes = split_nodes_delimiter([node], "_",TextType.TEXT)
        self.assertEqual(new_nodes, [node])

class Test_ExtractMarkdown(unittest.TestCase):

    def test_no_link(self):
        matches = extract_markdown_links(
            "This is text with an [link]https://i.imgur.com/zjjcJKZ.png"
        )
        self.assertListEqual([], matches)
    
    def test_extract_link_with_image(self):
        matches = extract_markdown_links(
            "This is text with an ![link]https://i.imgur.com/zjjcJKZ.png"
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
    
    def test_extract_image_with_link(self):
        matches = extract_markdown_images(
            "This is text with an [image]https://i.imgur.com/zjjcJKZ.png"
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

class Test_Split_Image(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_trailing_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and nothing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and nothing", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_no_image(self):
        node = TextNode(
            "This is text with no image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image", TextType.TEXT),
            ],
            new_nodes,
        )

class Test_Split_Link(unittest.TestCase):
    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_trailing_text(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and nothing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and nothing", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_no_link(self):
        node = TextNode(
            "This is text with no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no link", TextType.TEXT),
            ],
            new_nodes,
        )

class Test_Extract_Title(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, "Hello")
    
    def test_extract_title_1(self):
        md = """
html body
## not a title
# Hello
#not a title
"""
        title = extract_title(md)
        self.assertEqual(title, "Hello")

    def test_exception(self):
        md = "no title"
        self.assertRaises(Exception, lambda: extract_title(md))