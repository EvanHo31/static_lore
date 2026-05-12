import unittest
from conversion import text_node_to_html_node, text_to_text_nodes, markdown_to_blocks, markdown_to_html_node
from textnode import TextNode, TextType

class Test_test_node_to_html_node(unittest.TestCase):
    def test_invalid_text_type(self):
        node = TextNode("", -10)
        self.assertRaises(TypeError, lambda:text_node_to_html_node(node))

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "some/url/to/somewhere")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href":"some/url/to/somewhere"})
    
    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "some/url/to/somewhere")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"some/url/to/somewhere","alt":"This is a text node"})

class Test_Text_To_TextNode(unittest.TestCase):
    def test(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expect = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_text_nodes(text), expect)
    
    def test_nested(self):
        text = "This is **text with an _italic_** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expect = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text with an _italic_", TextType.BOLD),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_text_nodes(text), expect)
    
    def test_pure_text(self):
        text = "This is pure text"
        expect = [
            TextNode("This is pure text", TextType.TEXT),
        ]
        self.assertEqual(text_to_text_nodes(text), expect)
    
    def test_empty_str(self):
        expect = []
        self.assertEqual(text_to_text_nodes(""), expect)


class Test_Markdown_Converstion(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_with_extra_newlines(self):
        md = """
        This is **bolded** paragraph
 
        

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class Test_Markdown_To_HTML_Node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headerblock(self):
        md = """
# This is text that _should_ remain
the **same** even with inline stuff
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is text that <i>should</i> remain\nthe <b>same</b> even with inline stuff</h1></div>",
        )
    
    def test_headerblock_h4(self):
        md = """
#### This is text that _should_ remain
the **same** even with inline stuff
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>This is text that <i>should</i> remain\nthe <b>same</b> even with inline stuff</h4></div>",
        )

    def test_headerblock_fali(self):
        md = """
####### This is text that _should_ remain
the **same** even with inline stuff
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>####### This is text that <i>should</i> remain the <b>same</b> even with inline stuff</p></div>",
        )
    
    def test_quoteblock(self):
        md = """
>This is text that _should_ remain
> the **same** even with inline stuff
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is text that <i>should</i> remain</p><p> the <b>same</b> even with inline stuff</p></blockquote></div>",
        )

    def test_ulist_block(self):
        md = """
- This is text that _should_ remain
-  the **same** even with inline stuff
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is text that <i>should</i> remain</li><li> the <b>same</b> even with inline stuff</li></ul></div>",
        )
    
    def test_olist_block(self):
        md = """
1. This is text that _should_ remain
2.  the **same** even with inline stuff
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is text that <i>should</i> remain</li><li> the <b>same</b> even with inline stuff</li></ol></div>",
        )