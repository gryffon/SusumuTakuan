#!/bin/bash

#
# control.sh
#
# A control script to run SusumuTakuan, 
# the L5R DiscordBot
#

cmd=$1

if [ "$cmd" == "start" ]; then
		#Start SusumuTakuan
		supervisorctl start takuan

elif [ "$cmd" == "stop" ]; then
		#Stop SusumuTakuan
		supervisorctl stop takuan

elif [ "$cmd" == "restart" ]; then
		#Restart SusumuTakuan
		supervisorctl restart takuan

elif [ "$cmd" == "refresh" ]; then
		#Refresh Code
		git pull
fi