import rospy
from interbotix_xs_msgs.msg import ArmJoy
import sys, select, termios, tty

class publish():
    def __init__(self):
        keys = 'adwsqejlikzxochptu'
        self.pause_joy_cmd = ArmJoy()

        self.li = list(keys)
        self.settings = termios.tcgetattr(sys.stdin)
        
        pub_joy_cmd = rospy.Publisher("wx200/commands/joy_processed", ArmJoy, queue_size=10)
        try:
            while True:
                key = self.getKey()
                if key in self.li:
                    joy_cmd = self.map_key_to_cmd(key)
                    for _ in range(30):
                        pub_joy_cmd.publish(joy_cmd)
                elif key == 'n':  
                    break
                else:
                #     # Stop the robot if any other key is pressed
                    pub_joy_cmd.publish(self.pause_joy_cmd)
                pub_joy_cmd.publish(self.pause_joy_cmd)   

        except Exception as e:
            print(e)

        finally:
            #Stop the robot before exiting
            pub_joy_cmd.publish(self.pause_joy_cmd)
            
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        
    def map_key_to_cmd(self,key): 
        joy_cmd = ArmJoy()
        if key == 'a':
            joy_cmd.ee_x_cmd = ArmJoy.EE_X_DEC
        elif key == 'd':
            joy_cmd.ee_x_cmd = ArmJoy.EE_X_INC
        elif key == 'w':
            joy_cmd.ee_y_cmd = ArmJoy.EE_Y_INC
        elif key == 's':
            joy_cmd.ee_y_cmd = ArmJoy.EE_Y_DEC
        elif key == 'q':
            joy_cmd.ee_z_cmd = ArmJoy.EE_Z_DEC
        elif key == 'e':
            joy_cmd.ee_z_cmd = ArmJoy.EE_Z_INC
        elif key == 'j':
            joy_cmd.ee_roll_cmd = ArmJoy.EE_ROLL_CCW
        elif key == 'l':
            joy_cmd.ee_roll_cmd = ArmJoy.EE_ROLL_CW
        elif key == 'i':
            joy_cmd.ee_pitch_cmd = ArmJoy.EE_PITCH_UP
        elif key == 'k':
            joy_cmd.ee_pitch_cmd = ArmJoy.EE_PITCH_DOWN
        elif key == 'z':
            joy_cmd.waist_cmd = ArmJoy.WAIST_CCW
        elif key == 'x':
            joy_cmd.waist_cmd = ArmJoy.WAIST_CW
        elif key == 'o':
            joy_cmd.gripper_cmd = ArmJoy.GRIPPER_OPEN
        elif key == 'c':
            joy_cmd.gripper_cmd = ArmJoy.GRIPPER_CLOSE
        elif key == 'h':
            joy_cmd.pose_cmd = ArmJoy.HOME_POSE
        elif key == 'p':
            joy_cmd.pose_cmd = ArmJoy.SLEEP_POSE
        elif key == 't':
            joy_cmd.torque_cmd = ArmJoy.TORQUE_ON
        elif key == 'u':
            joy_cmd.torque_cmd = ArmJoy.TORQUE_OFF

        return joy_cmd

    def getKey(self):
    # Function to get the pressed key
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key
       
if __name__ == "__main__":
    rospy.init_node("xsarm_keyboard_control")
    
    rospy.loginfo("Arm control using the keyboard is now active.")
    rospy.loginfo("Use the following keys to control the arm:")
    rospy.loginfo("w: Move EE Y+  s: Move EE Y-  a: Move EE X-  d: Move EE X+")
    rospy.loginfo("q: Move EE Z-  e: Move EE Z+  j: Roll EE CCW  l: Roll EE CW")
    rospy.loginfo("i: Pitch EE Up  k: Pitch EE Down  z: Waist CCW  x: Waist CW")
    rospy.loginfo("o: Open Gripper  c: Close Gripper  h: Home Pose  p: Sleep Pose")
    rospy.loginfo("t: Enable Torque  u: Disable Torque")
 
    publish()