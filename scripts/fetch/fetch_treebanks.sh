echo "Downloading treebanks"
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-4923/ud-treebanks-v2.11.tgz
mkdir -p assets/treebanks
tar -xvzf ud-treebanks-v2.11.tgz -C assets/treebanks/
rm ud-treebanks-v2.11.tgz 
