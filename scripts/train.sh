# Assigning command line arguments to variables
CONFIG=$1
MODEL_NAME=$2
CORPUS=$3
DEVICE=$4

source environments/training/bin/activate
wandb login

args=()
args+=( "configs/$CONFIG.cfg" )
args+=( "--output" ) 
args+=( "training/$MODEL_NAME" ) 
args+=( "--paths.train" ) 
args+=( "corpus/$CORPUS/train.spacy" ) 
args+=( "--paths.dev" ) 
args+=( "corpus/$CORPUS/dev.spacy" ) 

# don't import custom component for ner models (it's already inherited)
if [ $CORPUS != "ner"]
then
    args+=( "--code" ) 
    args+=( "custom_components/lemmatizer.py" )
fi

# add gpu arg for trf models
if [ $DEVICE == "gpu" ]
then
    args+=( "--gpu-id" )
    args+=( "0" )
fi

python3 -m spacy train "${args[@]}"