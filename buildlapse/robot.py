# robot.py
# An interface to the Java-based robot controller
import subprocess

class RobotCtl(object):
    def __init__(self):
        self.sproc = subprocess.Popen(["nxjpc", "CameraComm"], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
        self.sproc.stdout.readline() # Wait for startup
    
    def _write(self, msg):
        self.sproc.stdin.write(bytes(msg, "ascii"))

    def calibfw(self, left, right):
        self._write("calibfw {0} {1}\n".format(left, right))

    def close(self):
        self._write("quit\n")
        self.sproc.communicate()

if __name__=="__main__":
    rctl = RobotCtl()
    print("Connection started")
    rctl.calibfw(100, 300)
    print("Movement Done")
    rctl.close()
