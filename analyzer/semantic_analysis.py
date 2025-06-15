class SemanticError(Exception):
    def __init__(self, message, node):
        self.node = node
        self.line = getattr(node, "line", -1)
        self.column = getattr(node, "column", -1)
        super().__init__(f"{message} at line {self.line}, column {self.column}")


class SemanticAnalysis:
    def __init__(self):
        self.symbols = set()

    def analyze(self, ast):
        self.visit(ast)

    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Só visita se o nó tem atributos
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
        # Coleta declarações
        for decl in node.declarations:
            self.visit(decl)
        self.visit(node.stmt_list)

    def visit_DeclarationNode(self, node):
        for ident in node.identifiers:
            self.symbols.add(ident.name)

    def visit_AssignmentNode(self, node):
        # Verifica se variável foi declarada
        if node.identifier.name not in self.symbols:
            raise SemanticError(
                f"Variable '{node.identifier.name}' not declared", node.identifier
            )
        self.visit(node.expr)

    def visit_IdentifierNode(self, node):
        if node.name not in self.symbols:
            raise SemanticError(f"Variable '{node.name}' not declared", node)
