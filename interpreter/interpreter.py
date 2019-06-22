from .ast import *
from .token import Kind, Token
from .parser import Parser
from .lexer import Lexer
from .error import NameNotFoundError, FileCouldNotBeLoaded

class Environment(object):
    """this class is the environment for a interpreter"""

    def __init__(self):
        self.stack = [{}]

    def push(self):
        """push a new stack frame"""
        self.stack.append({})

    def pop(self):
        """pop a stack frame"""
        self.stack.pop()

    def getValue(self, name):
        """get the value, searching all stack frames"""
        for frame in reversed(self.stack):
            if(name in frame):
                return frame[name]
        raise NameNotFoundError(name)

    def setValue(self, name, value):
        """set a value, searching all stack frames"""
        for frame in reversed(self.stack):
            if(name in frame):
                frame[name] = value
                return
        raise NameNotFoundError(name)

    def initValue(self, name):
        """init a variable in the current frame"""
        self.stack[-1][name] = None


class Interpreter(object):
    """this class interpretes an ast using an environment for variables
    
    this class uses a visitor pattern to access the ast"""
    def __init__(self, ast, env):
        self.ast = ast
        self.env = env

    def eval(self):
        """eval the ast returning its result or None"""
        return self.ast.visit(self)

    def visitScope(self, scope):
        """visit a scope node"""
        self.env.push()
        for stmt in scope.stmts:
            r = stmt.visit(self)
        self.env.pop()
        return None

    def visitIf(self, ifa):
        """visit a if node"""
        if(ifa.condition.visit(self)):
            ifa.scope.visit(self)
        return None
    
    def visitWhile(self, whilea):
        """visit a while node"""
        while(whilea.condition.visit(self)):
            whilea.scope.visit(self)
        return None

    def visitPrint(self, p):
        """visit a print node"""
        print(p.expr.visit(self))
        return None

    def visitLoad(self, load):
        """visit a load node"""

        # calculate the expression for the filename
        name = load.expr.visit(self)
        try:
            with open(name) as f:
                # lex, parse, interprete the file
                l = Lexer(f.read())
                p = Parser(l.lexTokens())
                i = Interpreter(p.parse(), self.env)
                return i.eval()
        except FileNotFoundError:
            raise FileCouldNotBeLoaded(name)
        return None

    def visitExec(self, exe):
        """visit a exec node"""

        # calculate the expression for the code
        expr = exe.expr.visit(self)

        # lex, parse, interprete the code
        l = Lexer(expr)
        p = Parser(l.lexTokens())
        i = Interpreter(p.parse(), self.env)
        return i.eval()

    def visitAssign(self, assign):
        """visit an assign node"""

        # set the value using the environment
        self.env.setValue(assign.name.value, assign.expr.visit(self))
        return None

    def visitDeclaration(self, decl):
        """visit a declaration node"""

        # init the variable using the environment
        self.env.initValue(decl.name.value)

        # set the value if present
        if(decl.expr):
            self.env.setValue(decl.name.value, decl.expr.visit(self))
        return None

    def visitBinary(self, binary):
        """visit a binary expression"""

        # calculate the result of the left and right expression
        left = binary.left.visit(self)
        right = binary.right.visit(self)

        # choose which operator to use
        if(binary.operator.kind == Kind.PLUS):
            # allow for string concatenation
            if(type(left) == str and type(right) == int):
                return left + str(right)
            elif(type(left) == int and type(right) == str):
                return str(left) + right
            else:
                return left + right
        elif(binary.operator.kind == Kind.MINUS):
            return left - right
        elif(binary.operator.kind == Kind.MULT):
            return left * right
        elif(binary.operator.kind == Kind.DIV):
            return left / right
        elif(binary.operator.kind == Kind.CMPEQ):
            return left == right
        elif(binary.operator.kind == Kind.CMPNOTEQ):
            return left != right
        elif(binary.operator.kind == Kind.CMPLESS):
            return left < right
        elif(binary.operator.kind == Kind.CMPLESSEQ):
            return left <= right
        elif(binary.operator.kind == Kind.CMPGREATER):
            return left > right
        elif(binary.operator.kind == Kind.CMPGREATEREQ):
            return left >= right

        return None

    def visitUnary(self, unary):
        """visit a unary expression"""

        # calculate the expression
        expr = unary.expr.visit(self)

        # apply the unary operator
        if(unary.operator.kind == Kind.MINUS):
            return - expr
        elif(unary.operator.kind == Kind.BANG):
            return not expr
        elif(unary.operator.kind == Kind.PLUS):
            return expr
        return None

    def visitLiteral(self, literal):
        """visit a literal node"""

        # return the value of this node
        if(literal.value.kind in [Kind.NUMBER, Kind.STRING]):
            return literal.value.value
        elif(literal.value.kind == Kind.TRUE):
            return True
        elif(literal.value.kind == Kind.FALSE):
            return False
        elif(literal.value.kind == Kind.IDENT):
            # get the value from the environment
            return self.env.getValue(literal.value.value)
        return None
