#!/bin/sh
while true; do
   gphoto2 --trigger-capture
   sleep 2
   nxjpc CameraComm forward
   sleep 3
done
