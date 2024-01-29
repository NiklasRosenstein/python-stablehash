__version__ = "0.1.0"

import hashlib
from typing import Any

from ._tokenize import tokenize

_sentinel = object()


class stablehash:
    """A fast and stable hash function for Python objects."""

    def __init__(self, data: Any = _sentinel, *, algorithm: str = "blake2b") -> None:
        """Create a new :class:`stablehash` instance.

        :param data: Data to hash.
        :param algorithm: The hash algorithm to use. Defaults to ``"blake2b"``.
        """

        self._hasher = hashlib.new(algorithm)
        if data is not _sentinel:
            self.update(data)


    def update(self, x: Any) -> None:
        """Update the hash with the specified object."""

        for token in tokenize(x):
            self._hasher.update(token)

    def digest(self) -> bytes:
        """Return the digest of the objects hashed so far."""

        return self._hasher.digest()

    def hexdigest(self) -> str:
        """Return the hex digest of the objects hashed so far."""

        return self._hasher.hexdigest()
