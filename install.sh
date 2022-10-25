#!/bin/bash

echo "Updating system..."
sudo apt-get update -qq
echo -e "Installing dependencies..."
sudo apt-get install -y -qq python3 python3-pip >/dev/null
pip uninstall -y -qq discord.py
pip uninstall -y -qq pydiscord
pip uninstall -y -qq python-discord
pip install --progress-bar off -qq -r requirements.txt
echo -e "Finishing up..."
echo "#!/bin/bash" > cybersec
echo >> cybersec
echo "python3 -B \"$(pwd)/main.py\" \$@" >> cybersec
chmod +x cybersec
sudo mv cybersec /usr/local/bin/cybersec
echo -e "\nDONE!"
