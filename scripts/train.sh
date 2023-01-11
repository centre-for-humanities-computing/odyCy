# Assigning command line arguments to variables
CONFIG = $1
MODEL_NAME = $2
CORPUS = $3

source environments/training/bin/activate
wandb login
python3 -m spacy train configs/$CONFIG.cfg --output training/$MODEL_NAME --paths.train corpus/$CORPUS/train.spacy --paths.dev corpus/$CORPUS/dev.spacy --gpu-id 0
deactivate