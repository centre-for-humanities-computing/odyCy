import re
from pathlib import Path
from typing import Iterable
import unicodedata
import json

import spacy
from spacy.language import Language
from spacy.training.corpus import Corpus
from spacy.training.example import Example
from spacy.pipeline import Pipe
from spacy.tokens import Doc
from spacy.lookups import Lookups


def normalize_token(token: str) -> str:
    token = unicodedata.normalize("NFD", token)
    token = re.sub("[\u0300-\u036f]", "", token)
    return token


def normalize_doc(doc: Doc) -> Doc:
    for token in doc:
        token.lemma_ = normalize_token(token.lemma_)
    return doc


@Language.factory(
    "lemma_normalizer",
    assigns=["token.lemma"],
    default_score_weights={"lemma_acc": 1.0},
)
def make_normalizer(
    nlp: Language,
    name: str,
):
    return LemmaNormalizer(nlp=nlp, name=name)


class LemmaNormalizer(Pipe):
    """
    Removes greek diacritics from lemmas as they don't contain any semantic information.
    """

    def __init__(self, nlp: Language, name: str):
        self.name = name

    def __call__(self, doc: Doc) -> Doc:
        """Apply lemma normalization to document"""
        error_handler = self.get_error_handler()
        try:
            return normalize_doc(doc)
        except Exception as e:
            error_handler(self.name, self, [doc], e)


def normalize_examples(examples: Iterable[Example]) -> Iterable[Example]:
    for example in examples:
        example.reference = normalize_doc(example.reference)
        yield example


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


def base() -> Language:
    """Base model with all components enabled."""
    nlp = spacy.load("grc_dep_treebanks_trf")
    return nlp


def main() -> None:
    pipelines = {
        "lookup_only": only_lookup,
        "base": base,
        "trainable_only": only_trainable,
        "freq_only": only_freq,
    }
    results = {}
    for corpus_name in ["perseus", "proiel"]:
        print("----------------------")
        print(corpus_name.upper())
        print("----------------------\n")
        results[corpus_name] = {}
        for diacritics in ["with", "without"]:
            print(f"{diacritics} diacritics:")
            results[corpus_name][f"{diacritics}_diacritics"] = {}
            for name, create_nlp in pipelines.items():
                nlp = create_nlp()
                corpus = Corpus(f"corpus/{corpus_name}/test.spacy")
                examples = corpus(nlp)
                if diacritics == "without":
                    nlp.add_pipe("lemma_normalizer")
                    examples = normalize_examples(examples)
                examples = list(examples)
                scores = nlp.evaluate(examples)
                lemma_acc = scores["lemma_acc"]
                print(f" - {name}: {lemma_acc}")
                results[corpus_name][f"{diacritics}_diacritics"][name] = scores
    with open("metrics/lemmatizers.json", "w") as out_file:
        json.dump(results, out_file)
    print("DONE")


if __name__ == "__main__":
    main()
