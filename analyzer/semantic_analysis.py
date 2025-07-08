class SemanticError(Exception):
    def __init__(self, message, node):
        self.node = node
        self.line = getattr(node, "line", -1)
        self.column = getattr(node, "column", -1)
        super().__init__(f"{message} at line {self.line}, column {self.column}")


class SemanticAnalysis:
    def __init__(self):
        self.symbols = {}  
        self.declared_vars = set()  # Para evitar redeclarações

    def analyze(self, ast):
        self.visit(ast)

    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if not hasattr(node, "__dict__"):
            return
        for attr in vars(node).values():
            if isinstance(attr, list):
                for item in attr:
                    if hasattr(item, "__class__"):
                        self.visit(item)
            elif hasattr(attr, "__class__"):
                self.visit(attr)

    def visit_ProgramNode(self, node):
        for decl in node.declarations:
            self.visit(decl)
        self.visit(node.stmt_list)

    def visit_DeclarationNode(self, node):
        for ident in node.identifiers:
            if ident.name in self.declared_vars:
                raise SemanticError(
                    f"Variável '{ident.name}' já declarada", ident
                )
            self.declared_vars.add(ident.name)
            self.symbols[ident.name] = node.var_type

    def visit_AssignmentNode(self, node):
        if node.identifier.name not in self.symbols:
            raise SemanticError(
                f"Variável '{node.identifier.name}' não declarada", node.identifier
            )
        
        expr_type = self.visit(node.expr)
        var_type = self.symbols[node.identifier.name]
        
        if not self._types_compatible(var_type, expr_type):
            raise SemanticError(
                f"Não é possível atribuir uma variável do tipo {expr_type} em uma do tipo {var_type}", node
            )

    def visit_IdentifierNode(self, node):
        if node.name not in self.symbols:
            raise SemanticError(f"Variável '{node.identifier.name}' não declarada", node)
        return self.symbols[node.name]

    def visit_BinaryOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        if node.op in ["ADD", "SUB", "MUL", "DIV", "INT_DIV", "MOD"]:
            if node.op == "MOD" and (left_type not in ["INTEGER"] or right_type not in ["INTEGER"]):
                raise SemanticError(f"MOD necessita de números inteiros", node)
            if node.op == "INT_DIV" and (left_type not in ["INTEGER"] or right_type not in ["INTEGER"]):
                raise SemanticError(f"Divisão inteira necessita de números inteiros", node)
            if left_type in ["INTEGER", "REAL"] and right_type in ["INTEGER", "REAL"]:
                return "REAL" if left_type == "REAL" or right_type == "REAL" else "INTEGER"
            else:
                raise SemanticError(f"Operadores inválidos para a operação {node.op}: {left_type}, {right_type}", node)
        
        elif node.op in ["EQ", "NEQ", "LT", "LTE", "GT", "GTE", "EQUALS"]:
            if not self._types_comparable(left_type, right_type):
                raise SemanticError(f"Não é possível comparar variável do tipo {left_type} com variável do tipo {right_type}", node)
            return "BOOLEAN"
        
        elif node.op in ["AND", "OR"]:
            if left_type != "BOOLEAN" or right_type != "BOOLEAN":
                raise SemanticError(f"Operadores lógicos precisam de operandos booleanos", node)
            return "BOOLEAN"
        
        else:
            raise SemanticError(f"Operação binária desconhecida: {node.op}", node)

    def visit_UnaryOpNode(self, node):
        expr_type = self.visit(node.expr)
        
        if node.op in ["ADD", "SUB"]:
            if expr_type not in ["INTEGER", "REAL"]:
                raise SemanticError(f"Operação {node.op} precisa de operando numérico", node)
            return expr_type
        elif node.op == "NOT":
            if expr_type != "BOOLEAN":
                raise SemanticError(f"NOT precisa de operando booleano", node)
            return "BOOLEAN"
        else:
            raise SemanticError(f"Operação unária desconhecida: {node.op}", node)

    def visit_LiteralNode(self, node):
        type_v = node.value_type
        if type_v == "DECIMAL" or type_v == "HEXADECIMAL" or type_v == "OCTAL":
            return "INTEGER"
        elif type_v == "FLOAT":
            return "REAL"
        elif type_v == "STRING":
            return "STRING"
        else:
            raise SemanticError(f"Tipo desconhecido: {type_v}", node)

    def visit_ForNode(self, node):
        self.visit(node.assignment)
        
        end_type = self.visit(node.end_value)
        var_type = self.symbols[node.assignment.identifier.name]
        
        if not self._types_compatible(var_type, end_type):
            raise SemanticError(
                f"Valor final do for tem tipo: {end_type}, incompatível com o tipo da variável de loop: {var_type}", 
                node.end_value
            )
        
        self.visit(node.stmt)

    def visit_WhileNode(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != "BOOLEAN":
            raise SemanticError(f"While precisa de condição booleana, mas é: {condition_type}", node.condition)
        
        self.visit(node.stmt)

    def visit_IfNode(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != "BOOLEAN":
            raise SemanticError(f"If precisa de condição booleana, mas é: {condition_type}", node.condition)
        
        self.visit(node.then_stmt)
        if node.else_stmt:
            self.visit(node.else_stmt)

    def visit_BreakNode(self, node):
        pass

    def visit_ContinueNode(self, node):
        pass

    def visit_IOStmtNode(self, node):
        if node.operation in ["READ", "READLN"]:
            for arg in node.args:
                if hasattr(arg, 'name'): 
                    if arg.name not in self.symbols:
                        raise SemanticError(f"Variável '{arg.name}' não declarada", arg)
        elif node.operation in ["WRITE", "WRITELN"]:
            for arg in node.args:
                self.visit(arg)

    def visit_BlockNode(self, node):
        for stmt in node.stmt_list:
            self.visit(stmt)

    def visit_EmptyNode(self, node):
        pass 

    def _types_compatible(self, target_type, source_type):
        if target_type == source_type:
            return True
        if target_type == "REAL" and source_type == "INTEGER":
            return True
        return False

    def _types_comparable(self, type1, type2):
        if type1 == type2:
            return True

        if type1 in ["INTEGER", "REAL"] and type2 in ["INTEGER", "REAL"]:
            return True
        return False
