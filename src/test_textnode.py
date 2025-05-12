import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_has_link(self):
        node = TextNode("Awesome Site", TextType.LINK, "awesomesite.com")
        self.assertIsNotNone(node.url)

    def test_has_no_link(self):
        node = TextNode("Awesome Site", TextType.LINK)
        self.assertIsNone(node.url)

    def test_normal_text_type(self):
        node = TextNode("this is normal text", TextType.TEXT)
        self.assertEqual(node.type, TextType.TEXT)

    def test_bold_text_type(self):
        node = TextNode("**this is bold text**", TextType.BOLD)
        self.assertEqual(node.type, TextType.BOLD)

    def test_italic_text_type(self):
        node = TextNode("_this is italic text_", TextType.ITALIC)
        self.assertEqual(node.type, TextType.ITALIC)

    def test_code_text_type(self):
        node = TextNode("```this is normal text```", TextType.CODE)
        self.assertEqual(node.type, TextType.CODE)

    def test_link_text_type(self):
        node = TextNode("this is [link](example.com) text", TextType.LINK)
        self.assertEqual(node.type, TextType.LINK)

    def test_image_text_type(self):
        node = TextNode("![this is normal text](./img.png)", TextType.IMAGE)
        self.assertEqual(node.type, TextType.IMAGE)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


   
if __name__ == "__main__":
    unittest.main()