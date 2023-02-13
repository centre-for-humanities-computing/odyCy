"""Script that produces different versions of 
homercy with different lemmatizer components.
"""
import os
import json
from pathlib import Path
import spacy
from spacy.language import Language
from spacy.lookups import Lookups

MODELS_PATH = "models/lemmatizer_effect"


def only_lookup() -> Language:
    """Model with only a lookup table."""
    nlp = spacy.load("grc_dep_treebanks_trf")
    nlp.remove_pipe("frequency_lemmatizer")
    nlp.remove_pipe("trainable_lemmatizer")
    lemmatizer = nlp.add_pipe("lemmatizer", config={"mode": "lookup"})
    lookups = Lookups()
    with open("assets/lemmas/lemma_lookup.json") as lookup_file:
        lookups.add_table("lemma_lookup", json.load(lookup_file))
    lemmatizer.initialize(nlp=nlp, lookups=lookups)
    return nlp


def only_trainable() -> Language:
    """Model with only a trainable lemmatizer."""
    nlp = spacy.load("grc_dep_treebanks_trf")
    nlp.remove_pipe("frequency_lemmatizer")
    return nlp


def only_freq() -> Language:
    """Model with only a frequency lemmatizer."""
    nlp = spacy.load("grc_dep_treebanks_trf")
    nlp.remove_pipe("trainable_lemmatizer")
    return nlp


def main() -> None:
    Path(MODELS_PATH).mkdir(exist_ok=True, parents=True)
    only_freq().to_disk(os.path.join(MODELS_PATH, "only_freq"))
    only_trainable().to_disk(os.path.join(MODELS_PATH, "only_trainable"))
    only_lookup().to_disk(os.path.join(MODELS_PATH, "only_lookup"))


if __name__ == "__main__":
    main()
