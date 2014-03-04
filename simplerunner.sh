#!/bin/sh
while true; do
   gphoto2 --trigger-capture
   sleep 2
   sh moverobot.sh
   sleep 3
done
