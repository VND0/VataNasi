import hashlib
from typing import NamedTuple


class TaskPathData(NamedTuple):
    instant_check: bool
    words_amount: int
    categories: list[str]


def passd_to_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()
