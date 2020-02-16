"""
Author : Christian Lindeneg
         https://github.com/Lindeneg
Contact: christian@lindeneg.org
Licence: Public Domain
"""

import json
import pickle
from typing import Dict, List, Union, TypeVar, Optional


ReadType = Dict[str, List[Dict[str, Union[int, float, str, List[str]]]]]

# TODO Generalise ReadJSON


def ReadJSON(path) -> Union[ReadType, None]:
    with open(path, "r") as mFile:
        mData: Optional[ReadType] = json.load(mFile)
        mFile.close()
    return mData





