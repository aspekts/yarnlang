class Position:
    def __init__(self,index,line,column,fn,filetext):
        """
        The function takes in a string and returns a list of tokens
        
        :param index: the current index of the filetext
        :param line: the line number of the current character
        :param column: the column number of the current character
        :param fn: file name
        :param filetext: the text of the file
        """
        self.idx = index
        self.fn = fn
        self.ftxt = filetext
        self.ln = line
        self.col = column
    def advance(self, current_char=None):
        """
        The function advances the index of the text by one, and if the current character is a newline, it
        advances the line number by one and resets the column number to zero
        
        :param current_char: The current character in the input string
        :return: The current instance of the class.
        """
        self.idx +=1
        self.col +=1
        if current_char == '\n':
            self.ln +=1
            self.col = 0
        return self
    def copy(self):
        """
        It returns a new Position object with the same values as the current object
        :return: A Position object.
        """
        return Position(self.idx,self.ln,self.col,self.fn,self.ftxt)