# upgrade system
sudo apt full-upgrade -y
sudo apt update -y
# nvidia drivers
sudo apt install nvidia-headless-460 nvidia-utils-460 -y
# general util
sudo apt install zip unzip git-lfs -y
# python util
sudo apt install python3-pip python3-venv -y