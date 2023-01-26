import os
import json
from typing import Dict, List

import spacy
from spacy.tokens import DocBin


NER_DIR = "corpus/ner"


def read_jsonl(path) -> Dict:
    with open(path) as fin:
        fold = [json.loads(line) for line in fin]
    return fold


def binarize_json(gold_dict, model=None) -> DocBin:

    if model:
        nlp = spacy.load(model)
    else:
        nlp = spacy.blank("grc")

    db = DocBin()
    for entry in gold_dict:
        doc = nlp.make_doc(entry['text'])
        ents = []
        for start, end, label in entry["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                print(entry)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    return db


def main():
    for fold_name in ['train', 'dev', 'test']:
        fold = read_jsonl(os.path.join(NER_DIR, fold_name + '.jsonl'))
        db = binarize_json(fold, model='grc_dep_treebanks_trf')
        db.to_disk(os.path.join(NER_DIR, fold_name + '.spacy'))


if __name__ == "__main__":
    main()