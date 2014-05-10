nxt-timelapse
=============

Tool to create movement in a timelapse video using a Lego Mindstorms NXT robot and the lejos firmware.  The eventual goal is to use a standard 2x4 piece of wood as the rail that the camera will move along.  Also planned is pan and tilt support.  Stay tuned.

Prerequisites
-------------

* Lejos (from lejos.org)
* gphoto2
* cython
* A Lego Mindstorms robot a single motor for movement.  This is probably the most difficult part of the setup.  I hope to add general instructions for how I did it at some point.

Building and Running
--------------------

Run `make` to compile and link the relevant files, and upload and run the program on the NXT.  Connect a USB cable to the robot and run `moverobot.sh` to ensure that the movement works, then use `simeplerunner.sh` with a camera connected via PTP/MTP to create a timelapse.

The GUI can be run by running the standard build.py procedure, then running the buildlapse.main module.
