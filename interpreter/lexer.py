from .token import Kind, Token
from .error import LexerError

class Lexer(object):
    """This class converts a string to tokens"""

    # list of all digits
    digits = "0123456789"

    # list of all alphas
    alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    # list of all the keywords
    keywords = {
        "true" : Kind.TRUE,
        "false": Kind.FALSE,
        "let"  : Kind.LET,
        "if"   : Kind.IF,
        "while": Kind.WHILE,
        "print": Kind.PRINT,
        "read" : Kind.READINT,
        "load" : Kind.LOAD,
        "exec" : Kind.EXEC
    }

    # list of all single character
    singleChar = {
        "+": Kind.PLUS,
        "-": Kind.MINUS,
        "*": Kind.MULT,
        "/": Kind.DIV,
        "(": Kind.LBRACKET,
        ")": Kind.RBRACKET,
        "{": Kind.LCURLY,
        "}": Kind.RCURLY,
        ";": Kind.SEMICOLON
    }

    def __init__(self, code):
        self.code = code
        self.tokens = []

        self.index = 0
        self.start = 0
        self.line = 0

    def next(self):
        """return the current character and advance the index"""
        self.index += 1
        return self.code[self.index - 1]

    def peek(self):
        """return the current character, returns 0 if none are left"""
        if(not self.has()):
            return "\0"
        return self.code[self.index]

    def has(self):
        """return true if there are characters left"""
        return self.index < len(self.code)

    def ahead(self, char):
        """check if the current character equals char. if this is the case
        return True and advance the index, otherwise return False"""
        if(self.peek() != char):
            return False
        
        self.index += 1
        return True

    def getRange(self):
        """return the code range of the current lexeme"""
        return self.code[self.start : self.index]

    def addToken(self, kind, value = None):
        """add a new token, with the specified kind and optionally a value"""
        self.tokens.append(Token(kind, self.line, value))

    def lexTokens(self):
        """lex all the tokens and return the token list"""

        # iterate until no characters are left
        while(self.has()):
            # set the start index of the current lexeme
            self.start = self.index
            self.lexToken()
        
        # always add a end of file token in the end
        self.addToken(Kind.EOF)
        return self.tokens

    def lexToken(self):
        """lex a single token. This will not always add a token"""

        # read the first character of a token and advance
        char = self.next()
        if(char in " \r\t"):
            # we simply declare these as tokens
            pass
        elif(char == "\n"):
            # advance the line count
            self.line += 1
        elif(char in self.digits):
            # all numers start with a digit
            self.lexNumber()
        elif(char in self.alphas):
            # all keywords and identifier start with a alpha
            self.lexIdentifier()
        elif(char == "\""):
            # strings start with a quotation mark
            self.lexString()
        elif(char in self.singleChar):
            # this covers all tokens that are only a single character
            self.addToken(self.singleChar[char])
        elif(char == "="):
            # this will lex "=" and "=="
            self.addToken(Kind.CMPEQ if self.ahead("=") else Kind.EQUALS)
        elif(char == "!"):
            # this will lex "!" and "!="
            self.addToken(Kind.CMPNOTEQ if self.ahead("=") else Kind.BANG)
        elif(char == "<"):
            # this will lex "<" and "<="
            self.addToken(Kind.CMPLESSEQ if self.ahead("=") else Kind.CMPLESS)
        elif(char == ">"):
            # this will lex ">" and ">="
            self.addToken(Kind.CMPGREATEREQ if self.ahead("=") else Kind.CMPGREATER)
        else:
            # there are no tokens that start with the current character
            raise LexerError
    
    def lexNumber(self):
        """this will lex a single number. the first character is already read"""

        # loop until no digits are left in this number
        while(self.peek() in self.digits):
            self.next()

        # add a number token, with the range already converted to int
        self.addToken(Kind.NUMBER, int(self.getRange()))
    
    def lexIdentifier(self):
        """this will lex a single keyword or identifier"""

        # loop until no digits or alphas are left
        while(self.peek() in self.digits or self.peek() in self.alphas):
            self.next()

        # get the value of the current lexme
        value = self.getRange()

        # if this is a keyword add a keyword otherwise add a identifier
        if(value in self.keywords):
            self.addToken(self.keywords[value])
        else:
            self.addToken(Kind.IDENT, value)

    def lexString(self):
        """this will lex a string, the starting quote is already read"""

        # loop until the closing quote is reached
        while(self.peek() != "\"" and self.has()):
            self.next()
        
        # skip the closing quote
        self.next()

        # add a string token without the quotation marks
        value = self.code[self.start + 1 : self.index - 1]
        self.addToken(Kind.STRING, value)