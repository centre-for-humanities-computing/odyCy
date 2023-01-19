source environments/training/bin/activate
echo "Using $VIRTUAL_ENV"
for MODEL_NAME in "grc_ud_proiel_trf" "grc_ud_perseus_trf"
    do
    for CORPUS in "joint" "perseus" "proiel"
    do
        mkdir -p "metrics/$MODEL_NAME/1.0.0/$CORPUS"
        spacy evaluate "$MODEL_NAME" corpus/$CORPUS/test.spacy --output "metrics/$MODEL_NAME/1.0.0/$CORPUS/hub_version.json" --gpu-id 0
    done
done