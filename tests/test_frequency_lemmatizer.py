"""Tests frequency lemmatizer"""
import spacy
from custom_components.lemmatizer import FrequencyTable


def test_freq_lemmatizer():
    nlp = spacy.blank("ru")
    freq_lemmatizer = nlp.add_pipe(
        "frequency_lemmatizer",
        config=dict(overwrite=True, fallback_priority="lookup"),
    )
    table: FrequencyTable = {
        "белки": [
            {
                "form": "белки",
                "lemma": "белка",
                "frequency": 2000,
                "upos": "NOUN",
            },
            {
                "form": "белки",
                "lemma": "белок",
                "frequency": 1000,
                "upos": "NOUN",
            },
        ]
    }
    lookup = {"медведи": "медведь"}
    freq_lemmatizer.initialize(
        get_examples=None, table=table, lookup=lookup  # type: ignore
    )
    doc = nlp("белки и медведи")
    assert doc[0].lemma_ == "белка"
    assert doc[1].lemma_ == "и"
    assert doc[2].lemma_ == "медведь"
