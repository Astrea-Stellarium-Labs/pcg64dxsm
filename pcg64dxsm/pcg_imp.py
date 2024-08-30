import typing
from random import Random

from .pcg_core import InternalPCG

__all__ = (
    "PCG64DXSM",
    "seed",
    "random",
    "uniform",
    "triangular",
    "randint",
    "choice",
    "randrange",
    "sample",
    "shuffle",
    "choices",
    "normalvariate",
    "lognormvariate",
    "expovariate",
    "vonmisesvariate",
    "gammavariate",
    "gauss",
    "betavariate",
    "paretovariate",
    "weibullvariate",
    "getrandbits",
)

SEED_TYPE = typing.Union[int, float, str, bytes, bytearray, None]


class PCG64DXSM(Random):
    """
    The PCG64DXSM class implements the PCG64DXSM algorithm for generating random numbers.

    Since the class is a subclass of random.Random, it can be used in the same way as the built-in random module.
    """

    def __init__(self, x: SEED_TYPE = None) -> None:
        """
        Initialize the PCG64DXSM instance.

        Args:
            x: An optional seed value. If x is None, the instance will be initialized with a random seed. \
            If x is a bytes, bytearray, or str, then care must be taken to ensure that the seed is at least 32 bytes long.
        """
        self._internal_state: InternalPCG = None
        super().__init__(x)

    def seed(self, a: SEED_TYPE = None, version: int = 1) -> None:
        """
        Initializes and seeds the PCG64DXSM instance.

        Args:
            x: An optional seed value. If x is None, the instance will be initialized with a random seed. \
            If x is a bytes, bytearray, or str, then care must be taken to ensure that the seed is at least 32 bytes long.
        """
        if a is None:
            self._internal_state = InternalPCG.from_entropy()
        elif isinstance(a, int):
            self._internal_state = InternalPCG.from_seed(
                a.to_bytes(32, byteorder="little")
            )
        elif isinstance(a, float):
            self._internal_state = InternalPCG.from_seed(
                int(a).to_bytes(32, byteorder="little")
            )
        elif isinstance(a, str):
            self._internal_state = InternalPCG.from_seed(a.encode())
        elif isinstance(a, (bytes, bytearray)):
            self._internal_state = InternalPCG.from_seed(a)
        else:
            raise TypeError(
                "seed() only accepts int, float, str, bytes, or bytearray, not"
                f" {type(a).__name__}"
            )

    def getstate(self) -> typing.Type[NotImplementedError]:
        """getstate is not implemented for PCG64DXSM."""
        return NotImplementedError

    def setstate(
        self, state: typing.Tuple[typing.Any, ...]
    ) -> typing.Type[NotImplementedError]:
        """setstate is not implemented for PCG64DXSM."""
        return NotImplementedError

    def random(self) -> float:
        """Return a random float in the range [0.0, 1.0)."""
        return self._internal_state.random()


_inst = PCG64DXSM()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
choices = _inst.choices
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getrandbits = _inst.getrandbits
