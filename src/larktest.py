from os import chdir

from lark import Lark

import output
import transformer

chdir("/workspace/src")
program = open("program.txt").read()

with open("grammar.lark", encoding="utf-8") as grammar:
    LP = Lark(grammar.read(), start="program")

tree = LP.parse(program)
trans = transformer.my_transformer()
testenv = transformer.Environment(None)
# print(tree.pretty())
ret = trans.program(tree, testenv)
print(testenv.outbuf.printed)
# print(ret)
