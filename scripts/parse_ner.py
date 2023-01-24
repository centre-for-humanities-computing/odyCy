from typing import List, Optional, Literal
from typing_extensions import NamedTuple, TypedDict
import json

from lxml import etree

TAGGED_WORKS = [
    "assets/pretraining/raw/perseus/tlg0008/tlg001/tlg0008.tlg001.perseus-grc4.xml",
    "assets/pretraining/raw/perseus/tlg0059/tlg004/tlg0059.tlg004.perseus-grc2.xml",
    "assets/pretraining/raw/perseus/tlg4036/tlg023/tlg4036.tlg023.cypria-grc1.xml",
    # "assets/pretraining/raw/perseus/tlg0653/tlg001/tlg0653.tlg001.perseus-grc1.xml",
]

OUT_PATH = "assets/named_entities/gold_standard.jsonl"

Tag = Literal["PLACE", "PERSON", "GROUP"]


class Entity(NamedTuple):
    start: int
    end: int
    tag: Tag


class GoldDict(TypedDict):
    text: str
    entities: List[Entity]


def get_local_name(tag: str) -> str:
    """Gets local name of XML tag."""
    return tag.split("}")[-1]


def get_tag(element) -> Optional[Tag]:
    """Returns the tag for a given element if it has one."""
    local_name = get_local_name(element.tag)
    if local_name == "placeName":
        return "PLACE"
    if local_name == "persName":
        return "PERSON"
    if local_name == "name":
        name_type = element.get("type")
        if name_type == "place":
            return "PLACE"
        if name_type == "person":
            return "PERSON"
        if (name_type == "group") or (name_type == "ethnic"):
            return "GROUP"
    return None


def parse_ner_recursive(
    texts: List[str], tags: List[Optional[str]], element
) -> None:
    """Parser the element tree recursively and adds element texts
    and named entity tags to the given lists.
    """
    if element.tag != "note":
        tag = get_tag(element)
        if element.text:
            texts.append(element.text)
            tags.append(tag)
        for child in element:
            parse_ner_recursive(texts, tags, element=child)
            if child.tail:
                texts.append(child.tail)
                tags.append(tag)


def parse_ner(root_element) -> GoldDict:
    """Parses TEI XML tree from root element into a gold dictionary."""
    contents = []
    tags = []
    parse_ner_recursive(contents, tags, element=root_element)
    text = ""
    entities: List[Entity] = []
    for content, tag in zip(contents, tags):
        text += " "
        start_index = len(text)
        text += content
        end_index = len(text)
        if tag is not None:
            entities.append(Entity(start=start_index, end=end_index, tag=tag))
    return GoldDict(text=text, entities=entities)


def write_jsonl(gold_dicts: List[GoldDict], path: str) -> None:
    """Writes gold standard data to disk in JSONL format."""
    with open(path, "w") as out_file:
        for gold_dict in gold_dicts:
            json_data = json.dumps(gold_dict)
            out_file.write(f"{json_data}\n")


def main() -> None:
    gold_dicts: List[GoldDict] = []
    for path in TAGGED_WORKS:
        tree = etree.parse(path)
        body = tree.xpath("//*[local-name()='body']")[0]
        gold_dicts.append(parse_ner(root_element=body))
    write_jsonl(gold_dicts, path=OUT_PATH)


if __name__ == "__main__":
    main()
