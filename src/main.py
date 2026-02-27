from textnode import TextNode, TextType

def main():
    text_class = TextNode("Lets see if this works", TextType.HYPERLINK, "https://github.com/DMcmac/Dansite" )
    print(text_class)

main()

