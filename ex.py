# S := A | [S]

from __future__ import annotations
from typing import Any, List, Union


class A:
    def eval(self, env):
        return self
        # raise Exception("Not implemented!", type(self))


class Proc(A):
    def __init__(self, env, names, body):
        self.env = env
        self.names = names
        self.body = body

    def apply(self, env, *args):
        # print(env)
        new_env = self.env.copy()
        for n, v in env.kv.items():
            new_env.extend(n, v)
        for n, v in zip(self.names, args):
            new_env.extend(n, v)
        return self.body.eval(new_env)


class Id(A):
    def __init__(self, v):
        self.name = v

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def eval(self, env):
        return env[self]

    def __str__(self):
        return f"{self.name}"


class Int(A):
    def __init__(self, v: int):
        self.val = v

    def __str__(self):
        return str(self.val)


class StringLiteral(A):
    pass


class AddOp(Proc):
    def __init__(self):
        pass

    def __str__(self):
        return "+"

    def apply(self, env, *args):
        x, y = args
        assert isinstance(x, Int)
        assert isinstance(y, Int)
        return Int(x.val + y.val)


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

    def __str__(self):
        return f"({' '.join(str(x) for x in self.body)})"

    def eval(self, env: Env):
        if isinstance(self.body, A):
            return self.body
        valuated = []
        for arg in self.body:
            valuated.append(arg.eval(env))
        assert isinstance(valuated[0], Proc), f"{valuated[0]} is not callable!"
        return valuated[0].apply(env, *valuated[1:])


class Let(S):
    def __init__(self, binds, body):
        self.binds = binds
        self.body = body

    def eval(self, env):
        ext = env.copy()
        for b in self.binds:
            ext.extend(b[0], b[1].eval(env))
        return self.body.eval(ext)

    def __str__(self):
        return f"(let {self.binds} {self.body})"


class Lambda(S):
    def __init__(self, names, body):
        self.names = names
        self.body = body

    def eval(self, env, *args):
        ret = Proc(env, self.names, self.body)
        return ret

    def __str__(self):
        return f"(lambda {self.names} {self.body})"


class Env:
    def __init__(self, kv=None):
        if kv:
            self.kv = kv.copy()
        else:
            self.kv = {}

    def extend(self, key, value):
        # print(f"extend {key}")
        self.kv[key] = value

    def __getitem__(self, val):
        try:
            return self.kv[val]
        except KeyError as e:
            print(f"{val} not found")
            raise

    def copy(self):
        return Env(self.kv)

    def __str__(self):
        return str(self.kv)


#   ((lambda (x) (lambda (x) x)) 5)

env = Env()

# test1 = Let(S(S(Id("x"), Int(5))), Id("x"))


# test2 = Let(S(S(Id("x"), Int(5)), S(Id("y"), Int(2))), S(AddOp(), Id("y"), Id("x")))

# test1 = S(Lambda(S(Id("x")), S(AddOp(), Int(2), Id("x"))), Int(2))

# test3

test1 = S(
    Let(S(S(Id("x"), Int(5))), Lambda(S(Id("z")), S(AddOp(), Id("x"), Id("z")))), Int(3)
)

print("input ast:", test1)

print(test1.eval(env))
