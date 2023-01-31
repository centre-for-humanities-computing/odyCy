MODEL_NAME=$1
PACKAGE_NAME=$2
PACKAGE_VERSION=$3
CUSTOM_COMPONENT=$4

source environments/training/bin/activate

mkdir -p packages

args=()
# input / output
args+=( "training/$MODEL_NAME/model-best" )
args+=( "packages/" )
# build style
args+=( "--build" )
args+=( "wheel" )
# metadata
args+=( "--create-meta" )
args+=( "--name" ) # override meta package name
args+=( "$PACKAGE_NAME" )
args+=( "--version" ) # override meta with version
args+=( "$PACKAGE_VERSION" )

if [ "$CUSTOM_COMPONENT" == "frequency_lemmatizer" ]
then
    args+=( "--code" ) 
    args+=( "custom_components/lemmatizer.py" )
fi

python3 -m spacy package "${args[@]}"