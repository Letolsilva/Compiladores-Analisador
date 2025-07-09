class IntermediateCodeExecutor:
    def __init__(self, instructions):
        self.instructions = instructions
        self.variables = {}  # {nome: {'value': valor, 'type': tipo}}
        self.labels = self._map_labels() 
        self.pc = 0  
        self.output = "" # Para armazenar a saida e fazer testes depois

    def _map_labels(self):
        labels = {}
        for idx, inst in enumerate(self.instructions):
            op, arg1, arg2, res = inst
            if op == "LABEL":
                labels[arg1] = idx
        return labels

    def _get_type(self, value):

        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'real'
        elif isinstance(value, str):
            return 'string'
        else:
            return 'unknown'

    def _set_variable(self, var_name, value):

        new_type = self._get_type(value)
        
        if var_name in self.variables:
            current_type = self.variables[var_name]['type']
            
            if current_type == 'string':
                value = str(value)
                new_type = 'string'
            
            elif current_type == 'real' and new_type == 'integer':
                value = float(value)
                new_type = 'real'
            
            elif current_type in ['integer', 'real', 'boolean'] and new_type == 'string':
                raise Exception(f"Erro de tipo: Não é possível atribuir string a variável '{var_name}' do tipo {current_type}")

            elif current_type != new_type:
                raise Exception(f"Erro de tipo: Variável '{var_name}' é do tipo {current_type}, mas tentou atribuir {new_type}")
        
        self.variables[var_name] = {'value': value, 'type': new_type}


    def run(self):
        while self.pc < len(self.instructions):
            op, arg1, arg2, res = self.instructions[self.pc]

            #print(f"\n[{self.pc+1}] Executando: {op}, {arg1}, {arg2}, {res}")

            if op == "ATT":
                value = self._get_value(arg2)
                self._set_variable(arg1, value)

            elif op in {"ADD", "SUB", "MUL", "DIV", "LT", "GT", "LTE", "GTE", "AND", "OR", "EQUALS", "MOD", "INT_DIV"}:
                val1 = self._get_value(arg2)
                val2 = self._get_value(res)
                result = self._execute_binary(op, val1, val2)
                self._set_variable(arg1, result)

            elif op == "NOT":
                val = self._get_value(arg2)
                result = int(not val)
                self._set_variable(arg1, result)

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
                    self.output += str(val)
                elif arg1 == "READ":
                    user_input = input()
                    try:
                        if self._is_hexadecimal(user_input):
                            value = self._convert_hexadecimal(user_input)
                        elif self._is_octal(user_input):
                            value = self._convert_octal(user_input)
                        elif '.' in user_input:
                            value = float(user_input)
                        else:
                            value = int(user_input)
                    except ValueError:
                        value = user_input
                    
                    self._set_variable(arg2, value)

            elif op == "LABEL":
                pass  

            else:
                raise Exception(f"Instrução não reconhecida: {op}")

            self.pc += 1
        return self.output

    
    def _get_value(self, arg):
        if self._is_hexadecimal(arg):
            return self._convert_hexadecimal(arg)
        
        elif self._is_octal(arg):
            return self._convert_octal(arg)
        
        elif arg.isdigit() or (arg.startswith('-') and arg[1:].isdigit()):
            return int(arg)
        
        elif self._is_float(arg):
            return float(arg)
        
        elif (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
            literal = arg[1:-1]
            try:
                if self._is_hexadecimal(literal):
                    return self._convert_hexadecimal(literal)
                elif self._is_octal(literal):
                    return self._convert_octal(literal)
                elif '.' in literal:
                    return float(literal)
                return int(literal)
            except ValueError:
                return literal 
        
        elif arg in self.variables:
            return self.variables[arg]['value']
        
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

    def _is_hexadecimal(self, arg):
        if isinstance(arg, str):
            if arg.startswith('-'):
                return arg[1:].startswith(('0x', '0X')) and len(arg) > 3
            return arg.startswith(('0x', '0X')) and len(arg) > 2
        return False

    def _is_octal(self, arg):
        if isinstance(arg, str):
            if arg.startswith('-'):
                test_arg = arg[1:]
            else:
                test_arg = arg
            
            if test_arg.startswith('0') and len(test_arg) > 1:
                return all(c in '01234567' for c in test_arg[1:]) and not any(c in '89' for c in test_arg)
        return False

    def _is_float(self, arg):
        if isinstance(arg, str):
            try:
                float(arg)
                return '.' in arg
            except ValueError:
                return False
        return False

    def _convert_hexadecimal(self, arg):
        try:
            return int(arg, 16)
        except ValueError:
            raise Exception(f"Erro ao converter hexadecimal: {arg}")

    def _convert_octal(self, arg):
        try:
            return int(arg, 8)
        except ValueError:
            raise Exception(f"Erro ao converter octal: {arg}")

