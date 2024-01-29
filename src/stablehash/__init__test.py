from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from uuid import UUID

from stablehash import stablehash


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
    assert stablehash({"key": "value"}, algorithm="md5").hexdigest() == "d5994850379366e314563ea555532052"
    assert stablehash([1, 2, 3], algorithm="md5").hexdigest() == "c8b541e613f5e7708f0553221e2725d5"
    assert stablehash((1, 2, 3), algorithm="md5").hexdigest() == "f1a8fe053f96bb01977d521912b3132f"
    assert stablehash({1, 2, 3}, algorithm="md5").hexdigest() == "9c6723e0da429c60295de72138e044c3"
    assert stablehash(frozenset({1, 2, 3}), algorithm="md5").hexdigest() == "ad8dc7fa75828154da48a62195f3d960"
    assert stablehash(MyDataclass(65, "2"), algorithm="md5").hexdigest() == "f98412096cfd833d36960628f36abb78"
    assert stablehash(Picklable(65, "2"), algorithm="md5").hexdigest() == "4bfe8c9b9e4dc02f0e63632ef33f365f"
    assert stablehash(datetime(2021, 1, 1, 0, 0, 0), algorithm="md5").hexdigest() == "a6d637e693ec7994b48c21e18162f1bd"
    assert (
        stablehash(datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc), algorithm="md5").hexdigest()
        == "f25ce0bb0171aacc5d2ea6d32f81137b"
    )
    assert stablehash(date(2021, 1, 1), algorithm="md5").hexdigest() == "a8d008bc6c73f527333b3d40726c7e1f"
    assert stablehash(time(0, 0, 0), algorithm="md5").hexdigest() == "531c98aced815358bb7375c5948d0d82"
    assert stablehash(timedelta(seconds=1), algorithm="md5").hexdigest() == "e5fe3b7bf1b4ca1fb9ba5bfe886fbff5"
    assert (
        stablehash(UUID("00000000-0000-0000-0000-000000000000"), algorithm="md5").hexdigest()
        == "34fa1fac0804eaebe1a8a3adce7cef3f"
    )
