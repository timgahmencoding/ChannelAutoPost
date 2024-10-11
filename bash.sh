#!/bin/bash

pip3 install -r requirements.txt

while :
do
	echo "starting Bot ~@ChannelAutoForwarder";
	python3 bot.py --break-system-packages
	sleep 10
done