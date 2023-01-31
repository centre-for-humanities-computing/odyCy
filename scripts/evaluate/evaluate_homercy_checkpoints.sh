# Assigning command line arguments to variables
MODEL_NAME=$1
PACKAGE_VERSION=$2

source environments/training/bin/activate
echo "Using $VIRTUAL_ENV"
for CORPUS in "joint" "perseus" "proiel" "ner"
do
    mkdir -p "metrics/$MODEL_NAME/$PACKAGE_VERSION/$CORPUS"
    spacy evaluate "$MODEL_NAME" corpus/$CORPUS/test.spacy --output "metrics/$MODEL_NAME/$PACKAGE_VERSION/$CORPUS/hub_version.json" --gpu-id 0
done