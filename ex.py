# S := A | [S]

from __future__ import annotations
from typing import Any, List, Union, Iterable
import abc


class Valable(abc.ABC):
    def eval(self, env: Env) -> Union[S, A]:
        raise Exception("not implemented!")


class A(Valable):
    def eval(self, env: Env) -> Union[S, A]:
        return self


class Void(A):
    def __str__(self) -> str:
        return "void"


class Proc(A):
    def __init__(self, env: Env, names: S, body: Union[S, A]):
        self.env = env
        self.names = names
        self.body = body

    def apply(self, env: Env, *args: Union[S, A]) -> Union[S, A]:
        new_env = self.env.copy()
        for n, v in env.kv.items():
            new_env.extend(n, v)
        for n, v in zip(self.names, args):
            new_env.extend(n, v)
        return self.body.eval(new_env)


class Id(A):
    def __init__(self, v: str):
        self.name = v

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Id):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def eval(self, env: Env) -> Union[S, A]:
        return env[self]

    def __str__(self) -> str:
        return f"{self.name}"


class Int(A):
    def __init__(self, v: int):
        self.val = v

    def __str__(self) -> str:
        return str(self.val)


class StringLiteral(A):
    pass


# class Print(Proc):
#     def apply(self, env: Env, *args) -> :
#         print(args[0])


class AddOp(Proc):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "+"

    def apply(self, env: Env, *args: Union[S, A]) -> Union[S, A]:
        x, y = args
        assert isinstance(x, Int)
        assert isinstance(y, Int)
        return Int(x.val + y.val)


class S(Iterable[Union[S, A]]):
    def __init__(self, *body: Union[S, A]):
        self.body = list(body)

    def __getitem__(self, idx) -> Union[S, A]:
        return self.body[idx]

    def __iter__(self) -> Iterable[Union[S, A]]:
        for item in self.body:
            yield item

    def __str__(self) -> str:
        return f"({' '.join(str(x) for x in self.body)})"

    def eval(self, env: Env) -> Union[S, A]:
        valuated = []
        for arg in self.body:
            valuated.append(arg.eval(env))
        assert isinstance(valuated[0], Proc), f"{valuated[0]} is not callable!"
        return valuated[0].apply(env, *valuated[1:])


class Let(S):
    def __init__(self, binds: S, body: Union[S, A]):
        self.binds = binds
        self.scope: Union[S, A] = body

    def eval(self, env) -> Union[S, A]:
        ext = env.copy()
        for b in self.binds:
            assert isinstance(b, S)
            ext.extend(b[0], b[1].eval(env))
        return self.scope.eval(ext)

    def __str__(self) -> str:
        return f"(let {self.binds} {self.scope})"


class Lambda(S):
    def __init__(self, names: S, body: Union[S, A]):
        self.names = names
        self.func = body

    def eval(self, env, *args) -> Union[S, A]:
        ret = Proc(env, self.names, self.func)
        return ret

    def __str__(self) -> str:
        return f"(lambda {self.names} {self.func})"


class Env:
    def __init__(self, kv=None) -> None:
        if kv:
            self.kv = kv.copy()
        else:
            self.kv = {}

    def extend(self, key, value) -> None:
        # print(f"extend {key}")
        self.kv[key] = value

    def __getitem__(self, val):
        try:
            return self.kv[val]
        except KeyError as e:
            print(f"{val} not found")
            raise

    def copy(self) -> Env:
        return Env(self.kv)

    def __str__(self) -> str:
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

# test1 = Let(S(S(Id("x", 200))), Let(S(

print("input ast:", test1)

print(test1.eval(env))
