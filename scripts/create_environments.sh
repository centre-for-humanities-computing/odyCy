# Cleaning previous environments
rm -rf environments/
# Making folder for environments
mkdir -p environments
for ENVIRONMENT in "preprocessing" "training" "packaging"
do
    python3 -m venv environments/$ENVIRONMENT
    source environments/$ENVIRONMENT/bin/activate
    pip install -r "requirements_$ENVIRONMENT.txt"
    deactivate
done