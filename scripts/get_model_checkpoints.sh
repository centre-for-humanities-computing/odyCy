# use the training venv
source environments/training/bin/activate

# clean our models
pip uninstall grc_homercy_treebanks_trf -y
pip uninstall grc_homercy_treebanks_sm -y
pip uninstall grc_dep_treebanks_trf -y
pip uninstall grc_dep_treebanks_sm -y

# install final models
pip install https://huggingface.co/janko/grc_homercy_treebanks_trf/resolve/main/grc_homercy_treebanks_trf-any-py3-none-any.whl

# install dep models
pip install https://huggingface.co/janko/grc_dep_treebanks_trf/resolve/main/grc_dep_treebanks_trf-any-py3-none-any.whl