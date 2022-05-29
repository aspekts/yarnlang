from tokens import *
from nodes import *
from error import InvalidSyntaxError
# It's a container for the result of a parse
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
    def register(self,result):
        """
        A function that is used to register the result of a parse.
        
        :param result: the result of the parse
        :return: The result of the parse.
        """
        if isinstance(result, ParseResult):
            if result.error: self.error = result.error
            return result.node
        return result
    def success(self,node):
        """
        It takes a node as an argument and returns the node
        
        :param node: The node to be added to the tree
        :return: The node that is being passed in.
        """
        self.node = node
        return self
    def failiure(self,error):
        """
        The function takes in an error and returns the error
        
        :param error: The error message that will be displayed to the user
        :return: The object itself.
        """
        self.error = error
        return self

# The `Parser` class is a class that takes a list of tokens and parses them.
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()
    def advance(self):
        """
        It advances the token index by one and sets the current token to the next token in the list
        :return: The current token.
        """
        self.token_idx +=1
        if self.token_idx < len(self.tokens):
            self.current_tok = self.tokens[self.token_idx]
        return self.current_tok
    def parse(self):
        """
        The function checks if the current token is an operator, if it is, it returns the result of the
        expression, if it isn't, it returns an error
        :return: The result of the parse function is being returned.
        """
        result = self.expr()
        if not result.error and self.current_tok.type != TT_EOF:
            return result.failiure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end, "Expected Valid Operator:\n '*','+','/' or '-'"
            )) 
        return result
    def factor(self):
        """
        If the current token is a plus or minus, then advance the token and return a UnaryOpNode with
        the token and the factor
        :return: The result of the function is being returned.
        """
        res = ParseResult()
        token = self.current_tok
        if token.type in (TT_PLUS,TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token,factor))
        if token.type in TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr)
            if res.error: return res
            if self.current_tok.type in TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failiure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end, "Expected ')'"))

        elif token.type in (TT_INT,TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(token))
        return res.failiure(InvalidSyntaxError(token.pos_start,token.pos_end,"Expected Type Int or Float"))

    def term(self):
        """
        It takes a factor and a tuple of two token types (TT_MUL and TT_DIV) and returns a BinaryOp
        :return: The BinaryOp function is being returned.
        """
        return self.BinaryOp(self.factor,(TT_MUL, TT_DIV))
    def expr(self):
        """
        It takes in a function and a tuple of tokens, and returns a function that takes in a token stream
        and returns a node
        :return: The BinaryOp function is being returned.
        """
        return self.BinaryOp(self.term,(TT_PLUS, TT_MINUS))
    def BinaryOp(self,func,ops):
        """
        It takes a function as an argument, and calls that function, and then checks if the current
        token is in the list of operators, and if it is, it advances the token, calls the function
        again, and then creates a BinaryOpNode with the left and right values
        
        :param func: The function that will be called to parse the expression on the right side of the
        operator
        :param ops: a list of token types that the operator can be
        :return: The result of the function.
        """
        res = ParseResult()
        left = res.register(func())
        if res.error: return res
        while self.current_tok.type in ops:
            op_token = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinaryOpNode(left,op_token,right)
        return res.success(left)

