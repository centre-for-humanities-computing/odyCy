from typing import Optional, List, TypedDict, Literal, Dict

import pandas as pd

from spacy.language import Language
from spacy.pipeline import Pipe
from spacy.tokens import Token
from spacy.tokens import Doc
from spacy.pipeline.lemmatizer import lemmatizer_score

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
    },
    default_score_weights={"lemma_acc": 1.0},
)
def make_lemmatizer(
    nlp: Language,
    name: str,
    overwrite: bool,
):
    return FrequencyLemmatizer(
        nlp=nlp,
        name=name,
        overwrite=overwrite,
    )  # type: ignore


class FrequencyLemmatizer(Pipe):
    """
    Part-of-speech and morphology, and frequency
    sensitive rule-based lemmatizer.
    """

    def __init__(
        self,
        nlp: Language,
        name: str = "freq_lemmatizer",
        *,
        overwrite: bool = True,
    ):
        self.name = name
        self.overwrite = overwrite
        self.scorer = lemmatizer_score

    def initialize(
        self,
        get_examples=None,
        *,
        nlp=None,
        table: Optional[List[TableEntry]],
        backoff_lookup: Optional[Dict[str, str]],
    ) -> None:
        if table is None:
            self.table = None
        else:
            self.table = pd.DataFrame.from_records(table)
        self.backoff_lookup = backoff_lookup

    def lemmatize(self, token: Token) -> str:
        """Lemmatizes token."""
        orth = token.orth_.lower()
        lookup = self.backoff_lookup
        # If lookup tabvle exists and it has the token, we use it as backoff
        if lookup is not None and orth in lookup:
            backoff = lookup[orth]
        # else if the token already has a lemma we assign it as backoff
        elif token.lemma != 0:
            backoff = token.lemma_
        else:
            # Otherwise the verbatim form will be the backoff
            backoff = token.orth_
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
