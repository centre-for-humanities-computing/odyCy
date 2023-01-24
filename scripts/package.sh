MODEL_NAME=$1
PACKAGE_NAME=$2

source environments/packaging/bin/activate

mkdir -p packages
python3 -m spacy package "training/$MODEL_NAME/model-best" "packages/" --build wheel --name $PACKAGE_NAME --code "custom_components/lemmatizer.py" --create-meta --force