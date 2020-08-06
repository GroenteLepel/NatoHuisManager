import os
from lark import Lark
from .nodes import BuildAST, ValNode

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "roll.grammar")) as f:
    grammar = f.read()

calc_parser = Lark(grammar, parser='earley')


def as_ast(txt, env):
    tree = calc_parser.parse(txt)
    return BuildAST().transform(tree)


def calc(txt, env):
    tree = calc_parser.parse(txt)
    ast = BuildAST().transform(tree)
    val, description = ast.get(env)
    if ast.calcable:
        env.set("_", ValNode(val))
        return "{} -> {}".format(description, int(val))
    return description

def calc_and_val(txt, env):
    tree = calc_parser.parse(txt)
    ast = BuildAST().transform(tree)
    val, description = ast.get(env)
    if ast.calcable:
        env.set("_", ValNode(val))
        return "{} -> {}".format(description, int(val)), int(val)
    return description, 0

def calc_val_only(txt, env):
    tree = calc_parser.parse(txt)
    ast = BuildAST().transform(tree)
    val, description = ast.get(env)
    if ast.calcable:
        return int(val)
    return 0


def distr(txt, env):
    tree = calc_parser.parse(txt)
    ast = BuildAST().transform(tree)
    return ast.distribution(env)

