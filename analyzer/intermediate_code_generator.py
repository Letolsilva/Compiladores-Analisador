from typing import List, Tuple


class IntermediateCodeGenerator:
    def __init__(self):
        self.instructions: List[Tuple[str, str, str, str]] = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self) -> str:
        self.temp_count += 1
        return f"T{self.temp_count}"

    def new_label(self) -> str:
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, op: str, arg1: str, arg2: str, result: str):
        self.instructions.append((op, arg1, arg2, result))

    def print_instructions(self):
        for idx, inst in enumerate(self.instructions, start=1):
            print(f"{idx:02} - {inst}")

    def generate_from_ast(self, node):
        method = "gen_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_gen)
        return visitor(node)

    def generic_gen(self, node):
        if not hasattr(node, "__dict__"):
            return
        for attr in vars(node).values():
            if isinstance(attr, list):
                for item in attr:
                    if hasattr(item, "__class__"):
                        self.generate_from_ast(item)
            elif hasattr(attr, "__class__"):
                self.generate_from_ast(attr)

    def gen_ProgramNode(self, node):
        for decl in node.declarations:
            self.generate_from_ast(decl)
        self.generate_from_ast(node.stmt_list)

    def gen_DeclarationNode(self, node):
        # Não gera código para declaração
        pass

    def gen_BlockNode(self, node):
        for stmt in node.stmt_list:
            self.generate_from_ast(stmt)

    def gen_AssignmentNode(self, node):
        expr_temp = self.generate_from_ast(node.expr)
        self.emit("ATT", node.identifier.name, expr_temp, "NONE")

    def gen_LiteralNode(self, node):
        if isinstance(node.value, str):
            return f'"{node.value}"'
        return str(node.value)

    def gen_IdentifierNode(self, node):
        return node.name

    def gen_BinaryOpNode(self, node):
        left = self.generate_from_ast(node.left)
        right = self.generate_from_ast(node.right)
        temp = self.new_temp()
        self.emit(node.op, temp, left, right)
        return temp

    def gen_UnaryOpNode(self, node):
        expr = self.generate_from_ast(node.expr)
        temp = self.new_temp()
        self.emit(node.op, temp, expr, "NONE")
        return temp

    def gen_IfNode(self, node):
        cond_temp = self.generate_from_ast(node.condition)
        true_label = self.new_label()
        false_label = self.new_label()
        end_label = self.new_label()
        self.emit("IF", cond_temp, true_label, false_label)
        self.emit("LABEL", true_label, "NONE", "NONE")
        self.generate_from_ast(node.then_stmt)
        self.emit("JUMP", end_label, "NONE", "NONE")
        self.emit("LABEL", false_label, "NONE", "NONE")
        if node.else_stmt:
            self.generate_from_ast(node.else_stmt)
        self.emit("LABEL", end_label, "NONE", "NONE")

    def gen_WhileNode(self, node):
        start_label = self.new_label()
        true_label = self.new_label()
        end_label = self.new_label()
        self.emit("LABEL", start_label, "NONE", "NONE")
        cond_temp = self.generate_from_ast(node.condition)
        self.emit("IF", cond_temp, true_label, end_label)
        self.emit("LABEL", true_label, "NONE", "NONE")
        self.generate_from_ast(node.stmt)
        self.emit("JUMP", start_label, "NONE", "NONE")
        self.emit("LABEL", end_label, "NONE", "NONE")

    def gen_ForNode(self, node):
        # Supondo que node.assignment é AssignmentNode (ex: i := 0)
        self.generate_from_ast(node.assignment)
        start_label = self.new_label()
        body_label = self.new_label()
        end_label = self.new_label()
        var_name = node.assignment.identifier.name
        end_value = self.generate_from_ast(node.end_value)
        self.emit("LABEL", start_label, "NONE", "NONE")
        temp = self.new_temp()
        self.emit("LTE", temp, var_name, end_value)
        self.emit("IF", temp, body_label, end_label)
        self.emit("LABEL", body_label, "NONE", "NONE")
        self.generate_from_ast(node.stmt)
        temp2 = self.new_temp()
        self.emit("ADD", temp2, var_name, "1")
        self.emit("ATT", var_name, temp2, "NONE")
        self.emit("JUMP", start_label, "NONE", "NONE")
        self.emit("LABEL", end_label, "NONE", "NONE")

    def gen_IOStmtNode(self, node):
        for arg in node.args:
            val = self.generate_from_ast(arg)
            if node.operation in ("WRITE", "WRITELN"):
                self.emit("CALL", "WRITE", val, "NONE")
            elif node.operation in ("READ", "READLN"):
                self.emit("CALL", "READ", val, "NONE")
        if node.operation in ("WRITELN", "READLN"):
            self.emit("CALL", "WRITE", "\\n", "NONE")

    def gen_BreakNode(self, node):
        # Precisa de contexto de loop para saber o label de saída
        self.emit("JUMP", "END_LOOP", "NONE", "NONE")

    def gen_ContinueNode(self, node):
        # Precisa de contexto de loop para saber o label de início
        self.emit("JUMP", "START_LOOP", "NONE", "NONE")

    def gen_EmptyNode(self, node):
        pass
