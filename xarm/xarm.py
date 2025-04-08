import serial
import struct
import time

import rclpy
from rclpy.node import Node
from example_interfaces.msg import UInt16MultiArray


class xArm(Node):

    def __init__(self, port = 'dev/learm',baud = 115200):
        super().__init__('xarm_node')
        self.subscription = self.create_subscription(UInt16MultiArray, 'arm_control', self.cmd_angle_callback, 10)
        self.ser = serial.Serial(port, baud, timeout = 1)
        self.get_logger().info('LeArm node is working...')


    def map_angle_to_pwm(self, value):
        in_min, in_max, out_min, out_max = 0, 180, 0, 1000
        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def forced_stop(self):
        set_servo_cmd = bytearray(b'\x55\x55\x04\x07\x00')
        self.ser.write(set_servo_cmd)

    def move_servo_angle(self, mt, s1, s2, s3, s4, s5, s6):
        s1 = self.map_angle_to_pwm(s1)
        s2 = self.map_angle_to_pwm(s2)
        s3 = self.map_angle_to_pwm(s3)
        s4 = self.map_angle_to_pwm(s4)
        s5 = self.map_angle_to_pwm(s5)
        s6 = self.map_angle_to_pwm(s6)
        set_servo_cmd = f"bus_servo.run_mult(({s1},{s2},{s3},{s4},{s5},{s6}),{mt})\r\n"
        self.ser.write(set_servo_cmd.encode('utf-8'))
        
        
    def move_servo_pwm(self, mt, s1, s2, s3, s4, s5, s6):
        set_servo_cmd = f"bus_servo.run_mult(({s1},{s2},{s3},{s4},{s5},{s6}),{mt})\r\n"
        self.ser.write(set_servo_cmd.encode('utf-8'))
        print(set_servo_cmd)


    def servo_reset_home(self):
        set_servo_cmd = "bus_servo.run_mult((500,500,500,500,500,500),1000)\r\n"
        self.ser.write(set_servo_cmd.encode('utf-8'))


    def cmd_angle_callback(self, msg):
        sd, s1, s2, s3, s4, s5, s6 = msg.data        
        self.move_servo_pwm(sd, s1, s2, s3, s4, s5, s6)




def main(args=None):
    rclpy.init(args=args)
    node = xArm(port = '/dev/ttyCH341USB0',baud = 115200)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
