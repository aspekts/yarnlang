# The class NumberNode is a class that has a constructor that takes a token as an argument and assigns
# it to the instance variable tok. It also has a method called __repr__ that returns the value of the
# instance variable tok
class NumberNode:
    def __init__(self,tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self):
        return f"{self.tok}"
# The BinaryOpNode class is a class that takes in a left node, an operator token, and a right node,
# and returns a string representation of the left node, the operator token, and the right node
class BinaryOpNode:
    def __init__(self,left_node,op_token,right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.op_token = op_token
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end
    def __repr__(self):
        return f"({self.left_node}, {self.op_token}, {self.right_node})"
# The UnaryOpNode class is a class that takes in a token and a node and returns a string
# representation of the token and the node
class UnaryOpNode:
    def __init__(self,op_token,node):
        self.op_token = op_token
        self.node = node
        self.pos_start = self.op_token.pos_start
        self.pos_end = self.node.pos_end
    def __repr__(self):
        return f"{self.op_token}, {self.node}"