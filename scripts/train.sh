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
if [ $DEVICE == "gpu" ]
then
    args+=( "--gpu-id" )
    args+=( "0" )
fi

python3 -m spacy train "${args[@]}"