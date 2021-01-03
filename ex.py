# S := A | [S]

from __future__ import annotations
from typing import Any, List, Union


class A:
    def eval(self, env):
        return self
        # raise Exception("Not implemented!", type(self))


class Callable(A):
    def apply(self, env):
        raise Exception("not implemented!")


class Id(A):
    def __init__(self, v):
        self.name = v

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def eval(self, env):
        return env[self]


class Int(A):
    def __init__(self, v: int):
        self.val = v

    def eval(self, env):
        return self

    def __str__(self):
        return str(self.val)


class StringLiteral(A):
    pass


class AddOp(Callable):
    def __init__(self):
        pass

    def apply(self, x, y):
        assert isinstance(x, Int)
        assert isinstance(y, Int)
        return Int(x.val + y.val)


class Let(Callable):
    def __init__(self, binds, body):
        self.binds = binds
        self.body = body

    def eval(self, env):
        ext = env.copy()
        for b in self.binds:
            ext.extend(b[0], b[1].eval(env))
        return self.body.eval(ext)


class Lambda(Callable):
    def __init(self, names, body):
        self.names = names
        self.body = body

    def apply(self, env, *args):
        assert self.names == len(args)
        env = env.copy()
        for name, value in zip(self.names, args):
            env.extend(name, value)
        return self.body.eval(env)


class Env:
    def __init__(self, kv=None):
        if kv:
            self.kv = kv.clone()
        else:
            self.kv = {}

    def extend(self, key, value):
        self.kv[key] = value

    def __getitem__(self, val):
        return self.kv[val]

    def copy(self):
        return Env(self.kv)


class S(A):
    def __init__(self, *body):
        self.body = body

    def __getitem__(self, idx):
        return self.body[idx]

    def __iter__(self):
        if isinstance(self.body, A):
            yield self.body
        else:
            for item in self.body:
                yield item

    def eval(self, env: Env):
        if isinstance(self.body, A):
            return self.body
        valuated = []
        for arg in self.body:
            valuated.append(arg.eval(env))
        assert isinstance(valuated[0], Callable), f"{valuated[0]} is not callable!"
        return valuated[0].apply(*valuated[1:])


#   ((lambda (x) (lambda (x) x)) 5)

env = Env()

test1 = Let(S(S(Id("x"), Int(5))), Id("x"))


test2 = Let(S(S(Id("x"), Int(5)), S(Id("y"), Int(2))), S(AddOp(), Id("y"), Id("x")))

test3

print(test2.eval(env))
