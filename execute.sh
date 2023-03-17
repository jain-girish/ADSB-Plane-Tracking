#!/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt install apache2 -y
user=$(id -un)
dir=$(pwd)
sudo chown $user: /var/www/html/index.html
sudo cp $dir/*.py /var/www/html/
sudo cp $dir/*.json /var/www/html/
sudo cp $dir/*.js /var/www/html/
sudo cp $dir/*.txt /var/www/html/
sudo cp $dir/*.css /var/www/html/
sudo cp $dir/*.html /var/www/html/index.html
sudo cp -r $dir/pyModeS /var/www/html/
echo "##################"
echo 
echo "Open a web-brower and enter this ip: $(hostname -I)"
echo
echo "##################"
python /var/www/html/app.py
