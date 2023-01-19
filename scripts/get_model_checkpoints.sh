# use the training venv
source environments/training/bin/activate

# clean our models
pip uninstall grc_homercy_treebanks_trf -y
pip uninstall grc_homercy_treebanks_sm -y

# install our models
pip install https://huggingface.co/janko/grc_homercy_treebanks_trf/resolve/main/grc_homercy_treebanks_trf-any-py3-none-any.whl
pip install https://huggingface.co/kardosdrur/grc_homercy_treebanks_sm/resolve/main/grc_homercy_treebanks_sm-any-py3-none-any.whl

# clean models by others
pip uninstall grc_ud_proiel_trf -y
pip uninstall grc_ud_perseus_trf -y

# install models by others
pip install https://huggingface.co/Jacobo/grc_ud_proiel_trf/resolve/main/grc_ud_proiel_trf-any-py3-none-any.whl
pip install https://huggingface.co/Jacobo/grc_ud_perseus_trf/resolve/main/grc_ud_perseus_trf-any-py3-none-any.whl