from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from uuid import UUID

from stablehash import stablehash

_nested_dict_1 = {
    1: "int",
    "key": {
        "b": "k",
        "a": "val",
        "nested": {
            "x": [1, 2, {"m": 10, "n": [3, 4, 5]}],
            "y": {"tuple": (1, 2, 3), "set": {3, 2, 1}},
        },
    },
    "k": "v",
    (1, 2): "233",
    "complex": {
        ("tuple", 42): {"inner": {True: "yes", None: "nil"}},
        frozenset({1, 2, 3}): "frozen",
    },
}

_nested_dict_2 = {
    "complex": {
        frozenset({3, 2, 1}): "frozen",
        ("tuple", 42): {"inner": {None: "nil", True: "yes"}},
    },
    (1, 2): "233",
    1: "int",
    "k": "v",
    "key": {
        "a": "val",
        "b": "k",
        "nested": {
            "y": {"set": {1, 3, 2}, "tuple": (1, 2, 3)},
            "x": [1, 2, {"n": [3, 4, 5], "m": 10}],
        },
    },
}


@dataclass
class MyDataclass:
    a: int
    b: str


class Picklable:
    def __init__(self, a: int, b: str) -> None:
        self.a = a
        self.b = b

    def __getstate__(self) -> tuple[int, str]:
        return self.a, self.b


def test__stablehash() -> None:
    assert stablehash(42, algorithm="md5").hexdigest() == "6d2cdfd21468e0ec822bcfbefc38c73d"
    assert stablehash({"key": "value"}, algorithm="md5").hexdigest() == "0ea2506ffbeef2699760d422d7a8b971"
    assert (
        stablehash(_nested_dict_1, algorithm="md5").hexdigest() 
        == stablehash(_nested_dict_2, algorithm="md5").hexdigest() 
        == "2e510913c66105a8dd563e5111e3c809"
    )
    assert stablehash([1, 2, 3], algorithm="md5").hexdigest() == "c8b541e613f5e7708f0553221e2725d5"
    assert stablehash((1, 2, 3), algorithm="md5").hexdigest() == "f1a8fe053f96bb01977d521912b3132f"
    assert stablehash({1, 2, 3}, algorithm="md5").hexdigest() == "10bf2edb0a4badb2aa27e29fff846f46"
    assert stablehash(frozenset({1, 2, 3}), algorithm="md5").hexdigest() == "40fa72eac25be910504c3e8f60303501"
    assert stablehash(MyDataclass(65, "2"), algorithm="md5").hexdigest() == "f98412096cfd833d36960628f36abb78"
    assert stablehash(Picklable(65, "2"), algorithm="md5").hexdigest() == "4bfe8c9b9e4dc02f0e63632ef33f365f"
    assert stablehash(datetime(2021, 1, 1, 0, 0, 0), algorithm="md5").hexdigest() == "a6d637e693ec7994b48c21e18162f1bd"
    assert (
        stablehash(datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc), algorithm="md5").hexdigest()
        == "f25ce0bb0171aacc5d2ea6d32f81137b"
    )
    assert stablehash(date(2021, 1, 1), algorithm="md5").hexdigest() == "a8d008bc6c73f527333b3d40726c7e1f"
    assert stablehash(time(0, 0, 0), algorithm="md5").hexdigest() == "531c98aced815358bb7375c5948d0d82"
    assert stablehash(timedelta(seconds=1), algorithm="md5").hexdigest() == "7babeee6b6b1e1c94e5bbd6eed14811e"
    assert (
        stablehash(UUID("00000000-0000-0000-0000-000000000000"), algorithm="md5").hexdigest()
        == "34fa1fac0804eaebe1a8a3adce7cef3f"
    )
    assert stablehash(int, algorithm="md5").hexdigest() == "21a85b46a16a64f9c58f5402c4c11bf1"
    assert stablehash(str, algorithm="md5").hexdigest() == "fc1830dca524be291dcda6dbca7bd509"
    assert stablehash({int, str}, algorithm="md5").hexdigest() == "f4216c5b72f84c0e17bda6f365b99f52"
    assert stablehash(Path("foo"))
