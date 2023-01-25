"""Splits NER data into train, dev and test set."""
import json
from typing import List, Tuple, TypeVar
import os

import numpy as np
from parse_ner import OUT_PATH, GoldDict, write_jsonl
from typing_extensions import NamedTuple


class SplitRatio(NamedTuple):
    train: int
    dev: int
    test: int


SPLIT_SEED = 69  # Very mature random seed
SPLIT_RATIO = SplitRatio(8, 1, 1)
OUT_DIR = "corpus/ner/"

T = TypeVar("T")


def shuffle(data: List[T], seed: int) -> List[T]:
    """Shuffles list randomly according to seed."""
    generator = np.random.default_rng(seed=seed)
    data_array = np.array(data)
    generator.shuffle(data_array)
    return data_array.tolist()


def split(
    data: List[T], split_ratio: SplitRatio, seed: int
) -> Tuple[List[T], List[T], List[T]]:
    """Splits data set into train dev and test sets."""
    data = shuffle(data, seed=seed)
    fraction = len(data) / sum(split_ratio)
    train_end_index = split_ratio.train * fraction
    train_end_index = int(train_end_index)
    dev_end_index = train_end_index + split_ratio.dev * fraction
    dev_end_index = int(dev_end_index)
    return (
        data[:train_end_index],
        data[train_end_index:dev_end_index],
        data[dev_end_index:],
    )


def main() -> None:
    with open(OUT_PATH) as file:
        gold_dicts: List[GoldDict] = [json.loads(line) for line in file]
    train, dev, test = split(
        gold_dicts, split_ratio=SPLIT_RATIO, seed=SPLIT_SEED
    )
    for name, set in zip(["train", "dev", "test"], [train, dev, test]):
        write_jsonl(set, path=os.path.join(OUT_DIR, f"{name}.jsonl"))


if __name__ == "__main__":
    main()
