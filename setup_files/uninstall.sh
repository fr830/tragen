#!/bin/bash

sudo pip uninstall opcua
cd ..
if [ -e "installation-files.txt" ]
then
	sudo rm -r $(cat installation-files.txt)
else
	sudo python ./setup.py install --record installation-files.txt
        sudo rm -r $(cat installation-files.txt)
fi

sudo rm -r dist build *egg-info 2>/dev/null
