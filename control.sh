#!/bin/bash

#
# control.sh
#
# A control script to run SusumuTakuan, 
# the L5R DiscordBot
#

cmd=$1

branch=`git branch | cut -d " " -f2`

if [ "$branch" = "master" ]; then
	#master branch
	susumu="takuan"
elif [ "$branch" = "develop" ]; then
	#develop branch
	susumu="takuantest"
fi



if [ "$cmd" = "start" ]; then
		#Start SusumuTakuan
		supervisorctl start $susumu

elif [ "$cmd" = "stop" ]; then
		#Stop SusumuTakuan
		supervisorctl stop $susumu

elif [ "$cmd" = "restart" ]; then
		#Restart SusumuTakuan
		supervisorctl restart $susumu

elif [ "$cmd" = "refresh" ]; then
		#Refresh Code
		git pull
fi