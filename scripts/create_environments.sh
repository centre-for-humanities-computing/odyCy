# Cleaning previous environments
rm -rf environments/
# Making folder for environments
mkdir -p environments
for ENVIRONMENT in "preprocessing" "training" "packaging"
do
    echo "Installing VENV: $ENVIRONMENT"
    python3 -m venv environments/$ENVIRONMENT
    source environments/$ENVIRONMENT/bin/activate
    pip install -r "requirements_$ENVIRONMENT.txt"
    deactivate
done

# extra installation of the cu101 integtaion for torch
source environments/training/bin/activate
pip install torch==1.8.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html
pip install spacy[cuda101]
deactivate

source environments/packaging/bin/activate
pip install torch==1.8.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html
pip install spacy[cuda101]
deactivate