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


class Identifier(A):
    def __init__(self, v):
        self.name = v

    def eval(self, env):
        return env[self.name]


class Integer(A):
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

    def eval(self, env):
        return self

    def apply(self, x, y):
        assert isinstance(x, Integer)
        assert isinstance(y, Integer)
        return Integer(x.val + y.val)


class Lambda(Callable):
    def __init(self, names, body):
        self.names = names
        self.body = body

    def apply(self, env, *args):
        assert self.names == len(args)
        env = env.clone()
        for name, value in zip(self.names, args):
            env.extend(name, value)
        return self.body.eval(env)


class Func(A):
    pass


class Env:
    def __init__(self, kv=None):
        if kv:
            self.kv = kv.clone()
        else:
            self.kv = {}

    def extend(self, key, value):
        self.kv[key] = value


class S:
    def __init__(self, body: Union[A, List[S]]):
        self.body = body

    def eval(self, env: Env):
        if isinstance(self.body, A):
            return self.body
        valuated = []
        for arg in self.body:
            valuated.append(arg.eval(env))
        assert isinstance(valuated[0], Callable)
        return valuated[0].apply(*valuated[1:])


#   ((lambda (x) (lambda (x) x)) 5)

env = Env()
print(test.eval(env))
