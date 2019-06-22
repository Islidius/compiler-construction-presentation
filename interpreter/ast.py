class Scope(object):
    """this is the ast node for a scope, contains a list of statements"""

    def __init__(self):
        self.stmts = []

    def add(self, stmt):
        self.stmts.append(stmt)

    def __repr__(self):
        return "Scope{%s}" % (self.stmts)

    def visit(self, visitor):
        return visitor.visitScope(self)

class Declaration(object):
    """this is the ast node for a declaration, contains the name and expression"""

    def __init__(self, name, expr = None):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return "Decl{%s, %s}" % (self.name, self.expr)

    def visit(self, visitor):
        return visitor.visitDeclaration(self)

class If(object):
    """this is the ast node for if, contains the condition and the scope"""

    def __init__(self, condition, scope):
        self.condition = condition
        self.scope = scope

    def __repr__(self):
        return "If{%s, %s}" % (self.condition, self.scope)
    
    def visit(self, visitor):
        return visitor.visitIf(self)

class While(object):
    """this is the ast node for while, contains the condition and the scope"""

    def __init__(self, condition, scope):
        self.condition = condition
        self.scope = scope

    def __repr__(self):
        return "While{%s, %s}" % (self.condition, self.scope)
    
    def visit(self, visitor):
        return visitor.visitWhile(self)

class Print(object):
    """this is the ast node for print, contains the expression"""

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "Print{%s}" % (self.expr)

    def visit(self, visitor):
        return visitor.visitPrint(self)

class Load(object):
    """this is the ast node for load, contains the expression"""

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "Load{%s}" % (self.expr)

    def visit(self, visitor):
        return visitor.visitLoad(self)

class Exec(object):
    """this is the ast node for exec, contains the expression"""

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "Exec{%s}" % (self.expr)

    def visit(self, visitor):
        return visitor.visitExec(self)

class Assign(object):
    """this is the ast node for assign, contains the name and expression"""

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return "Assign{%s, %s}" % (self.name, self.expr)

    def visit(self, visitor):
        return visitor.visitAssign(self)

class Binary(object):
    """this is the ast node for a binary expression, contains left, right and operator"""

    def __init__(self, operator, left, right):
        self.operator = operator
        self.right = right
        self.left = left

    def __repr__(self):
        return "Binary{%s, %s, %s}" % (self.operator, self.left, self.right)

    def visit(self, visitor):
        return visitor.visitBinary(self)

class Unary(object):
    """this is the ast node for a unary expression, contains expression and operator"""

    def __init__(self, operator, expr):
        self.operator = operator
        self.expr = expr

    def __repr__(self):
        return "Unary{%s, %s}" % (self.operator, self.expr)

    def visit(self, visitor):
        return visitor.visitUnary(self)

class Literal(object):
    """this is the ast node for a literal, contains its value"""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Literal{%s}" % (self.value)

    def visit(self, visitor):
        return visitor.visitLiteral(self)
