#!/bin/bash

#
# control.sh
#
# A control script to run SusumuTakuan, 
# the L5R DiscordBot
#

cmd=$1

if [ "$cmd" eq "start" ]; then
		#Start SusumuTakuan
		supervisorctl start takuan

elif [ "$cmd" eq "stop" ]; then
		#Stop SusumuTakuan
		supervisorctl start takuan

elif [ "$cmd" eq "restart" ]; then
		#Restart SusumuTakuan
		supervisorctl restart takuan

elif [ "$cmd" eq "refresh" ]; then
		#Refresh Code
		git pull
fi