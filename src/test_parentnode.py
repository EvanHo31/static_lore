import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_some_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node]*3)
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child</span><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_some_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node]*2)
        parent_node = ParentNode("div", [child_node]*2)
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild</b></span><span><b>grandchild</b><b>grandchild</b></span></div>",
        )

    def test_with_children_with_props(self):
        child_node = LeafNode("img", "Image 1", {"src":"url/for/image.jpg","alt":"description of image"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><img src="url/for/image.jpg" alt="description of image">Image 1</img></div>')
    
    def test_with_props(self):
        child_node = LeafNode("img", "Image 1")
        parent_node = ParentNode("div", [child_node], {"src":"url/for/image.jpg","alt":"description of image"})
        self.assertEqual(parent_node.to_html(), '<div src="url/for/image.jpg" alt="description of image"><img>Image 1</img></div>')

    def test_no_tag(self):
        node = ParentNode('', [])
        self.assertRaises(ValueError, node.to_html)
    
    def test_no_children(self):
        node = ParentNode('', [])
        self.assertRaises(ValueError, node.to_html)
    