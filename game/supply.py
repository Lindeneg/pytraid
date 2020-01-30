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
