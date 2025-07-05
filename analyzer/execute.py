class IntermediateCodeExecutor:
    def __init__(self, instructions):
        self.instructions = instructions
        self.variables = {}  # Dicionário de variáveis (x, y, T1, T2, etc)
        self.labels = self._map_labels()  # Mapa: label -> índice da instrução
        self.pc = 0  # Program Counter (posição atual de execução)

    def _map_labels(self):
        labels = {}
        for idx, inst in enumerate(self.instructions):
            op, arg1, arg2, res = inst
            if op == "LABEL":
                labels[arg1] = idx
        return labels

    def run(self):
        while self.pc < len(self.instructions):
            op, arg1, arg2, res = self.instructions[self.pc]

            #print(f"\n[{self.pc+1}] Executando: {op}, {arg1}, {arg2}, {res}")

            if op == "ATT":
                self.variables[arg1] = self._get_value(arg2)

            elif op in {"ADD", "SUB", "MUL", "DIV", "LT", "GT", "LTE", "GTE", "AND", "OR", "EQUALS", "MOD", "INT_DIV"}:
                val1 = self._get_value(arg2)
                val2 = self._get_value(res)
                result = self._execute_binary(op, val1, val2)
                self.variables[arg1] = result

            elif op == "NOT":
                val = self._get_value(arg2)
                self.variables[arg1] = int(not val)

            elif op == "IF":
                condition = self._get_value(arg1)
                if condition:
                    self.pc = self.labels.get(arg2, -1)
                else:
                    self.pc = self.labels.get(res, -1)
                if self.pc == -1:
                    raise Exception(f"Label não encontrado para IF: {arg2} ou {res}")
                continue

            elif op == "JUMP":
                self.pc = self.labels.get(arg1, -1)
                if self.pc == -1:
                    raise Exception(f"Label não encontrado para JUMP: {arg1}")
                continue

            elif op == "CALL":
                if arg1 == "WRITE":
                    val = self._get_value(arg2)
                    if isinstance(val, str):
                        val = val.replace("\\n", "\n")
                    print(val, end='')
                elif arg1 == "READ":
                    user_input = input()
                    try:
                        if '.' in user_input:
                            self.variables[arg2] = float(user_input)
                        else:
                            self.variables[arg2] = int(user_input)
                    except ValueError:
                        self.variables[arg2] = user_input

            elif op == "LABEL":
                pass  

            else:
                raise Exception(f"Instrução não reconhecida: {op}")

            self.pc += 1

    
    def _get_value(self, arg):
        if arg.isdigit() or (arg.startswith('-') and arg[1:].isdigit()):
            return int(arg)
        elif (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
            literal = arg[1:-1]
            try:
                if '.' in literal:
                    return float(literal)
                return int(literal)
            except ValueError:
                return literal 
        elif arg in self.variables:
            return self.variables[arg]
        else:
            return arg


    def _execute_binary(self, op, val1, val2):
        if op == "ADD":
            return val1 + val2
        elif op == "SUB":
            return val1 - val2
        elif op == "MUL":
            return val1 * val2
        elif op == "DIV":
            return val1 / val2 if val2 != 0 else 0.0
        elif op == "INT_DIV":
            return val1 // val2 if val2 != 0 else 0
        elif op == "MOD":
            return val1 % val2 if val2 != 0 else 0
        elif op == "LT":
            return int(val1 < val2)
        elif op == "GT":
            return int(val1 > val2)
        elif op == "LTE":
            return int(val1 <= val2)
        elif op == "GTE":
            return int(val1 >= val2)
        elif op == "AND":
            return int(bool(val1) and bool(val2))
        elif op == "OR":
            return int(bool(val1) or bool(val2))
        elif op == "EQUALS":
            return int(val1 == val2)

