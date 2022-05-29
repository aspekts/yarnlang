from tokens import *
from position import Position
from error import IllegalCharError
# The Lexer class is used to tokenize the input text
class Lexer:
    def __init__(self,fn,text):
        self.fn = fn # Name of File being Lexed
        self.text = text # Text to be lexed
        self.pos = Position(-1,0,-1,self.fn,text) # Position of character in Lexer
        self.current_char = None # Current Character being Lexed
        self.advance() # Increments next char
    def advance(self):
        """
        It advances to the next character in the text and verifies if there is more characters to process
        """
        self.pos.advance(self.current_char) # Advances to next char
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None # Verifies there is more characters, if none process ends
    # Creates Tokens for each operator
    def make_tokens(self):
        """
        It takes the current character and checks if it's a digit, a plus sign, a minus sign, a
        multiplication sign, a division sign, a left parenthesis, a right parenthesis, or an illegal
        character. If it's a digit, it calls the make_numbers function. If it's a plus sign, it appends a
        token with the type TT_PLUS to the tokens list. If it's a minus sign, it appends a token with the
        type TT_MINUS to the tokens list. If it's a multiplication sign, it appends a token with the type
        TT_MUL to the tokens list. If it's a division sign, it appends a token with the type TT_DIV to
        the tokens list. If it's a left parenthesis, it appends a token with the type TT_LPAREN to the
        tokens list. If it's a right parenthesis, it appends a token with the type TT_RPAR
        :return: The tokens and the error.
        """
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t': # Skips Tabs and Spaces
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_numbers())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS,pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS,pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL,pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV,pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN,pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN,pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start,self.pos,f"'{char}'")
        tokens.append(Token(TT_EOF,pos_start=self.pos))
        return tokens, None
        # Converts Integers and Floats into appendable tokens
    def make_numbers(self):
        """
        It takes a string of numbers and returns a token of type TT_INT if there are no decimal points,
        and TT_FLOAT if there are
        :return: The token type, the value, the position start, and the position end.
        """
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char ==".":
                if dot_count ==1: break
                dot_count+=1
                numstr+= "."
            else:
                    num_str += self.current_char
                    self.advance()
            if dot_count == 0:
                return Token(TT_INT, int(num_str),pos_start,self.pos)
            else:
                return Token(TT_FLOAT, float(num_str),pos_start,self.pos)