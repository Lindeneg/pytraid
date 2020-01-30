import json
import pickle
from typing import Dict, List, Union, TypeVar, Optional


ReadType = Dict[str, List[Dict[str, Union[int, float, str, List[str]]]]]

# TODO Generalise ReadJSON


def ReadJSON(path) -> Union[ReadType, None]:
    mData: Optional[ReadType] = None
    with open(path, "r") as mFile:
        mData = json.load(mFile)
        mFile.close()
    return mData





