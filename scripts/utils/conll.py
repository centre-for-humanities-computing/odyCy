from typing import Dict
from io import StringIO
import json

import pandas as pd

# Columns in a CONLL-U file
CONLL_COLUMNS = [
    "word_id",
    "form",
    "lemma",
    "upos",
    "xpos",
    "feats",
    "head",
    "deprel",
    "deps",
    "misc",
]

# Possible morphological features
POSSIBLE_FEATURES = [
    "Tense",
    "VerbForm",
    "Voice",
    "Case",
    "Gender",
    "Number",
    "Degree",
    "Mood",
    "Person",
    "Aspect",
    "Definite",
    "PronType",
    "Polarity",
    "Poss",
    "Reflex",
]


def load_conllu(path: str) -> pd.DataFrame:
    """Reads a CONLL-U file into a Dataframe"""
    with open(path) as conllu_file:
        lines = []
        # I only append lines from the file that are not comments.
        for line in conllu_file:
            if not line.startswith("#"):
                lines.append(line)
    # Joining the lines
    conllu_text = "".join(lines)
    # Turning it into a stream so that pandas can read it as a file.
    text_stream = StringIO(conllu_text)
    # Reading conllu files to a dataframe
    df = pd.read_csv(text_stream, sep="\t", names=CONLL_COLUMNS)
    return df


def features_to_dict(feature_string: str) -> Dict[str, str]:
    """Converts a string of morphological features to a
    dictionary."""
    features = dict()
    if feature_string == "_":
        return features
    declarations = feature_string.split("|")
    for declaration in declarations:
        feature, value = declaration.split("=")
        features[str(feature)] = str(value)
    return features
