import lexerProg


class Interpreter:
    def vis(self, node):
        method_name = f'vis_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)

    def vis_NumberNode(self, node):
        return Number(node.tok.value).set_pos(node.pos_start, node.pos_end)

    def vis_BinOpNode(self, node):
        left = self.vis(node.left_node)
        right = self.vis(node.right_node)
        if node.op_tok.type == lexerProg.TT_PLUS:
            result = left.add(right)
        elif node.op_tok.type == lexerProg.TT_MINUS:
            result = left.sub(right)
        elif node.op_tok.type == lexerProg.TT_MUL:
            result = left.mult(right)
        elif node.op_tok.type == lexerProg.TT_DIV:
            result = left.div(right)
        return result.set_pos(node.pos_start, node.pos_end)

    def vis_UnaryOpNode(self, node):
        number = self.vis(node.node)
        if node.op_tok.type == lexerProg.TT_MINUS:
            number = number.mult(Number(-1))
        return number.set_pos(lexerProg.pos_start, node.pos_end)
    def vis_VarAccess(self, node):
        vars = node.vars



class Number:
    def __init__(self, value):
        self.pos_end = None
        self.pos_start = None
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def mult(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def div(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)

    def __repr__(self):
        return f'{self.value}'


class Symbol:
    def __init__(self):
        self.symbol = {}
        self.parent = None

    def get(self, name):
        value = self.sybmol.get(name,None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbol[name] = value

    def remove(self,name):
        del self.symbol[name]
