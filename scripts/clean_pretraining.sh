echo "Cleaning pretraining data"
mkdir -p assets/pretraining/raw/perseus/ 
mkdir -p assets/pretraining/raw/first1k/ 
mkdir -p assets/pretraining/raw/pseudepigrapha/ 
cd assets/pretraining/raw/
cp -rf repos/canonical-greekLit/data/* perseus
cp -rf repos/First1KGreek/data/* first1k
cp -rf "repos/Online-Critical-Pseudepigrapha/static/docs/*" pseudepigrapha
rm -rf repos