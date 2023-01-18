# use the training venv
source environments/training/bin/activate

# transformer model
pip install https://huggingface.co/janko/grc_homercy_treebanks_trf/resolve/main/grc_homercy_treebanks_trf-any-py3-none-any.whl
# cpu model
pip install https://huggingface.co/kardosdrur/grc_homercy_treebanks_sm/resolve/main/grc_homercy_treebanks_sm-any-py3-none-any.whl