import random

from lark import Transformer

import output


# 関数や変数の名前空間を実装するクラス
class Environment:
    def __init__(self, parent_env):
        self._parent_env = parent_env
        self._env = dict()
        self.outbuf = output.outbuf()

    def get(self, key):
        value = self._env.get(key, None)
        if value is None:
            if not self._parent_env:
                print(key + " is not defined.")
                print(self._env)
                return None
            value = self._parent_env.get(key)
        return value

    def set(self, key, value):
        self._env[key] = value

    def delete(self, key):
        value = self._env.get(key, None)
        if not value:
            pass
        del self._env[key]

    def allenvs(self):
        return self._env


# 関数(composed by tree)を実装するクラス
class Function:
    def __init__(self, parameters, tree):
        self._parameters = parameters
        self._tree = tree

    def parameters(self):
        return self._parameters

    def tree(self):
        return self._tree


# パースして得た木を受け取って、実際に処理するクラス
class my_transformer(Transformer):
    def __init__(self, env: Environment) -> None:
        self.env = env

    def __default__(self, tree):
        raise

    def visit(self, tree):
        f = getattr(self, tree.data, self.__default__)
        return f(tree)

    def program(self, tree):
        for sub_tree in tree.children:
            r = self.visit(sub_tree)
        return r

    def def_func(self, tree):
        key = self.visit(tree.children[0])
        parameters = []
        if len(tree.children) > 2:
            parameters = [self.visit(child) for child in tree.children[1:-1]]
        ast = tree.children[-1]

        func = Function(parameters, ast)
        self.env.set(key, func)
        self.env.outbuf.printed += "function-define OK.\n"

    def if_mine(self, tree):
        if self.visit(tree.children[0]) > 0:
            self.visit(tree.children[1])

    def loop(self, tree):
        while self.visit(tree.children[0]) > 0:
            self.visit(tree.children[1])

    def undef_func(self, tree):
        key = self.visit(tree.children[0])
        self.env.delete(key)

    def def_var(self, tree):
        key = self.visit(tree.children[0])
        value = self.visit(tree.children[1])
        self.env.set(key, value)

    def return_state(self, tree):
        return self.visit(tree.children[0])

    def print_char(self, tree):
        r = self.visit(tree.children[0])
        self.env.outbuf.add(r)

    def print_sym(self, tree):
        r = self.visit(tree.children[0])
        # if r.__class__.__name__ == Function:
        #     env.outbuf.add("***this symbol is function!***")
        #     pass
        self.env.outbuf.add(str(int(r)) + " ")

    def publish(self, tree):
        self.env.outbuf.out()

    def flash(self, tree):
        self.env.outbuf.clear()

    def new_symbol(self, tree):
        return tree.children[0].value

    def parameter(self, tree):
        return tree.children[0].value

    def function_call(self, tree):
        func = self.visit(tree.children[0])

        arguments = [self.visit(c) for c in tree.children[1:]]
        if len(arguments) != len(func.parameters()):
            raise BaseException("Number of arguments is wrong")

        local_env = Environment(self.env)
        for (k, v) in zip(func.parameters(), arguments):
            local_env.set(k, v)
        temptrans = my_transformer(local_env)
        r = temptrans.visit(func.tree())
        self.env.outbuf.printed += local_env.outbuf.printed
        return r

    def addition(self, tree):
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])
        return left + right

    def substraction(self, tree):
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])
        return left - right

    def multiplication(self, tree):
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])
        return left * right

    def divisition(self, tree):
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])
        return left / right

    def dice(self, tree):
        left = int(self.visit(tree.children[0]))
        right = int(self.visit(tree.children[1]))
        if right < 1:
            right = 6
        r = 0
        for i in range(left):
            r = r + random.randint(1, right)
        return float(r)

    def not_mine(self, tree):
        r = self.visit(tree.children[0])
        return not r

    def greater(self, tree):
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])
        return left < right

    def less(self, tree):
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])
        return left > right

    def equal(self, tree):
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])
        return left == right

    def symbol(self, tree):
        key = tree.children[0].value
        return self.env.get(key)

    def number(self, tree):
        return float(tree.children[0].value)

    def sentence(self, tree):
        r = ""
        for s in tree.children[0:]:
            r += str(s.value)
        return r + " "
