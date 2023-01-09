echo "Downloading pretraining corpus:"
rm -rf assets/pretraining
mkdir -p assets/pretraining
cd assets/pretraining
mkdir -p raw
cd raw
mkdir -p repos
cd repos
echo " - Cloning Perseus"
git clone "https://github.com/PerseusDL/canonical-greekLit"
echo " - Cloning First1K Greek"
git clone "https://github.com/OpenGreekAndLatin/First1KGreek"
echo " - Cloning Online Critical Pseudepigrapha"
git clone "https://github.com/OnlineCriticalPseudepigrapha/Online-Critical-Pseudepigrapha.git"
