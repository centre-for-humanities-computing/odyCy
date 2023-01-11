rm -rf assets/named_entities
mkdir -p assets/named_entities
cd assets/named_entities
# Fetching personal names from CLTK's repo
mkdir -p repos
cd repos
git clone https://github.com/cltk/greek_ner_v1.git
# Fetching place names from PLEAIDES
curl --remote-name-all https://atlantides.org/downloads/pleiades/gis/pleiades_gis_data.zip
unzip pleiades_gis_data.zip -d pleiades
rm pleiades_gis_data.zip

