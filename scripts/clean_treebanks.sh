echo "Cleaning treebanks"
mkdir -p assets/treebanks/perseus/ 
mkdir -p assets/treebanks/proiel/ 
mkdir -p assets/treebanks/joint/ 
cp -f assets/treebanks/ud-treebanks-v*/UD_Ancient_Greek-Perseus/* assets/treebanks/perseus
cp -f assets/treebanks/ud-treebanks-v*/UD_Ancient_Greek-PROIEL/* assets/treebanks/proiel
rm -rf assets/treebanks/ud-treebanks-v*