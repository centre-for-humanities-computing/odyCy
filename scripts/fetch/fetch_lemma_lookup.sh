rm -rf assets/lemmas
mkdir -p assets/lemmas
cd assets/lemmas

# Fetching lookups from repo
git clone "https://github.com/explosion/spacy-lookups-data.git"

# Moving the lookup table to top level
mv spacy-lookups-data/spacy_lookups_data/data/grc_lemma_lookup.json lemma_lookup.json

# Cleanup
rm -rf spacy-lookups-data
