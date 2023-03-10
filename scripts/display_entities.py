"""Displays parsed entities in textual context with colors :)))"""
from typing import List, Dict
import json

import colorama

from parse_ner import GoldDict, Tag

OUT_PATH = "assets/named_entities/gold_standard.jsonl"


TAG_COLOR: Dict[Tag, str] = {
    "PLACE": colorama.Fore.GREEN,
    "PERSON": colorama.Fore.MAGENTA,
    "GROUP": colorama.Fore.BLUE,
}


def print_entities(gold_dict: GoldDict) -> None:
    """Pretty prints colored entities."""
    text = gold_dict["text"]
    entities = gold_dict["entities"]
    last_end = 0
    for entity in entities:
        start, end, tag = entity
        print(text[last_end:start], end="")
        print(TAG_COLOR[tag], end="")
        print(text[start:end], end="")
        print(colorama.Style.RESET_ALL, end="")
        last_end = end
    print(text[last_end:])


def main() -> None:
    colorama.init()
    print("\n")
    print("Color glossary:", end=" ")
    for tag, color in TAG_COLOR.items():
        print(color + tag + colorama.Style.RESET_ALL, end=" ")
    print("\n")
    with open(OUT_PATH) as file:
        gold_dicts: List[GoldDict] = [json.loads(line) for line in file]
    for i, gold_dict in enumerate(gold_dicts):
        print("\n")
        print("================================")
        print(f"        Section {i}")
        print("================================")
        print_entities(gold_dict)
        input("Press enter to go to next section...")


if __name__ == "__main__":
    main()
