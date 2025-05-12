import unittest

from htmlnode import HTMLNode 
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_all_none(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected = " href=\"https://www.google.com\" target=\"_blank\""
        node = HTMLNode(props=props)

        self.assertEqual(node.props_to_html(), expected)

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_paragraph(self):
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode(tag="a", 
        value="I am a link", props={"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">I am a link</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

   
if __name__ == "__main__":
    unittest.main()