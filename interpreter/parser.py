from .token import Kind, Token
from .ast import *
from .error import ParseError

class Parser(object):
    """this class parses a list of tokens into an ast"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def peek(self):
        """return the current token"""
        return self.tokens[self.index]

    def next(self):
        """return the current token and advance"""
        self.index += 1
        return self.tokens[self.index - 1]

    def has(self):
        """check if there are more no EOF tokens"""
        return self.peek().kind != Kind.EOF

    def test(self, *args):
        """test if the current token matches args, if so return it and advance
        if not return None"""

        kind = self.peek().kind
        for other in args:
            if(kind == other):
                return self.next()
        return None

    def consume(self, *args):
        """check if the current token matches args, if so return it and advance
        if not raise an Error"""

        kind = self.peek().kind
        for other in args:
            if(kind == other):
                return self.next()
        raise ParseError

    def parse(self):
        """parse the complete code
        
        code = statement*"""

        # place the complete code into a Scope
        ast = Scope()
        while(self.has()):
            ast.add(self.parseStatement())

        # all programms end in EOF
        self.consume(Kind.EOF)

        # if the scope contains only one stmt return it
        if(len(ast.stmts) == 1):
            return ast.stmts[0]
        return ast

    def parseStatement(self):
        """parse a single statement

        statement = let | scope | if | while | print | load | exec | expressionstmt"""

        # peek the kind in order to determine which type it is
        kind = self.peek().kind
        if(kind == Kind.LET):
            return self.parseLet()
        elif(kind == Kind.LCURLY):
            return self.parseScope()
        elif(kind == Kind.IF):
            return self.parseIf()
        elif(kind == Kind.WHILE):
            return self.parseWhile()
        elif(kind == Kind.PRINT):
            return self.parsePrint()
        elif(kind == Kind.LOAD):
            return self.parseLoad()
        elif(kind == Kind.EXEC):
            return self.parseExec()
        else:
            return self.parseExpressionStmt()
        
    def parseLet(self):
        """parse a single let statement

        let = LET IDENT (EQUALS expression)? SEMICOLON"""

        # they all start with let and ident
        self.consume(Kind.LET)
        ident = self.consume(Kind.IDENT)
        expr = None

        # test if the next token is EQUALS, then parse the expression
        if(self.test(Kind.EQUALS)):
            expr = self.parseExpression()

        # consume the trailing semicolo
        self.consume(Kind.SEMICOLON)
        return Declaration(ident, expr)

    def parseScope(self):
        """parse a single scope

        scope = LCURLY statement* RCURLY"""

        ast = Scope()

        # they start with a lcurly
        self.consume(Kind.LCURLY)

        # parse statements until closing bracket
        while(self.has() and self.peek().kind != Kind.RCURLY):
            ast.add(self.parseStatement())

        # consume the closing bracket
        self.consume(Kind.RCURLY)
        return ast

    def parseIf(self):
        """parse a single if statement

        if = IF LBRACKET expression RBRACKET scope"""

        # consume if and the lbracket
        self.consume(Kind.IF)
        self.consume(Kind.LBRACKET)

        # parse the condition
        condition = self.parseExpression()

        # parse the closing bracket and the scope
        self.consume(Kind.RBRACKET)
        scope = self.parseScope()
        return If(condition, scope)

    def parseWhile(self):
        """parse a single while statement

        while = WHILE LBRACKET expression RBRACKET scope"""

        # consume while and the lbracket
        self.consume(Kind.WHILE)
        self.consume(Kind.LBRACKET)

        # parse the condition
        condition = self.parseExpression()

        # parse the closing bracket and the scope
        self.consume(Kind.RBRACKET)
        scope = self.parseScope()
        return While(condition, scope)

    def parsePrint(self):
        """parse a single print statement

        print = PRINT expression SEMICOLON"""

        # consume the print
        self.consume(Kind.PRINT)

        # parse the expression and trailing semicolon
        expr = self.parseExpression()
        self.consume(Kind.SEMICOLON)
        return Print(expr)

    def parseLoad(self):
        """parse a single load statement

        load = LOAD expression SEMICOLON"""

        # consume the load
        self.consume(Kind.LOAD)

        # parse the expression and trailing semicolon
        expr = self.parseExpression()
        self.consume(Kind.SEMICOLON)
        return Load(expr)

    def parseExec(self):
        """parse a single exec statement

        exec = EXEC expression SEMICOLON"""

        # consume the exec
        self.consume(Kind.EXEC)

        # parse the expression and trailing semicolon
        expr = self.parseExpression()
        self.consume(Kind.SEMICOLON)
        return Exec(expr)

    def parseExpressionStmt(self):
        """parse a single expression statement

        expressionstmt = assignment SEMICOLON"""

        # parse the assignment and the trailing semicolon
        ast = self.parseAssignment()
        self.consume(Kind.SEMICOLON)
        return ast

    def parseExpression(self):
        """parse a single expression (NOT ASSIGNMENT)

        expressionstmt = equality"""
        return self.parseEquality()

    def parseAssignment(self):
        """parse a possible assignment

        assignment = equality (EQUALS equality)"""
        expr = self.parseEquality()

        # test if there is an EQUALS operator
        operator = self.test(Kind.EQUALS)
        if(operator):
            right = self.parseEquality()
            expr = Assign(expr.value, right)

        return expr

    def parseEquality(self):
        """parse a equality expression

        equality = comparison ((CMPEQ | CMPNOTEQ) comparison)*"""
        expr = self.parseComparison()

        # while there are more operators
        operator = self.test(Kind.CMPEQ, Kind.CMPNOTEQ)
        while(operator):
            right = self.parseComparison()
            expr = Binary(operator, expr, right)
            operator = self.test(Kind.CMPEQ, Kind.CMPNOTEQ)

        return expr

    def parseComparison(self):
        """parse a comparison expression

        comparison = addition ((CMPGREATER | CMPGREATEREQ | CMPLESS | CMPLESSEQ) comparison)?"""
        expr = self.parseAddition()

        # test if a operator follows
        operator = self.test(Kind.CMPGREATER, Kind.CMPGREATEREQ, Kind.CMPLESS, Kind.CMPLESSEQ)
        if(operator):
            right = self.parseComparison()
            expr = Binary(operator, expr, right)

        return expr

    def parseAddition(self):
        """parse a addition expression

        addition = multiplication ((PLUS | MINUS) addition)?"""
        expr = self.parseMultiplication()

        # test if a operator follows
        operator = self.test(Kind.PLUS, Kind.MINUS)
        if(operator):
            right = self.parseAddition()
            expr = Binary(operator, expr, right)

        return expr

    def parseMultiplication(self):
        """parse a multiplication expression

        multiplication = unary ((MULT | DIV) multiplication)?"""
        expr = self.parseUnary()

        # test if a operator follows
        operator = self.test(Kind.MULT, Kind.DIV)
        if(operator):
            right = self.parseMultiplication()
            expr = Binary(operator, expr, right)

        return expr

    def parseUnary(self):
        """parse a unary expression

        unary = ((MINUS | PLUS | BANG) unary) | primary"""

        # if there is a unary operator
        operator = self.test(Kind.MINUS, Kind.PLUS, Kind.BANG)
        if(operator):
            return Unary(operator, self.parseUnary())
        # if there is no unary operator
        return self.parsePrimary()

    def parsePrimary(self):
        """parse a primary expression

        primary = NUMBER | STRING | TRUE | FALSE | IDENT | LBRACKET expression RBRACKET"""

        # peek the kind of primary expression
        kind = self.peek().kind
        if(kind in [Kind.NUMBER, Kind.STRING, Kind.TRUE, Kind.FALSE, Kind.IDENT]):
            # this is a literal
            return Literal(self.next())
        elif(kind == Kind.LBRACKET):
            # this is a grouped expression
            self.consume(Kind.LBRACKET)
            ast = self.parseExpression()
            self.consume(Kind.RBRACKET)
            return ast
        else:
            raise ParseError

