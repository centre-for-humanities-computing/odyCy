# Sourcing preprocessing env
source environments/preprocessing/bin/activate
# Renaming perseus and proiel treebank files
# Perseus
mv assets/treebanks/perseus/grc_perseus-ud-dev.conllu assets/treebanks/perseus/dev.conllu
mv assets/treebanks/perseus/grc_perseus-ud-train.conllu assets/treebanks/perseus/train.conllu
mv assets/treebanks/perseus/grc_perseus-ud-test.conllu assets/treebanks/perseus/test.conllu
# Proiel
mv assets/treebanks/proiel/grc_proiel-ud-dev.conllu assets/treebanks/proiel/dev.conllu
mv assets/treebanks/proiel/grc_proiel-ud-train.conllu assets/treebanks/proiel/train.conllu
mv assets/treebanks/proiel/grc_proiel-ud-test.conllu assets/treebanks/proiel/test.conllu
# Joining treebank files
python3 scripts/join_treebanks.py
# Converting named entities to spaCy patterns
python3 scripts/prepare_named_entities.py
# Parses pretraining corpus to text
python3 scripts/parse_pretraining_corpus.py
# Converting treebank data to spaCy binraries
for CORPUS in "joint" "perseus" "proiel"
do
    mkdir -p corpus/$CORPUS
    for SET in "train" "dev" "test"
    do
        python3 -m spacy convert assets/treebanks/$CORPUS/$SET.conllu corpus/$CORPUS/ --converter conllu -n 10 
    done
done
# Creating lemma table
python3 scripts/prepare_lemma_table.py
# Parsing named entities from Perseus
python3 scripts/parse_ner.py
# Split named entities and prepare them for training
mkdir -p corpus/ner
python3 scripts/split_ner.py

# binarize NER
echo "Binarizing NER training data using grc_dep_treebanks_trf"
deactivate
source environments/training/bin/activate
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl
python3 scripts/binarize_ner.py