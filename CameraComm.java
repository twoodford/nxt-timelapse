import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;

import lejos.pc.comm.NXTCommLogListener;
import lejos.pc.comm.NXTConnector;

public class CameraComm {
   public static void main(String[] args) throws IOException {
      NXTConnector conn = new NXTConnector();

      conn.addLogListener(new NXTCommLogListener() {
         public void logEvent(String msg) {
            System.out.println("Comm: "+msg);
         }

         public void logEvent(Throwable thr) {
            System.out.println("Comm Stack Trace: ");
            thr.printStackTrace();
         }
      });
      boolean success = conn.connectTo("usb://");
      if (!success) {
         System.out.println("Couldn't connect, exiting");
         return;
      }

      DataOutputStream out = new DataOutputStream(conn.getOutputStream());
      DataInputStream in = new DataInputStream(conn.getInputStream());
      out.writeByte(CameraBot.FORWARD);
      out.writeInt(80);
      out.flush();
      byte outType = in.readByte();
      if (outType==CameraBot.OUT_GYRO) {
         System.out.println("Gyro position: "+in.readFloat());
      }
      try{ Thread.sleep(2000); } catch (InterruptedException ie) {}
      out.writeByte(CameraBot.QUIT);
      out.flush();
      out.close();
   }
}
