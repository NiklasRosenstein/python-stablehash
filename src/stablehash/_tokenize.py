import abc
import struct
from abc import ABC
from dataclasses import fields, is_dataclass
from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, Any, Protocol
from uuid import UUID

if TYPE_CHECKING:
    from _typeshed import DataclassInstance
else:
    DataclassInstance = ABC


def fqn(x: type[Any]) -> str:
    return f"{x.__module__}.{x.__qualname__}"


def tokenize(hasher: "Hasher", x: Any, *, header: bool = True) -> None:

    # Produce an opening/ending token to indicate the type of the object being hashed. This is
    # to minimize the chances that consecutive hashes of multiple objects imitate the hash of a
    # single object (e.g. "abc" vs. "ab" + "c"), as well as encoding the actual type of the object.
    if header:
        hasher.update(fqn(type(x)).encode("utf8"))
        hasher.update(b"[")

    match x:
        case None:
            pass
        case bool():
            hasher.update(b"1" if x else b"0")
        case int():
            bits = x.bit_length() // 8 + 1
            hasher.update(x.to_bytes(bits, "little"))
        case float():
            hasher.update(struct.pack("f", x))
        case str():
            # TODO(@niklas): Is there any way we can grab the actual in-memory representation of the string
            #   instead of encoding it? That should yield significant performance improvements. We could
            #   extracting the memory view of the string using the C API?..
            hasher.update(x.encode("utf-8"))
        case bytes():
            hasher.update(x)
        case tuple() | list():
            for item in x:
                tokenize(hasher, item)
        case set() | frozenset():
            for item in sorted(x):
                tokenize(hasher, item)
        case dict():
            for key, value in x.items():
                tokenize(hasher, key)
                tokenize(hasher, value)
        case Dataclass():
            for field in fields(x):
                tokenize(hasher, field.name)
                tokenize(hasher, getattr(x, field.name))
        case datetime() | date() | time():
            tokenize(hasher, x.isoformat(), header=False)
        case timedelta():
            tokenize(hasher, x.total_seconds(), header=False)
        case UUID():
            tokenize(hasher, x.int, header=False)
        case Picklable():
            tokenize(hasher, x.__getstate__())
        case _:
            raise TypeError(f"object of type {fqn(type(x))} is not consistent-hashable")

    if header:
        hasher.update(b"]")


class Dataclass(DataclassInstance):

    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        return is_dataclass(__subclass)


class Picklable(ABC):

    @abc.abstractmethod
    def __getstate__(self) -> Any: ...

    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        return hasattr(__subclass, "__getstate__")


class Hasher(Protocol):

    def update(self, __data: bytes) -> None: ...
