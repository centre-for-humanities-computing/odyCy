###
### jacobo proiel
###

MODEL1="grc_ud_proiel_trf"

# create a new venv
python3 -m venv environments/$MODEL1
source environments/$MODEL1/bin/activate
echo "Using $VIRTUAL_ENV"

# fetch model
pip uninstall $MODEL1 -y
pip install "https://huggingface.co/Jacobo/$MODEL1/resolve/main/$MODEL1-any-py3-none-any.whl"

# eval proiel
for CORPUS in "joint" "perseus" "proiel"
    do
    mkdir -p "metrics/$MODEL1/1.0.0/$CORPUS"
    spacy evaluate "$MODEL1" corpus/$CORPUS/test.spacy --output "metrics/$MODEL1/1.0.0/$CORPUS/hub_version.json"
done

deactivate

###
### jacobo perseus
###

MODEL2="grc_ud_perseus_trf"

# create a new venv
python3 -m venv environments/$MODEL2
source environments/$MODEL2/bin/activate
echo "Using $VIRTUAL_ENV"

# fetch model
pip uninstall $MODEL2 -y
pip install "https://huggingface.co/Jacobo/$MODEL2/resolve/main/$MODEL2-any-py3-none-any.whl"

# eval perseus
for CORPUS in "joint" "perseus" "proiel"
    do
    mkdir -p "metrics/$MODEL2/1.0.0/$CORPUS"
    spacy evaluate "$MODEL2" corpus/$CORPUS/test.spacy --output "metrics/$MODEL2/1.0.0/$CORPUS/hub_version.json"
done

deactivate