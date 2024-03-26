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
pip install -U pip setuptools wheel
pip install -r "requirements_preprocessing.txt"
pip install spacy[cuda12x]
deactivate

source environments/training/bin/activate
pip install -U pip setuptools wheel
pip install -r "requirements_training.txt"
pip install spacy[cuda12x]
deactivate

source environments/packaging/bin/activate
pip install -U pip setuptools wheel
pip install -r "requirements_packaging.txt"
pip install spacy[cuda12x]
deactivate