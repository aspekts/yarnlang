"""
YarnLang - A Lightweight Language free from Compromise
"""
__version__ = "0.0.1"
from lexer import Lexer
from parser import Parser
from interpeter import Interpreter
def run(fn,text):
    """
    It takes a string of code, and returns the result of running that code
    
    :param fn: The name of the file
    :param text: The code to be run
    :return: None, None
    """
    lexer = Lexer(fn,text)
    tokens, error = lexer.make_tokens()
    if error: return None,error
    #Gen AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error
    # Code to run program
    interpreter = Interpreter()
    result =  interpreter.visit(ast.node)
    return result.value, result.error
