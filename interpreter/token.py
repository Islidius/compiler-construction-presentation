from enum import Enum

class Kind(Enum):
    """This enum describes the different token kinds"""
    
    NUMBER = 1
    STRING = 2
    TRUE = 3
    FALSE = 4

    IDENT = 5

    LET = 6
    IF = 7
    WHILE = 8
    PRINT = 9
    READINT = 10

    PLUS = 11
    MINUS = 12
    MULT = 13
    DIV = 14
    LBRACKET = 15
    RBRACKET = 16
    LCURLY = 17
    RCURLY = 18
    EQUALS = 19
    BANG = 20
    SEMICOLON = 21

    CMPEQ = 22
    CMPNOTEQ = 23
    CMPLESS = 24
    CMPLESSEQ = 25
    CMPGREATER = 26
    CMPGREATEREQ = 27

    EOF = 38
    LOAD = 39
    EXEC = 40


class Token(object):
    """This class contains the data about a single token"""

    def __init__(self, kind, line = 0, value=None):
        self.kind = kind
        self.value = value
        self.line = line

    def __repr__(self):
        if(self.value):
            return "Token{%s, %s}" % (self.kind, self.value)
        else:
            return "Token{%s}" % (self.kind)
