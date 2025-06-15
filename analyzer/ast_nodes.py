class ASTNode:
    pass


class ProgramNode(ASTNode):
    def __init__(self, identifier, declarations, stmt_list):
        self.identifier = identifier
        self.declarations = declarations
        self.stmt_list = stmt_list


class DeclarationNode(ASTNode):
    def __init__(self, identifiers, var_type):
        self.identifiers = identifiers
        self.var_type = var_type


class AssignmentNode(ASTNode):
    def __init__(self, identifier, expr):
        self.identifier = identifier
        self.expr = expr


class BlockNode(ASTNode):
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list


class ForNode(ASTNode):
    def __init__(self, assignment, end_value, stmt):
        self.assignment = assignment
        self.end_value = end_value
        self.stmt = stmt


class IOStmtNode(ASTNode):
    def __init__(self, operation, args):
        self.operation = operation
        self.args = args


class WhileNode(ASTNode):
    def __init__(self, condition, stmt):
        self.condition = condition
        self.stmt = stmt


class IfNode(ASTNode):
    def __init__(self, condition, then_stmt, else_stmt=None):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt


class BreakNode(ASTNode):
    pass


class ContinueNode(ASTNode):
    pass


class EmptyNode(ASTNode):
    pass


class BinaryOpNode(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryOpNode(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class LiteralNode(ASTNode):
    def __init__(self, value, value_type):
        self.value = value
        self.value_type = value_type


class IdentifierNode(ASTNode):
    def __init__(self, name, line=None, column=None):
        self.name = name
        self.line = line
        self.column = column
