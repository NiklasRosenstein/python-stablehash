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

assert stablehash({"key": "value"}, algorithm="md5").hexdigest() == "0ea2506ffbeef2699760d422d7a8b971"
```

## Compatibility notes

### Since `0.3.x`
Hashing semantics are changed for certain inputs to improve stability:

* Dictionaries now hash independent of key insertion order (i.e., equal dicts produce the same digest regardless of the order keys were added).  
* Serialize floats as IEEE-754 64-bit little-endian (`struct.pack('<d', x)`) to guarantee cross-platform stable digests.  

These changes may cause the digest produced for the same value to **differ from** the `0.2.x` series. The public API is unchanged, but we treat changes that alter produced hashes as breaking from a user's perspective. (See PR [#20](https://github.com/NiklasRosenstein/python-stablehash/pull/20) for background.)

<details>

<summary>
<b>What should downstream users do?</b>
</summary>

* If your project depends on exact hash outputs (for example, using them as file identifiers or data fingerprints), either:  

  * pin an **upper bound** to the previous minor series: `stablehash >=0.2.0, <0.3.0`, or  
  * upgrade to `0.3.x` and **re-generate** your stored hashes.     

</details>

## Versioning policy

This project follows Semantic Versioning where applicable. During initial development (`0.y.z`), the public API should not be considered stable and **breaking changes may occur in a minor bump**. We therefore use the minor version to signal changes that can alter produced digests (semantic changes). Downstream users are encouraged to **specify an upper bound** on the minor version when depending on `0.y.z` releases. 

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
