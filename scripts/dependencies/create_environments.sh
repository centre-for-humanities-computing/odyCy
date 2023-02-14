# Cleaning previous environments
rm -rf environments/
# Making folder for environments
mkdir -p environments

# Creating virtual environments
for ENVIRONMENT in "preprocessing" "training" "packaging"
do
    echo "Installing VENV: $ENVIRONMENT"
    python3 -m venv environments/$ENVIRONMENT
done

# Installing dependencies for environments
source environments/preprocessing/bin/activate
pip install -r "requirements_preprocessing.txt"
pip install torch==1.8.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html
pip install spacy[cuda101]
pip install --upgrade torch
deactivate

source environments/training/bin/activate
pip install -r "requirements_training.txt"
pip install torch==1.8.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html
pip install spacy[cuda101]
pip install --upgrade torch
deactivate

source environments/packaging/bin/activate
pip install -r "requirements_packaging.txt"
pip install torch==1.8.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html
pip install spacy[cuda101]
pip install --upgrade torch
deactivate