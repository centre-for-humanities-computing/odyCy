import json
from typing import List, Iterable, Dict, Sequence
from io import StringIO
import os
from pathlib import Path
from typing_extensions import TypedDict
import spacy
from spacy.tokens import Doc
import pandas as pd
from tqdm import trange

CONLLU_FIELDS = [
    "ID",
    "FORM",
    "LEMMA",
    "UPOS",
    "XPOS",
    "FEATS",
    "HEAD",
    "DEPREL",
    "DEPS",
    "MISC",
]


class ConlluEntry(TypedDict):
    """Entry in CONLL-U files"""

    ID: str
    FORM: str
    LEMMA: str
    UPOS: str
    XPOS: str
    FEATS: str
    HEAD: str
    DEPREL: str
    DEPS: str
    MISC: str


def read_conllu_df(path: str) -> pd.DataFrame:
    """Reads a CONLL-U file into a Dataframe"""
    with open(path) as conllu_file:
        lines = []
        # I only append lines from the file that are not comments.
        for line in conllu_file:
            if not line.startswith("#") and line.strip():
                lines.append(line)
    # Joining the lines
    conllu_text = "".join(lines)
    # Turning it into a stream so that pandas can read it as a file.
    text_stream = StringIO(conllu_text)
    # Reading conllu files to a dataframe
    df = pd.read_csv(text_stream, sep="\t", names=CONLLU_FIELDS)
    return df


def is_sentence_end(i_entry: int, entries: Sequence[ConlluEntry]) -> bool:
    """Determines whether the given entry is the end of a sentence."""
    n_entries = len(entries)
    return (i_entry < (n_entries - 1)) and (
        int(entries[i_entry]["ID"]) > int(entries[i_entry + 1]["ID"])
    )


def to_conllu_text(
    entries: Sequence[ConlluEntry], separate_lines: bool = True
) -> str:
    """Turns a sequence of entries to a CONLL-U compliant string."""
    n_entries = len(entries)
    lines: List[str] = []
    for i_entry in range(n_entries):
        current = entries[i_entry]
        # Joining fields together with a tab
        line = "\t".join(str(current[field]) for field in CONLLU_FIELDS)
        lines.append(line)
        # Adding empty line if sentence ends
        if is_sentence_end(i_entry, entries=entries) and separate_lines:
            lines.append("")
    # Joining lines together with line break
    text = "\n".join(lines)
    return text


def df_to_entries(df: pd.DataFrame) -> List[ConlluEntry]:
    """Turns data frame to a list of conllu entries."""
    # Selecting important rows in the proper order
    df = df[CONLLU_FIELDS]
    entries: List[ConlluEntry] = []
    for index, row in df.iterrows():
        entry: ConlluEntry = row.to_dict()  # type:ignore
        entries.append(entry)
    return entries


def write_conllu(
    entries: Sequence[ConlluEntry], path: str, separate_lines: bool = True
) -> None:
    """Writes entries to a conllu file."""
    if not path.endswith(".conllu"):
        raise ValueError(
            f"Path: {path}, is not the right format, file extension has to be conllu"
        )
    # Making sure directory exists
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    text = to_conllu_text(entries, separate_lines=separate_lines)
    with open(path, "w") as out_file:
        out_file.write(text)


def write_conllu_df(
    df: pd.DataFrame, path: str, separate_lines: bool = True
) -> None:
    """Writes dataframe with entries to a conllu file."""
    entries = df_to_entries(df)
    write_conllu(entries, path, separate_lines=separate_lines)


def get_gold_data() -> pd.DataFrame:
    """Reads concatenates and returns all gold standard data."""
    gold_dfs = []
    for corpus in ["proiel", "perseus"]:
        for split in ["test", "dev", "train"]:
            gold_dfs.append(
                read_conllu_df(f"assets/treebanks/{corpus}/{split}.conllu")
            )
    gold = pd.concat(gold_dfs)
    return gold


def get_sentences(df: pd.DataFrame) -> List[List[ConlluEntry]]:
    """Converts a conllu dataframe to a list of sentences."""
    entries = df_to_entries(df)
    sents = []
    sent = []
    for i_entry in range(len(entries)):
        sent.append(entries[i_entry])
        if is_sentence_end(i_entry=i_entry, entries=entries):
            sents.append(sent)
            sent = []
    sents.append(sent)
    return sents


def highlight_mismatch(row):
    """Highlights mismatches in lemmas in a sentence."""
    if row.gold != row.pred:
        bg_color = "red"
        color = "white"
    else:
        bg_color = "white"
        color = "black"
    return [f"background-color: {bg_color}; color: {color}" for _ in row]


def serialize_sentence(
    gold_tokens: List[ConlluEntry], pred_tokens: Doc
) -> Dict:
    sentence_text = " ".join(token["FORM"] for token in gold_tokens)
    return {
        "text": sentence_text,
        "gold_lemmas": [token["LEMMA"].lower() for token in gold_tokens],
        "gold_pos": [token["UPOS"] for token in gold_tokens],
        "pred_lemmas": [token.lemma_.lower() for token in pred_tokens],
        "pred_pos": [token.pos_ for token in pred_tokens],
    }


def main() -> None:
    Path("error_analysis").mkdir(parents=True, exist_ok=True)
    # Loading pipeline
    nlp = spacy.load("grc_dep_treebanks_trf")
    # Loading data
    print("Loading all data.")
    gold = get_gold_data()
    gold_sentences = get_sentences(gold)
    n_sents = len(gold_sentences)
    print("Finding mismatching sentences and producing markdown data.")
    with open("error_analysis/lemmas.jsonl", "w") as out_file:
        for i_sent in trange(n_sents):
            # Extracting lemmas and pos tags
            gold_sentence = gold_sentences[i_sent]
            sentence_text = " ".join(token["FORM"] for token in gold_sentence)
            pred_sentence = nlp(sentence_text)
            sentence = serialize_sentence(
                gold_tokens=gold_sentence, pred_tokens=pred_sentence
            )
            # Where lemmas don't match we pretty print the errors
            if sentence["pred_lemmas"] != sentence["gold_lemmas"]:
                sentence_json = json.dumps(sentence)
                out_file.write(f"{sentence_json}\n")
    print("DONE")


if __name__ == "__main__":
    main()
