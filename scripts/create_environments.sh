# Cleaning previous environments
rm -rf environments/
# Making folder for environments
mkdir -p environments
# Creating environment for preprocessing
python3 -m venv environments/preprocessing
source environments/preprocessing/bin/activate
pip install -r requirements_preprocessing.txt
deactivate
# Creating environment for training
python3 -m venv environments/training
source environments/training/bin/activate
pip install -r requirements_training.txt
deactivate
# Creating environment for packaging
python3 -m venv environments/packaging
source environments/packaging/bin/activate
pip install -r requirements_packaging.txt
deactivate