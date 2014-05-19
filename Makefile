all: upload CameraComm.class

CameraBot.class: CameraBot.java
	nxjc CameraBot.java

CameraComm.class: CameraComm.java
	nxjpcc CameraComm.java

CameraBot.nxj: CameraBot.class
	nxjlink -o CameraBot.nxj -od CameraBot.nxd CameraBot

upload: CameraBot.nxj
	nxjupload -r CameraBot.nxj

clean:
	rm -f *.class *.nxj *.nxd
