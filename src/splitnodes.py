from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType):
    if not delimiter:
        raise ValueError("cannot split with empty delimiter")
    new_nodes = []
    for node in old_nodes:
        node:TextNode
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        splited = node.text.split(delimiter)
        # delimiter not found
        if len(splited) == 1:
            raise ValueError(f"delimiter {delimiter} not found in {node.text}")
        # missing closing delimiter
        if len(splited)%2 == 0:
            raise ValueError(f"invalid markdown, closing delimiter {delimiter} not found")
        is_block = False
        for part in splited:
            if part == "":
                pass
            elif not is_block:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
            is_block = not is_block
    return new_nodes
