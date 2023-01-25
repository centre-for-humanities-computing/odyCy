"""Creates a table of lemmas with form, upos, morhpology and
frequency for our custom lemmatizer."""

import json

from utils.conll import features_to_dict, load_conllu, POSSIBLE_FEATURES

TREEBANKS_PATH = "assets/treebanks/joint/train.conllu"
LEMMA_TABLE_PATH = "assets/lemmas/lemma_table.json"


def main() -> None:
    # Loading treebanks
    treebanks = load_conllu(TREEBANKS_PATH)
    # Lowercasing forms and lemmata
    treebanks["lemma"] = treebanks.lemma.str.lower()
    treebanks["form"] = treebanks.form.str.lower()
    # Creating unique groups with frequencies
    lemma_df = (
        treebanks.groupby(["form", "lemma", "upos", "feats"])
        .count()
        .word_id.rename("frequency")
        .reset_index()
    )
    lemma_df["feats"] = lemma_df.feats.map(features_to_dict)
    for feature in POSSIBLE_FEATURES:
        lemma_df[feature] = lemma_df.feats.map(
            lambda feats: feats.get(feature, "")
        )
    lemma_df = lemma_df.drop(columns="feats")
    # Converting to hashtable with list of records
    lemma_table = {
        form: entries.to_dict(orient="records")
        for form, entries in lemma_df.groupby("form")
    }
    # Exporting as JSON
    with open(LEMMA_TABLE_PATH, "w") as out_file:
        json.dump(lemma_table, out_file)


if __name__ == "__main__":
    main()
