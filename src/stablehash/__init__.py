__version__ = "0.2.4"

import hashlib
from typing import Any

from ._tokenize import Hasher, tokenize

_sentinel = object()


class stablehash:
    """A fast and stable hash function for Python objects."""

    def __init__(self, data: Any = _sentinel, *, hasher: Hasher | None = None, algorithm: str = "blake2b") -> None:
        """Create a new :class:`stablehash` instance.

        :param data: Data to hash.
        :param algorithm: The hash algorithm to use. Defaults to ``"blake2b"``.
        """

        self._hasher: Hasher = hasher or hashlib.new(algorithm)
        if data is not _sentinel:
            self.update(data)

    def __eq__(self, other: object) -> bool:
        """Check if two stablehash instances are equal based on their digests."""

        if not isinstance(other, stablehash):
            return NotImplemented
        return self._hasher.digest() == other._hasher.digest()

    def __ne__(self, other: object) -> bool:
        """Check if two stablehash instances are not equal based on their digests."""

        if not isinstance(other, stablehash):
            return NotImplemented
        return self._hasher.digest() != other._hasher.digest()

    def update(self, x: Any) -> None:
        """Update the hash with the specified object."""

        tokenize(self._hasher, x)

    def digest(self) -> bytes:
        """Return the digest of the objects hashed so far."""

        return self._hasher.digest()

    def hexdigest(self) -> str:
        """Return the hex digest of the objects hashed so far."""

        return self._hasher.hexdigest()
