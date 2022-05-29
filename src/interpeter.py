from tokens import *
from values import *
from runtime import RTResult
class Interpreter:
    def visit(self,node):
        """
        The visit function is a generic function that takes a node as an argument and calls the
        appropriate visit method based on the type of the node
        
        :param node: The node to visit
        :return: The return value is the result of the visit method.
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self,method_name,self.novisitmethod)
        return method(node)
    def novisitmethod(self,node):
        """
        If the method `visit_<type(node).__name__>` is not defined, then raise an exception
        
        :param node: The node that is being visited
        """
        raise Exception(f'No visit_{type(node).__name__} method defined.')
    
    def visit_NumberNode(self,node):
        """
        The function takes a node as an argument and prints "Number Node found" if the node is a NumberNode
        
        :param node: The node that is being visited
        """
        return RTResult().success(Number(node.tok.value).set_pos(node.pos_start,node.pos_end))
    def visit_BinaryOpNode(self,node):
        """
        The function takes a node as an argument, and then visits the left and right nodes of the node
        
        :param node: The node that is being visited
        """
        res = RTResult()
        left = res.register(self.visit(node.left_node))
        if res.error: return res
        right = res.register(self.visit(node.right_node))
        if res.error: return res
        if node.op_token.type == TT_PLUS:
            result,error = left.added_to(right)
        elif node.op_token.type == TT_MINUS:
            result,error = left.subtracted_by(right)
        elif node.op_token.type == TT_MUL:
            result,error = left.multiplied_by(right)
        elif node.op_token.type == TT_DIV:
            result,error = left.divided_by(right)
        if error: return res.failure(error)
        else: return res.success(result.set_pos(node.pos_start,node.pos_end))
    def visit_UnaryOpNode(self,node):
        """
        The function takes a node as an argument, and then visits the node's child node
        
        :param node: The node to visit
        """
        res = RTResult()
        number = res.register(self.visit(node.node))
        if res.error: return res
        if node.op_token.type == TT_MINUS:
            number,error = number.multed_by(Number(-1))
        if error: return res.failure(error)
        else: return res.successs(number.set_pos(node.pos_start,node.pos_end))