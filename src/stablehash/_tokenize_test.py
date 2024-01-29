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


def test__tokenize__datetime() -> None:
    from datetime import datetime, timezone

    assert b"".join(tokenize(datetime(2021, 1, 1, 0, 0, 0))) == b"datetime.datetime[2021-01-01T00:00:00]"
    assert (
        b"".join(tokenize(datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)))
        == b"datetime.datetime[2021-01-01T00:00:00+00:00]"
    )


def test__tokenize__uuid() -> None:
    from uuid import UUID

    assert b"".join(tokenize(UUID("00000000-0000-0000-0000-000000000000"))) == b"uuid.UUID[\x00]"
