from analyzer.lexeme import Lexeme
from analyzer.ast_nodes import (
    ProgramNode,
    DeclarationNode,
    AssignmentNode,
    BlockNode,
    ForNode,
    IOStmtNode,
    WhileNode,
    IfNode,
    BreakNode,
    ContinueNode,
    EmptyNode,
    BinaryOpNode,
    UnaryOpNode,
    LiteralNode,
    IdentifierNode,
)


class SyntaxError(Exception):
    def __init__(self, message, token):
        self.token = token
        self.line = token.line
        self.column = token.column
        super().__init__(f"{message} at line {self.line}, column {self.column}")


class SyntacticAnalysis:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        ast = self.program()
        # Após o programa, não pode haver mais tokens "úteis"
        if self.current < len(self.tokens):
            token = self.tokens[self.current]
            raise SyntaxError(
                f"Unexpected token after end of program: {token.token_type} ('{token.value}')",
                token,
            )
        return ast

    def expect(self, expected_type):
        if not self.match(expected_type):
            current_token = (
                self.tokens[self.current] if self.current < len(self.tokens) else None
            )
            if current_token:
                raise SyntaxError(
                    f"Expected {expected_type}, but got {current_token.token_type} ('{current_token.value}')",
                    current_token,
                )
            else:
                # Pega o último token válido, se houver
                last_token = (
                    self.tokens[self.current - 1]
                    if self.current > 0
                    else Lexeme(expected_type, "", -1, -1)
                )
                raise SyntaxError(
                    f"Unexpected end of input, expected {expected_type}",
                    last_token,
                )

    def match(self, expected_type):
        if (
            self.current < len(self.tokens)
            and self.tokens[self.current].token_type == expected_type
        ):
            self.current += 1
            return True
        return False

    def program(self):
        self.expect("PROGRAM")
        identifier = self.tokens[self.current - 1].value
        self.expect("IDENTIFIER")
        self.expect("SEMICOLON")
        declarations = self.declarations()
        self.expect("BEGIN")
        stmt_list = self.stmtList()
        self.expect("END")
        self.expect("DOT")
        return ProgramNode(identifier, declarations, stmt_list)

    def declarations(self):
        self.expect("VAR")
        declarations = []
        while (
            self.current < len(self.tokens)
            and self.tokens[self.current].token_type == "IDENTIFIER"
        ):
            declarations.append(self.declaration())
        return declarations

    def declaration(self):
        identifiers = self.listaIdent()
        self.expect("COLON")
        var_type = self.type()
        self.expect("SEMICOLON")
        return DeclarationNode(identifiers, var_type)

    def listaIdent(self):
        identifiers = []
        while True:
            token = self.tokens[self.current]
            identifiers.append(IdentifierNode(token.value, token.line, token.column))
            self.expect("IDENTIFIER")
            if not self.match("COMMA"):
                break
        return identifiers

    def type(self):
        if self.match("INTEGER"):
            return "INTEGER"
        elif self.match("REAL"):
            return "REAL"
        elif self.match("STRING"):
            return "STRING"
        raise SyntaxError("Expected type", self.tokens[self.current])

    def stmtList(self):
        statements = []
        while self.current < len(self.tokens):
            if self.tokens[self.current].token_type in {"END", "ELSE", "DOT"}:
                break
            statements.append(self.stmt())
        return BlockNode(statements)

    def stmt(self):
        token = self.tokens[self.current].token_type
        if token == "FOR":
            return self.forStmt()
        elif token in {"READ", "WRITE", "READLN", "WRITELN"}:
            return self.ioStmt()
        elif token == "WHILE":
            return self.whileStmt()
        elif token == "IF":
            return self.ifStmt()
        elif token == "BREAK":
            self.expect("BREAK")
            self.expect("SEMICOLON")
            return BreakNode()
        elif token == "CONTINUE":
            self.expect("CONTINUE")
            self.expect("SEMICOLON")
            return ContinueNode()
        elif token == "SEMICOLON":
            self.expect("SEMICOLON")
            return EmptyNode()
        elif token == "BEGIN":
            return self.bloco()
        elif token == "IDENTIFIER":
            assignment = self.atrib()
            self.expect("SEMICOLON")
            return assignment
        else:
            raise SyntaxError(
                "Unexpected token in statement", self.tokens[self.current]
            )

    def bloco(self):
        self.expect("BEGIN")
        stmt_list = self.stmtList()
        self.expect("END")
        self.expect("SEMICOLON")
        return BlockNode(stmt_list.stmt_list)

    def forStmt(self):
        self.expect("FOR")
        assignment = self.atrib()
        self.expect("TO")
        if self.match("IDENTIFIER"):
            token = self.tokens[self.current - 1]
            end_value = IdentifierNode(token.value, token.line, token.column)
        elif self.match("DECIMAL"):
            end_value = LiteralNode(self.tokens[self.current - 1].value, "DECIMAL")
        else:
            raise SyntaxError("Expected end value in for", self.tokens[self.current])
        self.expect("DO")
        stmt = self.stmt()
        return ForNode(assignment, end_value, stmt)

    def ioStmt(self):
        token = self.tokens[self.current].token_type
        self.current += 1
        self.expect("LPAREN")
        if token in {"READ", "READLN"}:
            identifier = self.tokens[self.current].value
            self.expect("IDENTIFIER")
            self.expect("RPAREN")
            self.expect("SEMICOLON")
            return IOStmtNode(
                token,
                [
                    IdentifierNode(
                        identifier,
                        self.tokens[self.current - 1].line,
                        self.tokens[self.current - 1].column,
                    )
                ],
            )
        else:
            out_list = self.outList()
            self.expect("RPAREN")
            self.expect("SEMICOLON")
            return IOStmtNode(token, out_list)

    def outList(self):
        outputs = [self.out()]
        while self.match("COMMA"):
            outputs.append(self.out())
        return outputs

    def out(self):
        if self.match("STRING"):
            return LiteralNode(self.tokens[self.current - 1].value, "STRING")
        elif self.match("IDENTIFIER"):
            token = self.tokens[self.current - 1]
            return IdentifierNode(token.value, token.line, token.column)
        elif self.match("DECIMAL"):
            return LiteralNode(self.tokens[self.current - 1].value, "DECIMAL")
        elif self.match("FLOAT"):
            return LiteralNode(self.tokens[self.current - 1].value, "FLOAT")
        raise SyntaxError("Expected output type", self.tokens[self.current])

    def whileStmt(self):
        self.expect("WHILE")
        condition = self.expr()
        self.expect("DO")
        stmt = self.stmt()
        return WhileNode(condition, stmt)

    def ifStmt(self):
        self.expect("IF")
        condition = self.expr()
        self.expect("THEN")
        then_stmt = self.stmt()
        else_stmt = None
        if self.match("ELSE"):
            else_stmt = self.stmt()
        return IfNode(condition, then_stmt, else_stmt)

    def atrib(self):
        token = self.tokens[self.current]
        identifier = IdentifierNode(token.value, token.line, token.column)
        self.expect("IDENTIFIER")
        self.expect("ASSIGN")
        expr = self.expr()
        return AssignmentNode(identifier, expr)

    def expr(self):
        return self.orExpr()

    def orExpr(self):
        left = self.andExpr()
        while self.match("OR"):
            right = self.andExpr()
            left = BinaryOpNode("OR", left, right)
        return left

    def andExpr(self):
        left = self.notExpr()
        while self.match("AND"):
            right = self.notExpr()
            left = BinaryOpNode("AND", left, right)
        return left

    def notExpr(self):
        if self.match("NOT"):
            return UnaryOpNode("NOT", self.notExpr())
        else:
            return self.rel()

    def rel(self):
        left = self.add()
        while (
            self.match("EQ")
            or self.match("NEQ")
            or self.match("LT")
            or self.match("LTE")
            or self.match("GT")
            or self.match("GTE")
            or self.match("EQUALS")
        ):
            operator = self.tokens[self.current - 1].token_type
            right = self.add()
            left = BinaryOpNode(operator, left, right)
        return left

    def add(self):
        left = self.mult()
        while self.match("ADD") or self.match("SUB"):
            operator = self.tokens[self.current - 1].token_type
            right = self.mult()
            left = BinaryOpNode(operator, left, right)
        return left

    def mult(self):
        left = self.uno()
        while (
            self.match("MUL")
            or self.match("DIV")
            or self.match("MOD")
            or self.match("INT_DIV")
        ):
            operator = self.tokens[self.current - 1].token_type
            right = self.uno()
            left = BinaryOpNode(operator, left, right)
        return left

    def uno(self):
        if self.match("ADD"):
            return UnaryOpNode("ADD", self.uno())
        elif self.match("SUB"):
            return UnaryOpNode("SUB", self.uno())
        else:
            return self.fator()

    def fator(self):
        if self.match("DECIMAL"):
            return LiteralNode(self.tokens[self.current - 1].value, "DECIMAL")
        elif self.match("FLOAT"):
            return LiteralNode(self.tokens[self.current - 1].value, "FLOAT")
        elif self.match("IDENTIFIER"):
            token = self.tokens[self.current - 1]
            return IdentifierNode(token.value, token.line, token.column)
        elif self.match("LPAREN"):
            expr = self.expr()
            self.expect("RPAREN")
            return expr
        elif self.match("STRING"):
            return LiteralNode(self.tokens[self.current - 1].value, "STRING")
        raise SyntaxError("Expected factor", self.tokens[self.current])
