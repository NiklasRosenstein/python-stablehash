import abc
import struct
from abc import ABC
from dataclasses import fields, is_dataclass
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:
    from _typeshed import DataclassInstance
else:
    DataclassInstance = ABC


def fqn(x: type[Any]) -> str:
    return f"{x.__module__}.{x.__qualname__}"


def tokenize(x: Any) -> Iterable[bytes]:

    # Produce an opening/ending token to indicate the type of the object being hashed. This is
    # to minimize the chances that consecutive hashes of multiple objects imitate the hash of a
    # single object (e.g. "abc" vs. "ab" + "c"), as well as encoding the actual type of the object.
    yield fqn(type(x)).encode("utf8")
    yield b"["

    match x:
        case None:
            yield b""
        case bool():
            yield b"1" if x else b"0"
        case int():
            bits = x.bit_length() // 8 + 1
            yield x.to_bytes(bits, "little")
        case float():
            yield struct.pack("f", x)
        case str():
            # TODO(@niklas): Is there any way we can grab the actual in-memory representation of the string
            #   instead of encoding it? That should yield significant performance improvements. We could
            #   extracting the memory view of the string using the C API?..
            yield x.encode("utf-8")
        case bytes():
            yield x
        case tuple() | list():
            yield from (b for item in x for b in tokenize(item))
        case set() | frozenset():
            yield from (b for item in sorted(x) for b in tokenize(item))
        case dict():
            for key, value in x.items():
                yield from tokenize(key)
                yield from tokenize(value)
        case Dataclass():
            for field in fields(x):
                yield from tokenize(field.name)
                yield from tokenize(getattr(x, field.name))
        case Picklable():
            yield from tokenize(x.__getstate__())
        case _:
            raise TypeError(f"object of type {fqn(type(x))} is not consistent-hashable")

    yield b"]"


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
