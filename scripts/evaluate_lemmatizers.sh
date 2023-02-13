source environments/training/bin/activate
echo "Creating lemmatizer effect estimation models."
python3 scripts/create_lemmatizer_models.py

for MODEL in "only_lookup" "only_trainable" "only_freq"
do
    for CORPUS in "perseus" "proiel" "joint" 
    do
        echo "Evaluating homercy_trf_${MODEL} on $CORPUS"
        mkdir -p metrics/homercy_trf_$MODEL/$VERSION/
        python3 -m spacy benchmark accuracy models/lemmatizer_effect/$MODEL corpus/$CORPUS/test.spacy --output metrics/homercy_trf_$MODEL/$VERSION/$CORPUS.json --code custom_components/lemmatizer.py
    done
done
deactivate

