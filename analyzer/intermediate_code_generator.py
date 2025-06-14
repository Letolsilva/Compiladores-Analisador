from typing import List, Tuple
from analyzer.lexeme import Lexeme

class IntermediateCodeGenerator:
    def __init__(self):
        self.instructions: List[Tuple[str, str, str, str]] = []
        self.temp_count = 0
        self.label_count = 0
        self.dict: dict = {}

    def new_temp(self) -> str:
        temp = f"T{self.temp_count+1}"
        self.temp_count += 1
        return temp

    def new_label(self) -> str:
        label = f"L{self.label_count+1}"
        self.label_count += 1
        return label

    def emit(self, op: str, arg1: str, arg2: str, result: str):
        self.instructions.append((op, arg1, arg2, result))
        self.dict[op] = self.dict.get(op, 0) + 1

    def generate_from_tokens(self, tokens: List[Lexeme]):
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok.token_type == 'IDENTIFIER' and i + 1 < len(tokens) and tokens[i+1].token_type == 'ASSIGN':
                i = self._handle_assignment(tokens, i)
            elif tok.token_type == 'IF':
                i = self._handle_if(tokens, i)
            elif tok.token_type == 'WHILE':
                i = self._handle_while(tokens, i)
            elif tok.token_type == 'FOR':
                i = self._handle_for(tokens, i)
            else:
                i += 1
    
    def _handle_boolean_expression(self, tokens: List[Lexeme], i: int) -> Tuple[str, int]:
        return self._parse_or(tokens, i)

    # OR é o nível mais baixo (menor precedência)
    def _parse_or(self, tokens: List[Lexeme], i: int) -> Tuple[str, int]:
        left_temp, i = self._parse_and(tokens, i)
        while i < len(tokens) and tokens[i].token_type == 'OR':
            i += 1
            right_temp, i = self._parse_and(tokens, i)
            res = self.new_temp()
            self.emit('OR', res, left_temp, right_temp)
            left_temp = res
        return left_temp, i

    # AND acima de OR
    def _parse_and(self, tokens: List[Lexeme], i: int) -> Tuple[str, int]:
        left_temp, i = self._parse_not(tokens, i)
        while i < len(tokens) and tokens[i].token_type == 'AND':
            i += 1
            right_temp, i = self._parse_not(tokens, i)
            res = self.new_temp()
            self.emit('AND', res, left_temp, right_temp)
            left_temp = res
        return left_temp, i

    # NOT tem precedência máxima
        # NOT tem precedência máxima
    def _parse_not(self, tokens: List[Lexeme], i: int) -> Tuple[str, int]:
        not_count = 0
        # Conta quantos NOTs seguidos existem
        while i < len(tokens) and tokens[i].token_type == 'NOT':
            not_count += 1
            i += 1
        operand_temp, i = self._parse_primary(tokens, i)
        # Aplica os NOTs na ordem correta
        for _ in range(not_count):
            res = self.new_temp()
            self.emit('NOT', res, operand_temp, 'NONE')
            operand_temp = res
        return operand_temp, i

    # Primários: parênteses ou comparação relacional
    def _parse_primary(self, tokens: List[Lexeme], i: int) -> Tuple[str, int]:
        # subexpressão em parênteses
        if tokens[i].token_type == 'LPAREN':
            i += 1
            temp, i = self._handle_boolean_expression(tokens, i)
            if tokens[i].token_type != 'RPAREN':
                raise Exception(f"Expected RPAREN, got {tokens[i].token_type}")
            return temp, i + 1

        # relacional simples: x < y, 2 >= 3, etc.
        left  = tokens[i].value
        op    = tokens[i+1].token_type
        right = tokens[i+2].value
        res = self.new_temp()
        self.emit(op, res, left, right)
        return res, i + 3


    def _handle_assignment(self, tokens: List[Lexeme], i: int) -> int:
        # Parse: <id> := <expr>;
        var_name = tokens[i].value
        i += 2 

        expr_tokens = []
        while i < len(tokens) and tokens[i].token_type != 'SEMICOLON':
            expr_tokens.append(tokens[i])
            i += 1

        if any(token.token_type in {'NOT','AND','OR','LT', 'LTE', 'GT', 'GTE', 'EQ', 'NEQ'} for token in expr_tokens):
            temp, _ = self._handle_boolean_expression(expr_tokens, 0)
            self.emit('ATT', var_name, temp, 'NONE')
        elif any(token.token_type in {'ADD', 'SUB', 'MUL', 'DIV'} for token in expr_tokens):
            current = expr_tokens[0].value
            j = 1
            while j < len(expr_tokens):
                op_tok = expr_tokens[j]
                right = expr_tokens[j+1].value if (j+1) < len(expr_tokens) else ''
                temp = self.new_temp()
                self.emit(op_tok.token_type, temp, current, right)
                current = temp
                j += 2
                self.emit('ATT', var_name, current, 'NONE')
        else:
            self.emit('ATT', var_name, expr_tokens[0].value, 'NONE')

        
        return i + 1

    def _handle_if(self, tokens: List[Lexeme], i: int, end_label: str = None) -> int:
        """
        IF <cond> THEN ... [ELSE ...]
        usando _handle_boolean_expression para toda a condição.
        """
        # pula o 'IF'
        i += 1

        # trata condição inteira e recebe o temp final
        cond_temp, i = self._handle_boolean_expression(tokens, i)

        # agora deve estar em 'THEN'
        if tokens[i].token_type == 'THEN':
            i += 1

        # gera labels
        true_label  = self.new_label()
        false_label = self.new_label()
        if not end_label:
            end_label = self.new_label()

        # salto condicional
        self.emit('IF', cond_temp, true_label, false_label)

        # bloco THEN
        self.emit('LABEL', true_label, 'NONE', 'NONE')
        if tokens[i].token_type == 'BEGIN':
            # consome bloco BEGIN...END;
            i += 1
            while tokens[i].token_type != 'END':
                if tokens[i].token_type == 'IF':
                    i = self._handle_if(tokens, i)
                else:
                    i = self._handle_command(tokens, i)
            i += 1  # pula 'END'
        else:
            # comando único
            if tokens[i].token_type == 'IF':
                i = self._handle_if(tokens, i)
            else:
                i = self._handle_command(tokens, i)

        # pula para fim do IF
        self.emit('JUMP', end_label, 'NONE', 'NONE')
        self.emit('LABEL', false_label, 'NONE', 'NONE')

        # ELSE (se existir)
        if i < len(tokens) and tokens[i].token_type == 'ELSE':
            i += 1
            if tokens[i].token_type == 'BEGIN':
                i += 1
                while tokens[i].token_type != 'END':
                    if tokens[i].token_type == 'IF':
                        i = self._handle_if(tokens, i)
                    else:
                        i = self._handle_command(tokens, i)
                i += 1  # pula 'END'
            else:
                if tokens[i].token_type == 'IF':
                    i = self._handle_if(tokens, i)
                else:
                    i = self._handle_command(tokens, i)

        # marca fim do IF
        self.emit('LABEL', end_label, 'NONE', 'NONE')
        return i
        
    def handle_loop_execution(self, tokens: List[Lexeme], i: int, start_label: str, end_label: str, _isIncreasing = False, var_name = None) -> int:
        if tokens[i].token_type in {'BREAK', 'CONTINUE'}:
            i = self.handle_loop_interruption(tokens, i, start_label, end_label, _isIncreasing, var_name)
        elif tokens[i].token_type == 'WHILE':
            i = self._handle_while(tokens, i)
        elif tokens[i].token_type == 'FOR':
            i = self._handle_for(tokens, i)
        else:
            i = self._handle_command(tokens, i)
        return i

    def _handle_while(self, tokens: List[Lexeme], i: int) -> int:
        start_label = self.new_label()
        true_label = self.new_label()
        end_label = self.new_label()

        self.emit('LABEL', start_label, 'NONE', 'NONE')

        # Exemplo: WHILE <left> <op> <right> DO ...
        left = tokens[i + 1].value
        op = tokens[i + 2].token_type
        right = tokens[i + 3].value

        temp = self.new_temp()
        self.emit(op, left, right, temp)

        self.emit('IF', temp, true_label, end_label)

        self.emit('LABEL', true_label, 'NONE', 'NONE')
        i += 4  # pula WHILE + condicional
        if tokens[i].token_type == 'DO':
            i += 1

        if tokens[i].token_type == 'BEGIN':
            i += 1
            while tokens[i].token_type != 'END':
                i = self.handle_loop_execution(tokens, i, start_label, end_label)
            i += 1  # pula END
            if i < len(tokens) and tokens[i].token_type == 'SEMICOLON':
                i += 1
        else:
            i = self.handle_loop_execution(tokens, i, start_label, end_label)


        self.emit('JUMP', start_label, 'NONE', 'NONE')
        self.emit('LABEL', end_label, 'NONE', 'NONE')

        return i

    def _handle_for(self, tokens: List[Lexeme], i: int) -> int:
        var_name = tokens[i + 1].value  # variável de controle
        assign_token = tokens[i + 2]
        start_value = tokens[i + 3].value  # valor inicial

        # Inicialização da variável de controle
        self.emit('ATT', var_name, start_value, 'NONE')

        direction = tokens[i + 4].token_type  # TO ou DOWNTO
        end_value = tokens[i + 5].value

        start_label = self.new_label()
        body_label = self.new_label()
        end_label = self.new_label()

        self.emit('LABEL', start_label, 'NONE', 'NONE')

        isIncreasing = direction == 'TO'
        # Verifica a condição do loop
        temp = self.new_temp()
        if isIncreasing:
            self.emit('LEQ', temp, var_name, end_value)
        else:
            self.emit('GEQ', temp, var_name, end_value)

        self.emit('IF', temp, body_label, end_label)

        # Corpo do laço
        self.emit('LABEL', body_label, 'NONE', 'NONE')
        i += 6
        if tokens[i].token_type == 'DO':
            i += 1

        if tokens[i].token_type == 'BEGIN':
            i += 1
            while tokens[i].token_type != 'END':
                i = self.handle_loop_execution(tokens, i, start_label, end_label, var_name, isIncreasing)
            i += 1  # END
            if i < len(tokens) and tokens[i].token_type == 'SEMICOLON':
                i += 1
        else:
            i = self.handle_loop_execution(tokens, i, start_label, end_label, var_name, isIncreasing)

        # Incremento ou decremento
        temp2 = self.new_temp()
        if isIncreasing:
            self.emit('ADD', temp2, temp2, 1)
        else:
            self.emit('SUB', temp2, var_name, 1)
        self.emit('ATT', var_name, temp2, 'NONE')

        self.emit('JUMP', start_label, 'NONE', 'NONE')
        self.emit('LABEL', end_label, 'NONE', 'NONE')

        return i

    def _handle_command(self, tokens: List[Lexeme], i: int) -> int:
        tok = tokens[i]

        if tok.token_type in ('READLN', 'READ'):
            arg = tokens[i+2].value if tokens[i+1].token_type == 'LPAREN' else tokens[i+1].value
            self.emit('CALL', 'READ', arg, 'NONE')
            self.emit('CALL', 'WRITE', '\n', 'NONE')
            i += 3
        elif tok.token_type in ('WRITELN', 'WRITE'):
            arg = tokens[i+2].value if tokens[i+1].token_type == 'LPAREN' else tokens[i+1].value
            self.emit('CALL', 'WRITE', arg, 'NONE')
            if tok.token_type == 'WRITELN':
                self.emit('CALL', 'WRITE', '\n', 'NONE')
            i += 3
        elif tok.token_type == 'IDENTIFIER' and tokens[i+1].token_type == 'ASSIGN':
            i=self._handle_assignment(tokens,i)

        return i

    def _handle_statement(self, tokens: List[Lexeme], i: int) -> int:
        tok = tokens[i]
        # Variable assignment
        if tok.token_type == 'IDENTIFIER':
            return self._handle_assignment(tokens, i)

        # I/O calls
        if tok.token_type in ('READLN', 'READ'):
            arg = tokens[i+1].value
            self.emit('CALL', 'READ', arg, 'NONE')
        elif tok.token_type in ('WRITELN', 'WRITE'):
            arg_index = i+1
            if tokens[arg_index].token_type == 'LPAREN':
                arg_index += 1
            arg = tokens[arg_index].value
            self.emit('CALL', 'WRITE', arg, 'NONE')
            if tok.token_type == 'WRITELN':
                self.emit('CALL', 'WRITE', '\n', 'NONE')

        # Skip tokens until semicolon
        while i < len(tokens) and tokens[i].token_type != 'SEMICOLON':
            i += 1
        return i + 1 

    def handle_loop_interruption(self, tokens: List[Lexeme], i: int, start_label: str, end_label: str, _isIncreasing: bool, var_name:str) -> int:
        tok = tokens[i]

        if tok.token_type == 'BREAK':
            self.emit('JUMP', end_label, 'NONE', 'NONE')
            return i + 1

        elif tok.token_type == 'CONTINUE':
            if var_name != None: #eh for loop
                temp2 = self.new_temp()
                if _isIncreasing:
                    self.emit('ADD', temp2, temp2, 1)
                else:
                    self.emit('SUB', temp2, var_name, 1)
                self.emit('ATT', var_name, temp2, 'NONE')
            self.emit('JUMP', start_label, 'NONE', 'NONE')
            return i + 1

        return i

    def save_to_file(self, filepath: str):
        """Write the intermediate code instructions to a file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            for idx, inst in enumerate(self.instructions, start=1):
                op, a1, a2, res = inst
                f.write(f"{idx:02} - ({op}, {a1}, {a2}, {res})\n")

    def print_instructions(self):
        for idx, inst in enumerate(self.instructions, start=1):
            print(f"{idx:02} - {inst}")
