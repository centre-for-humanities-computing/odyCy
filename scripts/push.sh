MODEL_NAME=$1
PACKAGE_NAME=$2
PACKAGE_VERSION=$3
LANG=$4

source environments/packaging/bin/activate

# Logging into Huggingface
huggingface-cli login

# Packaging the model up
mkdir -p packages
python3 -m spacy package "training/$MODEL_NAME/model-best" "packages/" --build wheel --name $PACKAGE_NAME --create-meta --force

# Pushing to Huggingface
python3 -m spacy huggingface-hub push "packages/${LANG}_${PACKAGE_NAME}-${PACKAGE_VERSION}/dist/${LANG}_${PACKAGE_NAME}-${PACKAGE_VERSION}-py3-none-any.whl"
