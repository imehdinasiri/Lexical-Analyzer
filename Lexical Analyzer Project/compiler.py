# TOKEN DEFINITIONS

KEYWORDS = {"int", "float", "double", "if", "else"}
OPERATORS = {'+', '-', '*', '/', '%', '=', '<', '>', '!'}
DOUBLE_OPERATORS = {"==", "!=", "<=", ">="}
SIGNS = {';', '(', ')', '{', '}'}


# LEXER

def next_state(current, ch):
    if current == 0:
        if ch.isspace():
            return 0
        elif ch.isalpha() or ch == '_':
            return 1
        elif ch.isdigit():
            return 3
        elif ch in OPERATORS:
            return 6
        elif ch in SIGNS:
            return 7
        else:
            return 8

    if current == 1:
        return 1 if ch.isalnum() or ch == '_' else -1

    if current == 3:
        return 3 if ch.isdigit() else -1

    return -1


def lexical_analyzer_from_text(code):
    tokens = []
    i = 0
    line = 1
    col = 1

    while i < len(code):
        ch = code[i]

        if ch == '\n':
            line += 1
            col = 1
            i += 1
            continue

        state = next_state(0, ch)

        if state == 0:
            i += 1
            col += 1
            continue

        start_line = line
        start_col = col
        buffer = ch
        i += 1
        col += 1

        while i < len(code):
            next_ch = code[i]
            new_state = next_state(state, next_ch)

            if new_state == -1:
                break

            buffer += next_ch
            i += 1
            col += 1
            state = new_state

        if state == 1:
            token_type = "KEYWORD" if buffer in KEYWORDS else "IDENTIFIER"
            tokens.append((token_type, buffer, start_line, start_col))

        elif state == 3:
            tokens.append(("INTEGER", buffer, start_line, start_col))

        elif state == 6:
            if i < len(code):
                possible = buffer + code[i]
                if possible in DOUBLE_OPERATORS:
                    tokens.append(
                        ("OPERATOR", possible, start_line, start_col))
                    i += 1
                    col += 1
                    continue
            tokens.append(("OPERATOR", buffer, start_line, start_col))

        elif state == 7:
            tokens.append(("SIGN", buffer, start_line, start_col))

        else:
            tokens.append(("UNKNOWN", buffer, start_line, start_col))

    tokens.append(("EOF", "", line, col))
    return tokens


# PARSER

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        self.current += 1

    def match(self, expected_type, expected_value=None):
        tok = self.peek()
        if tok[0] != expected_type:
            raise SyntaxError(f"Unexpected token {tok}")
        if expected_value and tok[1] != expected_value:
            raise SyntaxError(f"Unexpected token {tok}")
        self.advance()
        return tok

    def parse_program(self):
        statements = []
        while self.peek()[0] != "EOF":
            statements.append(self.parse_statement())
        return ("PROGRAM", statements)

    def parse_statement(self):
        tok = self.peek()

        if tok[0] == "KEYWORD" and tok[1] in {"int", "float", "double"}:
            return self.parse_declaration()

        if tok[0] == "KEYWORD" and tok[1] == "if":
            return self.parse_if()

        if tok[0] == "IDENTIFIER":
            return self.parse_assignment()

        raise SyntaxError(f"Invalid statement {tok}")

    def parse_declaration(self):
        type_tok = self.match("KEYWORD")
        id_tok = self.match("IDENTIFIER")

        if self.peek()[0] == "OPERATOR" and self.peek()[1] == "=":
            self.match("OPERATOR", "=")
            expr = self.parse_expression()
            self.match("SIGN", ";")
            return ("DECLARATION", type_tok[1], id_tok[1], expr)

        self.match("SIGN", ";")
        return ("DECLARATION", type_tok[1], id_tok[1], None)

    def parse_assignment(self):
        id_tok = self.match("IDENTIFIER")
        self.match("OPERATOR", "=")
        expr = self.parse_expression()
        self.match("SIGN", ";")
        return ("ASSIGNMENT", id_tok[1], expr)

    def parse_if(self):
        self.match("KEYWORD", "if")
        self.match("SIGN", "(")
        condition = self.parse_expression()
        self.match("SIGN", ")")
        stmt = self.parse_statement()
        return ("IF", condition, stmt)

    def parse_expression(self):
        left = self.parse_term()

        while self.peek()[0] == "OPERATOR" and self.peek()[1] in {"+", "-", "<", ">", "=="}:
            op = self.match("OPERATOR")[1]
            right = self.parse_term()
            left = ("BIN_OP", op, left, right)

        return left

    def parse_term(self):
        left = self.parse_factor()

        while self.peek()[0] == "OPERATOR" and self.peek()[1] in {"*", "/"}:
            op = self.match("OPERATOR")[1]
            right = self.parse_factor()
            left = ("BIN_OP", op, left, right)

        return left

    def parse_factor(self):
        tok = self.peek()

        if tok[0] == "INTEGER":
            self.advance()
            return ("NUMBER", tok[1])

        if tok[0] == "IDENTIFIER":
            self.advance()
            return ("IDENTIFIER", tok[1])

        if tok[0] == "SIGN" and tok[1] == "(":
            self.match("SIGN", "(")
            expr = self.parse_expression()
            self.match("SIGN", ")")
            return expr

        raise SyntaxError(f"Invalid expression {tok}")


# MAIN

def run_compiler(source_code):
    tokens = lexical_analyzer_from_text(source_code)
    parser = Parser(tokens)
    ast = parser.parse_program()

    print("\nTOKENS:")
    for t in tokens:
        print(t)

    print("\nAST:")
    print(ast)


if __name__ == "__main__":
    print("Enter your code (finish with an empty line):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    source_code = "\n".join(lines)
    run_compiler(source_code)
