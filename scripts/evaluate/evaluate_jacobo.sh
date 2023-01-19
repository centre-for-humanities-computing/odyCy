# create a new venv
python3 -m venv environments/eval_jacobo
source environments/eval_jacobo/bin/activate

# fetch jacobo's models
# clean existing instalation
pip uninstall grc_ud_proiel_trf -y
pip uninstall grc_ud_perseus_trf -y

# install models
pip install https://huggingface.co/Jacobo/grc_ud_proiel_trf/resolve/main/grc_ud_proiel_trf-any-py3-none-any.whl
pip install https://huggingface.co/Jacobo/grc_ud_perseus_trf/resolve/main/grc_ud_perseus_trf-any-py3-none-any.whl

echo "Using $VIRTUAL_ENV"
for MODEL_NAME in "grc_ud_proiel_trf" "grc_ud_perseus_trf"
    do
    for CORPUS in "joint" "perseus" "proiel"
    do
        mkdir -p "metrics/$MODEL_NAME/1.0.0/$CORPUS"
        spacy evaluate "$MODEL_NAME" corpus/$CORPUS/test.spacy --output "metrics/$MODEL_NAME/1.0.0/$CORPUS/hub_version.json" --gpu-id 0
    done
done