# 🧠 Python Mini Compiler (Lexer + Parser)

This repository contains a small **Lexical Analyzer (lexer)** and a **Recursive Descent Parser** implemented in **Python**.  
The code is an educational mini-compiler front-end that tokenizes input source code and produces a simple Abstract Syntax Tree (AST).

> **This README documents exactly what the provided `compiler.py` does** — the token types it recognizes, the grammar the parser accepts, how to run it, its current limitations, and suggested improvements.

---

## 📂 Files (expected in project folder)
- `compiler.py` — the Python program containing lexer + parser + `main`.
- `README.md` — this file.
- `sample_input.txt` — (recommended) sample code for quick testing.

---

## 🔧 Requirements
- Python 3.8+ installed.
- No external packages required (uses only Python standard library).

---

## 📌 What this program does (quick summary)
1. **Lexical analysis**: converts source text into a stream of tokens. Each token is a tuple:(TYPE, lexeme, line, col)
where `line` and `col` are the starting line and column of the token.
2. **Parsing**: a recursive-descent parser consumes tokens and builds a simple AST.
3. **Output**: prints the token stream and the AST.

---

## 🔎 Token definitions (exactly as in `compiler.py`)
```python
KEYWORDS = {"int", "float", "double", "if", "else"}
OPERATORS = {'+', '-', '*', '/', '%', '=', '<', '>', '!'}
DOUBLE_OPERATORS = {"==", "!=", "<=", ">="}
SIGNS = {';', '(', ')', '{', '}'}
Token types produced by the lexer

KEYWORD — lexeme is one of the keywords (e.g. int, if).

IDENTIFIER — variable names; start with a letter or _, continue with letters, digits or _.

INTEGER — integer literal (sequence of digits; no decimal points).

OPERATOR — single or double operators; double operators (==, !=, <=, >=) are recognized.

SIGN — punctuation symbols ; ( ) { }.

UNKNOWN — any character sequence that does not match above rules.

EOF — end-of-input marker appended at the end of token list.

Each token is appended as a tuple like ("KEYWORD", "int", 1, 1).

⚙️ Lexer behavior (detailed)

Whitespace (space, tab, newline) is ignored except newline increments line and resets col.

Identifiers/keywords: start in state 1 when the first char is isalpha() or _, continue while isalnum() or _.

Integers: state 3 — continue while digits. No floats.

Operators: when an operator char found, lexer attempts to form a two-character operator by peeking the next char; if the pair is in DOUBLE_OPERATORS, it forms a single OPERATOR token for the pair.

Signs: ; ( ) { } are emitted as SIGN.

If a character does not match any recognized class, an UNKNOWN token is emitted for that buffer.

At the end, ("EOF", "", line, col) is appended.

🧭 Parser behavior (detailed)

The parser is a recursive-descent parser implemented in class Parser and expects the token stream from the lexer (ending with EOF).

Main entry

parse_program() → returns ("PROGRAM", [statement, statement, ...])

Supported statements

Declaration

type IDENTIFIER ;
type IDENTIFIER = expression ;

(type is a keyword in {"int", "float", "double"})

Assignment

IDENTIFIER = expression ;

If-statement

if ( expression ) statement

Note: after if(...) only a single statement is accepted (no {} block support in parser).

Expressions parsed

expression handles binary operators of precedence levels:

term combined with { +, -, <, >, == }

term combines factor with { *, / }

factor is INTEGER or IDENTIFIER or ( expression )

AST nodes are simple tuples, for example:

-("NUMBER", "5")

-("IDENTIFIER", "x")

-("BIN_OP", "+", left_node, right_node)

-("DECLARATION", "int", "x", expr_or_None)

-("ASSIGNMENT", "x", expr)

-("IF", condition_expr, statement_node)

📖 Grammar (exactly as implemented)
program       → statement*
statement     → declaration | assignment | if_statement

declaration   → type IDENTIFIER ;
              | type IDENTIFIER = expression ;

assignment    → IDENTIFIER = expression ;

if_statement  → if ( expression ) statement

expression    → term ((+ | - | < | > | ==) term)*
term          → factor ((* | /) factor)*
factor        → INTEGER | IDENTIFIER | ( expression )

Example Input (sample_input.txt)
int x = 5;
x = x + 3;

if (x > 2)
x = x * 2;

Example Output (what compiler.py prints)

Tokens

('KEYWORD', 'int', 1, 1)
('IDENTIFIER', 'x', 1, 5)
('OPERATOR', '=', 1, 7)
('INTEGER', '5', 1, 9)
('SIGN', ';', 1, 10)
('IDENTIFIER', 'x', 2, 1)
('OPERATOR', '=', 2, 3)
('IDENTIFIER', 'x', 2, 5)
('OPERATOR', '+', 2, 7)
('INTEGER', '3', 2, 9)
('SIGN', ';', 2, 10)
('KEYWORD', 'if', 4, 1)
('SIGN', '(', 4, 4)
('IDENTIFIER', 'x', 4, 5)
('OPERATOR', '>', 4, 7)
('INTEGER', '2', 4, 9)
('SIGN', ')', 4, 10)
('IDENTIFIER', 'x', 5, 1)
('OPERATOR', '=', 5, 3)
('IDENTIFIER', 'x', 5, 5)
('OPERATOR', '*', 5, 7)
('INTEGER', '2', 5, 9)
('SIGN', ';', 5, 10)
('EOF', '', 6, 1)

AST 

('PROGRAM', [
  ('DECLARATION', 'int', 'x', ('NUMBER', '5')),
  ('ASSIGNMENT', 'x', ('BIN_OP', '+', ('IDENTIFIER', 'x'), ('NUMBER', '3'))),
  ('IF', ('BIN_OP', '>', ('IDENTIFIER', 'x'), ('NUMBER', '2')),
       ('ASSIGNMENT', 'x', ('BIN_OP', '*', ('IDENTIFIER', 'x'), ('NUMBER', '2')))
  )
])

How to run

Option A — Interactive input (default main in compiler.py)
python compiler.py

Then paste or type code line-by-line.

Finish input by pressing Enter on an empty line.

The program prints tokens and AST.


Option B — Run using sample_input.txt (recommended)

1-Create sample_input.txt in the same folder and paste the example input into it.

2-Replace the bottom interactive block of compiler.py with this small change (or add as the faster path):

if __name__ == "__main__":
    import os, sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path, "r") as f:
            source_code = f.read()
    elif os.path.exists("sample_input.txt"):
        with open("sample_input.txt", "r") as f:
            source_code = f.read()
    else:
        print("Enter your code (finish with an empty line):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        source_code = "\n".join(lines)

    run_compiler(source_code)

3-Run:

python compiler.py sample_input.txt

⚠️ Known limitations (be explicit)

Integer literals only: floats/doubles not recognized as literals.

float and double are keywords but their literal syntax is not supported.

else keyword exists in KEYWORDS but parser has no else handling — using else will cause a SyntaxError.

Parser accepts only one statement after if (no { ... } blocks).

Lexer recognizes % and ! as operators, but parser does not implement % or unary !.

No support for comments (e.g., // ... or /* ... */) or string literals.

Error messages raised by the parser are SyntaxError(f"Unexpected token {tok}") — they do not automatically print the human-friendly line/column; tokens carry that info and can be used to improve error reporting.

🎯 Purpose

This project is intended for educational use in compiler construction courses.


