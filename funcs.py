import hashlib
from typing import NamedTuple


class TaskPathData(NamedTuple):
    instant_check: bool
    words_amount: int
    categories: list[str]


def passd_to_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def parse_task1_args(args) -> TaskPathData:
    instant_check = bool(int(args["ic"]))
    words_amount = int(args["amount"])
    categories = args.getlist("cat")

    if instant_check:
        raise NotImplementedError
    if words_amount < 0:
        raise ValueError
    if not categories:
        raise ValueError

    return TaskPathData(instant_check, words_amount, categories)
