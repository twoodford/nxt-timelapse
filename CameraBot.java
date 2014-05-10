/* Copyright 2014 Timothy Woodford */

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.EOFException;
import lejos.nxt.Motor;
import lejos.nxt.SensorPort;
import lejos.nxt.Sound;
import lejos.nxt.addon.GyroDirectionFinder;
import lejos.nxt.addon.GyroSensor;
import lejos.nxt.comm.USB;
import lejos.nxt.comm.USBConnection;
import lejos.nxt.comm.NXTConnection;
import lejos.robotics.DirectionFinder;
import lejos.robotics.navigation.DifferentialPilot;

public class CameraBot {
   public static final byte FORWARD = 0x10;
   public static final byte QUIT = 0x11;
   public static final byte DONE = 0x20;

   private GyroDirectionFinder direction;
   
   public CameraBot(){
      direction = new GyroDirectionFinder(new GyroSensor(SensorPort.S2), true); 
      direction.setDegrees(0);
   }

   public void serveConn(NXTConnection conn) throws IOException {
      DataInputStream in = conn.openDataInputStream();
      DataOutputStream out = conn.openDataOutputStream();

      srvLoop: while(true) {
         try {
            byte cmd = in.readByte();
            System.out.print(cmd+": ");
            switch(cmd) {
               case FORWARD:
                  System.out.println("forward");
                  int rot = in.readInt();
                  forward(rot);
                  out.writeByte(DONE);
                  out.flush();
                  break;
              case QUIT:
                  break srvLoop;
            }
         } catch (EOFException eofe) {
             System.out.println("IOException!");
            break srvLoop;
         }
      }
   }

   public void forward(int rot) {
       Motor.A.rotate(rot, true);
   }

   public static void main(String[] args){
      Motor.A.setSpeed(300);
      CameraBot bot = new CameraBot();
      Sound.beep();
      runLoop: while(true) {
         USBConnection conn = USB.waitForConnection();
         try {
            bot.serveConn(conn);
         } catch (IOException ioe) {}
         conn.close();
      }
   }
}
