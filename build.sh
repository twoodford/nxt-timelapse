#!/bin/sh
TOOL_PATH="../leJOS_NXJ_svn/bin"

nxjc CameraBot.java
nxjpcc CameraComm.java
nxjlink -o CameraBot.nxj -od CameraBot.nxd CameraBot
nxjupload -r CameraBot.nxj
#sleep 1
#echo "running"
#nxjpc CameraComm
