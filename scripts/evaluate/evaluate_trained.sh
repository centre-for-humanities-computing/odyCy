# Assigning command line arguments to variables
MODEL_NAME=$1
PACKAGE_VERSION=$2

source environments/training/bin/activate
for CORPUS in "joint" "perseus" "proiel"
do
    mkdir -p "metrics/$MODEL_NAME/$PACKAGE_VERSION/$CORPUS"
    for WHICH in "best" "last"
    do
        python3 -m spacy evaluate "training/$MODEL_NAME/model-$WHICH" corpus/$CORPUS/test.spacy --output "metrics/$MODEL_NAME/$PACKAGE_VERSION/$CORPUS/$WHICH.json" --code "custom_components/lemmatizer.py"
    done
done