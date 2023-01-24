import os
import json
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union, Iterable
from typing_extensions import TypedDict

import pandas as pd
from spacy.language import Language
from spacy.pipeline import Pipe
from spacy.pipeline.lemmatizer import lemmatizer_score
from spacy.util import ensure_path
from spacy.tokens import Doc, Token

MATCH_ORDER = [
    "upos",
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


class TableEntry(TypedDict):
    form: str
    lemma: str
    upos: str
    frequency: int
    Tense: str
    VerbForm: str
    Voice: str
    Case: str
    Gender: str
    Number: str
    Degree: str
    Mood: str
    Person: str
    Aspect: str
    Definite: str
    PronType: str
    Polarity: str
    Poss: str
    Reflex: str


@Language.factory(
    "frequency_lemmatizer",
    assigns=["token.lemma"],
    default_config={
        "overwrite": True,
        "fallback_priority": "lookup",
    },
    default_score_weights={"lemma_acc": 1.0},
)
def make_lemmatizer(
    nlp: Language,
    name: str,
    overwrite: bool,
    fallback_priority: Literal["lemma", "lookup"],
):
    return FrequencyLemmatizer(
        nlp=nlp,
        name=name,
        overwrite=overwrite,
        fallback_priority=fallback_priority,
    )  # type: ignore


def read_lookup(path: str) -> Dict[str, str]:
    with open(path) as file:
        obj = json.load(file)
        return obj


def read_table(path: str) -> List[TableEntry]:
    with open(path) as file:
        entries = [json.loads(line) for line in file]
        return entries


class FrequencyLemmatizer(Pipe):
    """
    Part-of-speech and morphology, and frequency
    sensitive rule-based lemmatizer.

    Parameters
    ----------
    overwrite: bool, default True
        Specifies whether the frequency lemmatizer should overwrite
        already assigned lemmas.
    fallback_priority: 'lemma' or 'lookup', default 'lookup'
        Specifies which fallback should have higher priority
            if the lemma is not found in
        the primary table.
    """

    def __init__(
        self,
        nlp: Language,
        name: str = "freq_lemmatizer",
        *,
        overwrite: bool = True,
        fallback_priority: Literal["lemma", "lookup"] = "lookup",
    ):
        self.name = name
        self.overwrite = overwrite
        self.scorer = lemmatizer_score
        self.fallback_priority = fallback_priority

    def initialize(
        self,
        get_examples=None,
        *,
        nlp=None,
        table: Optional[List[TableEntry]] = None,
        lookup: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initializes the frequency lemmatizer from given lemma table and lookup.

        Parameters
        ----------
        table: iterable of entries or None, default None
            Iterable of all entries in the lemma table
            with pos tags morph features and frequencies.
        lookup: dict of str to str or None, default None
            Backoff lookup table for simple token-lemma lookup.
        """
        if table is None:
            self.table = None
        else:
            self.table = pd.DataFrame.from_records(table)
        self.lookup = lookup

    def backoff(self, token: Token) -> str:
        """Gets backoff token based on priority."""
        orth = token.orth_.lower()
        lookup = self.lookup
        in_lookup = (lookup is not None) and (orth in lookup)
        priority = self.fallback_priority
        has_lemma = (token.lemma != 0) and (token.lemma_ != token.orth_)
        if in_lookup:
            if priority == "lookup":
                return lookup[orth]  # type: ignore
            else:
                if has_lemma:
                    return token.lemma_
                else:
                    return token.orth_
        else:
            if has_lemma:
                return token.lemma_
            else:
                return token.orth_

    def lemmatize(self, token: Token) -> str:
        """Lemmatizes token."""
        backoff = self.backoff(token)
        orth = token.orth_.lower()
        # If the table is empty we early return
        if self.table is None:
            return backoff
        # I make these so we can iterate through properties
        _token = {
            "form": orth,
            "upos": token.pos_,
            **token.morph.to_dict(),
        }
        # We try to match the token first
        match = self.table[self.table.form == _token["form"]]
        # If the token is not found we return the backoff lemma
        if not len(match.index):
            return backoff
        # We go through all properties in the matching order
        for match_property in MATCH_ORDER:
            match_column = match[match_property].fillna("")
            match_value = _token.get(match_property, "")
            match_new = match[match_column == match_value]
            # If the new property doesn't match we return the highest
            # frequency value from the previous match
            if not len(match_new.index):
                return match.loc[match.frequency.idxmax()].lemma
            match = match_new
        return match.loc[match.frequency.idxmax()].lemma

    def __call__(self, doc: Doc) -> Doc:
        """Apply the lemmatization to a document."""
        error_handler = self.get_error_handler()
        try:
            for token in doc:
                if self.overwrite or token.lemma == 0:
                    token.lemma_ = self.lemmatize(token)
            return doc
        except Exception as e:
            error_handler(self.name, self, [doc], e)

    def to_disk(
        self, path: Union[str, Path], *, exclude: Iterable[str] = tuple()
    ):
        """Save frequency lemmatizer data to a directory."""
        path = ensure_path(path)
        Path(path).mkdir(parents=True, exist_ok=True)
        config = dict(
            overwrite=self.overwrite, fallback_priority=self.fallback_priority
        )
        with open(os.path.join(path, "config.json"), "w") as config_file:
            json.dump(config, config_file)
        if self.table is not None:
            self.table.to_json(
                os.path.join(path, "table.jsonl"), orient="records", lines=True
            )
        if self.lookup is not None:
            with open(os.path.join(path, "lookup.json"), "w") as lookup_file:
                json.dump(self.lookup, lookup_file)

    def from_disk(
        self, path: Union[str, Path], *, exclude: Iterable[str] = tuple()
    ) -> "FrequencyLemmatizer":
        """Load component from disk."""
        path = ensure_path(path)
        config = read_lookup(os.path.join(path, "config.json"))
        self.overwrite = config.get("overwrite", self.overwrite)
        self.fallback_priority = config.get(
            "fallback_priority", self.fallback_priority
        )
        try:
            table: Optional[List[TableEntry]] = read_table(
                os.path.join(path, "table.jsonl")
            )
        except FileNotFoundError:
            table = None
        try:
            lookup: Optional[Dict[str, str]] = read_lookup(
                os.path.join(path, "lookup.json")
            )
        except FileNotFoundError:
            lookup = None
        self.initialize(table=table, lookup=lookup)
        return self
