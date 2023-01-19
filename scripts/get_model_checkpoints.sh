# use the training venv
source environments/training/bin/activate

# clean our models
pip uninstall grc_homercy_treebanks_trf -y
pip uninstall grc_homercy_treebanks_sm -y

# install our models
pip install https://huggingface.co/janko/grc_homercy_treebanks_trf/resolve/main/grc_homercy_treebanks_trf-any-py3-none-any.whl
pip install https://huggingface.co/kardosdrur/grc_homercy_treebanks_sm/resolve/main/grc_homercy_treebanks_sm-any-py3-none-any.whl