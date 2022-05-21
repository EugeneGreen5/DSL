import interpreterProg
import parserProg
import string

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_VAR = 'VAR'
TT_SIGN = 'SIGN'
TT_VAR_NAME = 'VAR_NAME'


DIGITS = '0123456789'
ALPHABET = string.ascii_letters
ALPHABET_DIGITS = ALPHABET + DIGITS


class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end

    def matcher(self, type, value):
        return self.type == type and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        else:
            return f'{self.type}'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def Token(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_SIGN))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_SIGN))
                self.advance()
            elif self.current_char in ALPHABET:
                tokens.append(self.make_string())
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()

        return tokens

    def make_number(self):
        num_str = ''
        counter = 0
        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if counter == 1:
                    break
                counter += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if counter == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

    def make_string(self):
        id_string = ''
        while self.current_char is not None and self.current_char in ALPHABET_DIGITS + '_':
            id_string += self.current_char
            self.advance()
        if id_string == 'VAR':
            tok_type = TT_VAR
        else:
            tok_type = TT_VAR_NAME
        return Token(tok_type, id_string)


class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self):
        return f'{self.tok}'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f'({self.op_tok},{self.node})'


def run(text):
    lexer1 = Lexer(text)
    tokens = lexer1.Token()
    print(tokens)
    parser1 = parserProg.Parser(tokens)
    ast = parser1.parse()
    print(ast)
    interpreter1 = interpreterProg.Interpreter()
    result1 = interpreter1.vis(ast)
    return result1
