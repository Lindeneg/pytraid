from math import sin, cos, sqrt, atan2, radians
from typing import TypeVar

City = TypeVar("City")


def DistanceBetween(c1: City, c2: City) -> int:
    p1: float
    p2: float
    g1: float
    g2: float
    R: int = 6371
    p1, g1 = c1.coordinates
    p2, g2 = c2.coordinates
    deltaPhi: float = abs(radians(p2) - radians(p1))
    deltaGamma: float = abs(radians(g2) - radians(g1))
    a: float = sin(deltaPhi / 2) ** 2 + cos(radians(p1)) * cos(radians(p2)) * sin(deltaGamma / 2) ** 2
    c: float = 2 * atan2(sqrt(abs(a)), sqrt(abs(1 - a)))
    return int(R * c)
