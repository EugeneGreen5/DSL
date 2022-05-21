import lexerProg


class Parser:
    def __init__(self, tokens):
        self.current_tok = None
        self.tokens = tokens
        self.tok_id = -1  # Текущий индекс токена
        self.advance()

    def advance(self):
        self.tok_id += 1
        if self.tok_id < len(self.tokens):
            self.current_tok = self.tokens[self.tok_id]
        return self.current_tok

    def parse(self):
        res = self.expression()
        return res

    def factor(self):
        tok = self.current_tok
        if tok.type in (lexerProg.TT_MINUS, lexerProg.TT_PLUS):
            self.advance()
            factor = self.factor()
            return lexerProg.UnaryOpNode(tok, factor)
        elif tok.type in (lexerProg.TT_INT, lexerProg.TT_FLOAT):
            self.advance()
            return lexerProg.NumberNode(tok)
        elif tok.type == lexerProg.TT_LPAREN:
            self.advance()
            expression = self.expression()
            if self.current_tok.type == lexerProg.TT_RPAREN:
                self.advance()
                return expression

    def summand(self):
        return self.operation(self.factor, (lexerProg.TT_MUL, lexerProg.TT_DIV))

    def expression(self):
        if self.current_tok.matcher(lexerProg.TT_VAR, 'VAR'):
            self.advance()
        return self.operation(self.summand, (lexerProg.TT_PLUS, lexerProg.TT_MINUS))

    def operation(self, func, ops):
        left = func()
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = lexerProg.BinOpNode(left, op_tok, right)
        return left
