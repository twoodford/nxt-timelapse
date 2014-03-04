nxt-timelapse
=============

Tool to create movement in a timelapse video using a Lego Mindstorms NXT robot and the lejos firmware

Prerequisites
-------------

* Lejos (from lejos.org)
* gphoto2
* A Lego Mindstorms robot with two wheels and a camera mounted on it.  This is probably the most difficult part of the setup.  I hope to add general instructions for how I did it at some point.

Building and Running
--------------------

Run the `build.sh` function to compile and link the relevant files, and upload and run the program on the NXT.  Connect a USB cable to the robot and run `moverobot.sh` to ensure that the movement works, then use `simeplerunner.sh` with a camera connected via PTP/MTP to create a timelapse.

