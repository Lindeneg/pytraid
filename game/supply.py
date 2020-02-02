from __future__ import annotations
from util.constants import SUPPLY, DEMAND


class Supply:
    def __init__(
            self,
            name: str,
            value: int,
            weight: int,
            typeof: str
    ) -> None:
        self.__name: str = name
        self.__value: int = value
        self.__weight: int = weight
        self.__typeof: str = typeof

    @property
    def name(self) -> str:
        return self.__name.replace("_", " ")

    @property
    def value(self) -> int:
        return self.__value

    @property
    def weight(self) -> int:
        return self.__weight

    @property
    def typeof(self) -> str:
        return self.__typeof

    def __eq__(self, otherSupply: Supply) -> bool:
        return self.name == otherSupply.name

    def __repr__(self) -> str:
        return f"[ {self.name.upper()}, {self.value}G, {self.weight}T ]  "
