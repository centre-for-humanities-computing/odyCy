import os
import json
from typing import List, TypedDict, Literal, Iterable, Dict

import pandas as pd

SRC_DIR = "assets/named_entities"
DEST_PATH = "assets/named_entities/patterns.jsonl"


class Pattern(TypedDict):
    label: str
    pattern: str


Label = Literal["LOCATION", "PERSON", "ETHNICITY"]


def create_patterns(tokens: List[str], label: Label) -> Iterable[Pattern]:
    """Creates generator of patterns for the given tokens and label."""
    for token in tokens:
        pattern: Pattern = {"label": label, "pattern": token}
        yield pattern


def get_personal_names(src_dir: str) -> List[str]:
    """Reads personal names from disk."""
    src_path = os.path.join(src_dir, "personal_names.txt")
    with open(src_path) as src_file:
        src_text = src_file.read()
        personal_names = src_text.split()
    return personal_names


def get_greek_loc_data(src_dir: str) -> pd.DataFrame:
    """Reads locality and ethnicity data from disk and filters for greek."""
    src_path = os.path.join(src_dir, "place_names.csv")
    loc_data = pd.read_csv(src_path)
    # Selecting greek entries
    greek_loc_data = loc_data[loc_data.language_tag == "grc"]
    # Removing entries that don't have an attested form (greek form)
    greek_loc_data = greek_loc_data.dropna(subset=["attested_form"])
    # Removing duplicates from attested form, where name_type matches
    greek_loc_data = greek_loc_data.drop_duplicates(
        subset=["attested_form", "name_type"]
    )
    return greek_loc_data


def get_place_names(loc_data: pd.DataFrame) -> List[str]:
    """Extracts place names from the location dataset."""
    return loc_data.attested_form[loc_data.name_type == "geographic"].tolist()


def get_ethnic_names(loc_data: pd.DataFrame) -> List[str]:
    """Extracts ethnic names from the location dataset."""
    return loc_data.attested_form[loc_data.name_type == "ethnic"].tolist()


def main():
    personal_names = get_personal_names(src_dir=SRC_DIR)
    loc_data = get_greek_loc_data(src_dir=SRC_DIR)
    place_names = get_place_names(loc_data)
    ethnic_names = get_ethnic_names(loc_data)
    labeled_names: Dict[Label, List[str]] = {
        "PERSON": personal_names,
        "LOCATION": place_names,
        "ETHNICITY": ethnic_names,
    }
    with open(DEST_PATH, "w") as dest_file:
        for label, names in labeled_names.items():
            patterns = create_patterns(names, label)
            # Converting each pattern to json
            json_patterns = map(json.dumps, patterns)
            # Writing each json entries to a line
            for line in json_patterns:
                dest_file.write(line + "\n")


if __name__ == "__main__":
    main()
