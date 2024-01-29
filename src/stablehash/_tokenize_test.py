from dataclasses import dataclass

from stablehash._tokenize import tokenize


@dataclass
class MyDataclass:
    a: int
    b: str


def test__tokenize__dataclass() -> None:
    assert (
        b"".join(tokenize(MyDataclass(65, "2")))
        == b"stablehash._tokenize_test.MyDataclass[builtins.str[a]builtins.int[A]builtins.str[b]builtins.str[2]]"
    )


class Picklable:

    def __init__(self, a: int, b: str) -> None:
        self.a = a
        self.b = b

    def __getstate__(self) -> tuple[int, str]:
        return self.a, self.b


def test__tokenize__getstate() -> None:
    assert (
        b"".join(tokenize(Picklable(65, "2")))
        == b"stablehash._tokenize_test.Picklable[builtins.tuple[builtins.int[A]builtins.str[2]]]"
    )
