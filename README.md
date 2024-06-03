# stablehash

The `stablehash` module provides a "pure" hash function that is stable across Python processes and runs. This is in
contrast to the builtin `hash()` function, which may return a different value for the same input in separate
invokations even with the Python version.

We support most Python built-in types, including mutable types such as `list` and `dict`, as well as dataclasses. The
default internal hash algorithm is Blake2b, but this can be changed by passing a different `hashlib` algorithm to the
`stablehash` function.

## Usage

```python
from stablehash import stablehash

assert stablehash({"key": "value"}, algorithm="md5").hexdigest() == 'd5994850379366e314563ea555532052'
```

## API

### `stablehash(obj=..., *, algorithm="blake2b")`

Returns a `hashlib`-compatible object with the given algorithm and the hash of the given object. The algorithm must be
one of the algorithms supported by `hashlib`.

### `stablehash.update(obj)`

Updates the hash with the given object. If the object is not supported, a `TypeError` is raised.

### `stablehash.digest()`

Returns the digest of the hash as a bytes object.

### `stablehash.hexdigest()`

Returns the digest of the hash as a string object.

## Supported types

The following types are supported:

- `None`
- `bool`
- `int`
- `float`
- `str`
- `bytes`
- `tuple`
- `list`
- `set`
- `frozenset`
- `dict`
- `@dataclass` objects
- `datetime` objects (`datetime`, `date`, `time` and `timedelta`)
- `uuid.UUID`
- Picklable objects (e.g. those that implement `__getstate__()`)
- `type` objects (by their full qualified name)
