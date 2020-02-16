"""
Author : Christian Lindeneg
         https://github.com/Lindeneg
Contact: christian@lindeneg.org
Licence: Public Domain
"""

from json import load as jLoad
from pickle import load as pLoad
from pickle import dump as pDump
from typing import Dict, List, Tuple, Union, TypeVar, Callable, TextIO, Optional

Game = TypeVar("Game")
FileType = Dict[str, Union[List[Dict[str, Union[int, float, str, List[str]]]], Game]]


def FileManager(args: Tuple[str, str], data: Optional[Game] = None) -> Optional[FileType]:
    path: str
    name: str
    flag: str
    method: Callable
    mData: Optional[Game] = None
    GetMethod: Callable = lambda yData, yName: ["r", jLoad] if name[-4:].lower() == "json" \
        else (["wb", pDump] if yData else ["rb", pLoad])
    path, name = args
    flag, method = GetMethod(data, name)
    mFile: TextIO
    try:
        with open(f"{path}/{name}", flag) as mFile:
            if data:
                method(data, mFile)
            else:
                mData = method(mFile)
            mFile.close()
    except FileNotFoundError:
        pass  # Returns None
    return mData
