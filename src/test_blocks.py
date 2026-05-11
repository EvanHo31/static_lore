import unittest
from blocks import block_to_block_type, BlockType

class Test_Block_To_Block_Type(unittest.TestCase):
    def test_paragraph(self):
        text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Mauris convallis nunc vel purus semper luctus.
In ac lorem vitae massa auctor pretium.
Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_heading(self):
        text = """#### Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Mauris convallis nunc vel purus semper luctus.
In ac lorem vitae massa auctor pretium.
Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
    
    def test_heading_no_space(self):
        text = """####Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Mauris convallis nunc vel purus semper luctus.
In ac lorem vitae massa auctor pretium.
Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_heading_extra_hash(self):
        text = """######## Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Mauris convallis nunc vel purus semper luctus.
In ac lorem vitae massa auctor pretium.
Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_code(self):
        text = """```
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Mauris convallis nunc vel purus semper luctus.
In ac lorem vitae massa auctor pretium.
Cras blandit justo at nisi lobortis condimentum.```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    
    def test_code_no_newline(self):
        text = """```Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Mauris convallis nunc vel purus semper luctus.
In ac lorem vitae massa auctor pretium.
Cras blandit justo at nisi lobortis condimentum.```"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_quote(self):
        text = """>
>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
>Mauris convallis nunc vel purus semper luctus.
>In ac lorem vitae massa auctor pretium.
>Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_quote_missing_arrow(self):
        text = """>
>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
>Mauris convallis nunc vel purus semper luctus.
In ac lorem vitae massa auctor pretium.
>Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        text = """- 
- Lorem ipsum dolor sit amet, consectetur adipiscing elit.
- Mauris convallis nunc vel purus semper luctus.
- In ac lorem vitae massa auctor pretium.
- Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_missing_dash(self):
        text = """-
-Lorem ipsum dolor sit amet, consectetur adipiscing elit.
-Mauris convallis nunc vel purus semper luctus.
In ac lorem vitae massa auctor pretium.
Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        text = """1. 
2. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
3. Mauris convallis nunc vel purus semper luctus.
4. In ac lorem vitae massa auctor pretium.
5. Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)
    
    def test_ordered_list_missing_no(self):
        text = """1. 
2. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
. Mauris convallis nunc vel purus semper luctus.
. In ac lorem vitae massa auctor pretium.
5. Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
    
    def test_ordered_list_wrong_sequence(self):
        text = """1. 
2. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
4. Mauris convallis nunc vel purus semper luctus.
3. In ac lorem vitae massa auctor pretium.
5. Cras blandit justo at nisi lobortis condimentum."""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)