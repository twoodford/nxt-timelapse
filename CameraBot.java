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
   public static final byte CONTINUOUS_FW = 0x12;
   public static final byte STOP = 0x13;
   public static final byte OUT_GYRO = 0x50;

   private GyroDirectionFinder direction;
   private DifferentialPilot pilot;
   private boolean msw = false;
   
   public CameraBot(){
      direction = new GyroDirectionFinder(new GyroSensor(SensorPort.S2), true); 
      direction.setDegrees(0);
      pilot = new DifferentialPilot(4.5f*8/24, 14f, Motor.A, Motor.B);
      //pilot.travel(3);
      //pilot.setTravelSpeed(30);
   }

   public void serveConn(NXTConnection conn) throws IOException {
      DataInputStream in = conn.openDataInputStream();
      DataOutputStream out = conn.openDataOutputStream();

      srvLoop: while(true) {
         try {
            byte cmd = in.readByte();
            switch(cmd) {
               case FORWARD:
                  System.out.println("forward");
                  int rot = in.readInt();
                  forward(rot);
                  out.writeByte(OUT_GYRO);
                  out.writeFloat(direction.getDegrees());
                  out.flush();
                  break srvLoop;
               case CONTINUOUS_FW:
                  System.out.println("continuous");
                  pilot.setTravelSpeed(1);
                  pilot.travel(100000, true);
                  break srvLoop;
               case STOP:
                  pilot.stop();
                  break srvLoop;
               case QUIT:
                  break srvLoop;
            }
         } catch (EOFException eofe) {
            break srvLoop;
         }
      }
   }

   public void forward(int rot) {
      
      if(msw) {
         Motor.A.rotate(rot, true);
         Motor.B.rotate(rot, false);
      } else {
         Motor.B.rotate(rot, true);
         Motor.A.rotate(rot, false);
      }
      msw = !msw;
      if(direction.getDegreesCartesian()<-0.5f) {
          Motor.A.rotate((int) direction.getDegreesCartesian());
          Motor.B.rotate((int) -direction.getDegreesCartesian());
      } else if (direction.getDegreesCartesian()>0.5f) {
          Motor.A.rotate((int) -direction.getDegreesCartesian());
          Motor.B.rotate((int) direction.getDegreesCartesian());
      }
      //pilot.travel(2);
      //pilot.rotate(direction.getDegreesCartesian());
      direction.resetCartesianZero();
   }

   public void recalibrate() {
       direction.startCalibration();
    }

   public static void main(String[] args){
      Motor.A.setSpeed(300);
      Motor.B.setSpeed(300);
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
