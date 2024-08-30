"""
This implementation is largely based on the documentation by Tony Finch.
An article about it can be found here: https://dotat.at/@/2023-06-21-pcg64-dxsm.html

Copyright Tony Finch <dot@dotat.at>, Cambridge.

Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the
Software without restriction, including without
limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice
shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import os
import typing

__all__ = ("InternalPCG",)

MUL: typing.Final[int] = 15750249268501108917
BITSHIFT_128: typing.Final[int] = 1 << 128
BITSHIFT_64: typing.Final[int] = 1 << 64
MASK_128: typing.Final[int] = BITSHIFT_128 - 1
MASK_64: typing.Final[int] = BITSHIFT_64 - 1
MAGIC_NUMBER: typing.Final[float] = float.fromhex("0x1.0p-53")


class InternalPCG:
    state: int
    incr: int

    def __init__(self, state: int, incr: int) -> None:
        self.state = state
        self.incr = incr

    @classmethod
    def from_entropy(cls) -> "InternalPCG":
        return cls.from_seed(os.urandom(32))

    @classmethod
    def from_seed(cls, seed: bytes) -> "InternalPCG":
        if len(seed) < 32:
            raise ValueError("Seed must be 32 bytes long or greater.")

        state, incr = cls._unpack_seed(seed)
        return cls.from_state_incr(state, incr | 1)

    @classmethod
    def from_state_incr(cls, state: int, incr: int) -> "InternalPCG":
        self = cls(state, incr)
        self.state = (self.state + incr) % MASK_128
        self.pcg64_dxsm()
        return self

    @staticmethod
    def _unpack_seed(seed: bytes) -> typing.Tuple[int, int]:
        return (
            int.from_bytes(seed[:16], byteorder="little"),
            int.from_bytes(seed[16:32], byteorder="little"),
        )

    def pcg64_dxsm(self) -> int:
        self.state = (self.state * MUL + self.incr) % MASK_128

        high: int = (self.state >> 64) % MASK_64
        low: int = (self.state | 1) % MASK_64

        high = (high ^ (high >> 22)) % MASK_64
        high = (high * MUL) % MASK_64
        high = (high ^ (high >> 48)) % MASK_64
        return (high * low) % MASK_64

    def random(self) -> float:
        return (self.pcg64_dxsm() >> 11) * MAGIC_NUMBER
