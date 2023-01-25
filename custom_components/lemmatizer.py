import os
import json
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union, Iterable
from typing_extensions import TypedDict, NotRequired

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
    Tense: NotRequired[str]
    VerbForm: NotRequired[str]
    Voice: NotRequired[str]
    Case: NotRequired[str]
    Gender: NotRequired[str]
    Number: NotRequired[str]
    Degree: NotRequired[str]
    Mood: NotRequired[str]
    Person: NotRequired[str]
    Aspect: NotRequired[str]
    Definite: NotRequired[str]
    PronType: NotRequired[str]
    Polarity: NotRequired[str]
    Poss: NotRequired[str]
    Reflex: NotRequired[str]


FrequencyTable = Dict[str, List[TableEntry]]

LookupTable = Dict[str, str]


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


def max_freq_lemma(entries: List[TableEntry]) -> str:
    """Returns lemma with highest frequency from the given entries."""
    max_index = 0
    n_entries = len(entries)
    for index in range(1, n_entries):
        if entries[index]["frequency"] > entries[max_index]["frequency"]:
            max_index = index
    return entries[max_index]["lemma"]


def match_lemma(
    token_entry: TableEntry, table: FrequencyTable
) -> Optional[str]:
    """Returns a lemma for a token if it
    can be found in the frequency table.
    """
    # Tries to find the entries associated with the token in the table
    match = table.get(token_entry["form"], [])
    if not match:
        return None
    # We go through all the properties to be matched
    for match_property in MATCH_ORDER:
        match_new = [
            entry
            for entry in match
            if entry.get(match_property, "")
            == token_entry.get(match_property, "")
        ]
        if not match_new:
            return max_freq_lemma(entries=match)
        match = match_new
    return max_freq_lemma(entries=match)


def read_json(path: str) -> Dict:
    with open(path) as file:
        res = json.load(file)
    return res


def write_json(object: Dict, path: str) -> None:
    with open(path, "w") as file:
        json.dump(object, file)


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
        table: Optional[FrequencyTable] = None,
        lookup: Optional[LookupTable] = None,
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
            self.table = table
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
        # I only add frequency for type compatibility
        token_entry: TableEntry = TableEntry(
            form=orth, upos=token.pos_, frequency=-1, **token.morph.to_dict()
        )
        lemma = match_lemma(token_entry=token_entry, table=self.table)
        if lemma is None:
            return backoff
        else:
            return lemma

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
            table_path = os.path.join(path, "table.json")
            write_json(self.table, path=table_path)
        if self.lookup is not None:
            lookup_path = os.path.join(path, "lookup.json")
            write_json(self.lookup, path=lookup_path)

    def from_disk(
        self, path: Union[str, Path], *, exclude: Iterable[str] = tuple()
    ) -> "FrequencyLemmatizer":
        """Load component from disk."""
        path = ensure_path(path)
        config = read_json(os.path.join(path, "config.json"))
        self.overwrite = config.get("overwrite", self.overwrite)
        self.fallback_priority = config.get(
            "fallback_priority", self.fallback_priority
        )
        try:
            table: Optional[FrequencyTable] = read_json(
                os.path.join(path, "table.json")
            )
        except FileNotFoundError:
            table = None
        try:
            lookup: Optional[LookupTable] = read_json(
                os.path.join(path, "lookup.json")
            )
        except FileNotFoundError:
            lookup = None
        self.initialize(table=table, lookup=lookup)
        return self
