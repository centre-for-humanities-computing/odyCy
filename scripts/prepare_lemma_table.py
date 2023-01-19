"""Creates a table of lemmas with form, upos, morhpology and
frequency for our custom lemmatizer."""

from io import StringIO

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

TREEBANKS_PATH = "assets/treebanks/joint/train.conllu"
LEMMA_TABLE_PATH = "assets/lemmas/lemma_table.jsonl"


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


def main() -> None:
    # Loading treebanks
    treebanks = load_conllu(TREEBANKS_PATH)
    # Lowercasing forms and lemmata
    treebanks["lemma"] = treebanks.lemma.str.lower()
    treebanks["form"] = treebanks.form.str.lower()
    # Creating unique groups with frequencies
    lemma_table = (
        treebanks.groupby(["form", "lemma", "upos", "feats"])
        .count()
        .word_id.rename("frequency")
        .reset_index()
    )
    # Exporting as JSON lines
    lemma_table.to_json(LEMMA_TABLE_PATH, orient="records", lines=True)


if __name__ == "__main__":
    main()
