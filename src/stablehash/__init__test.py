from stablehash import stablehash


def test__stablehash() -> None:
    assert stablehash(42, algorithm="md5").hexdigest() == "6d2cdfd21468e0ec822bcfbefc38c73d"
    assert stablehash({"key": "value"}, algorithm="md5").hexdigest() == "d5994850379366e314563ea555532052"
    assert stablehash([1, 2, 3], algorithm="md5").hexdigest() == "c8b541e613f5e7708f0553221e2725d5"
    assert stablehash((1, 2, 3), algorithm="md5").hexdigest() == "f1a8fe053f96bb01977d521912b3132f"
    assert stablehash({1, 2, 3}, algorithm="md5").hexdigest() == "9c6723e0da429c60295de72138e044c3"
    assert stablehash(frozenset({1, 2, 3}), algorithm="md5").hexdigest() == "ad8dc7fa75828154da48a62195f3d960"
