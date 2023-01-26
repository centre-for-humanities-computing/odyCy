MODEL_NAME=$1
PACKAGE_NAME=$2
PACKAGE_VERSION=$3

source environments/training/bin/activate

mkdir -p packages
python3 -m spacy package "training/$MODEL_NAME/model-best" "packages/" \
    --build wheel \
    --code "custom_components/lemmatizer.py" \
    --create-meta \
    --version $PACKAGE_VERSION