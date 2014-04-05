import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Arrays;

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
      
      if(args.length>0) {
          System.out.println("CLI command: "+args[0]);
          String[] cmd = new String[args.length-1];
          System.arraycopy(args, 1, cmd, 0, cmd.length);
          cmd(conn, cmd);
      } else {
          String cmd;
          BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
          while(!(cmd = bufferedReader.readLine()).equals("quit")) {
              cmd(conn, cmd.split(" "));
          }
      }
      DataOutputStream out = new DataOutputStream(conn.getOutputStream());
      out.writeByte(CameraBot.QUIT);
      out.flush();
      out.close();
   }

   public static void cmd(NXTConnector conn, String[] cmd) throws IOException {
      DataOutputStream out = new DataOutputStream(conn.getOutputStream());
      DataInputStream in = new DataInputStream(conn.getInputStream());
      
      if(cmd[0].equals("forward")){
          out.writeByte(CameraBot.FORWARD);
          out.writeInt(80);
          out.flush();
          byte outType = in.readByte();
          if (outType==CameraBot.OUT_GYRO) {
              System.out.println("Gyro position: "+in.readFloat());
          }
          try{ Thread.sleep(2000); } catch (InterruptedException ie) {}
      } else if (cmd[0].equals("continuous")) {
          out.writeByte(CameraBot.CONTINUOUS_FW);
          out.flush();
      } else if (cmd[0].equals("stop")) {
          out.writeByte(CameraBot.STOP);
          out.flush();
      } else if (cmd[0].equals("calibfw")) {
          out.writeByte(CameraBot.CALIB_FW);
          out.writeInt(Integer.parseInt(cmd[1]));
          out.writeInt(Integer.parseInt(cmd[2]));
          out.flush();
          byte outType = in.readByte();
          if (outType==CameraBot.OUT_GYRO) {
              System.err.println("Gyro position: "+in.readFloat());
          }
      } else if (cmd[0].equals("quit")) {
          out.writeByte(CameraBot.QUIT);
          out.flush();
      }
   }
}
