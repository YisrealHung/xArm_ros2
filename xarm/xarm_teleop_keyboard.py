import sys

import rclpy
from example_interfaces.msg import UInt16MultiArray

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


msg = """
anything else : home

a/z : S1 motor control
s/x : S2 motor control
d/c : S3 motor control
f/v : S4 motor control
g/b : S5 motor control
h/n : S6 motor control

CTRL-C to quit
"""

moveBindings = {
    'a': (10),
    'z': (-10),
    's': (10),
    'x': (-10),
    'd': (10),
    'c': (-10),
    'f': (10),
    'v': (-10),
    'g': (10),
    'b': (-10),
    'h': (10),
    'n': (-10)

}

def getKey(settings):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)


def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def vels(runtime, s1, s2, s3, s4, s5, s6):
    return 'runtime: {}, S1: {}, S2: {}, S3: {}, S4: {}, S5: {}, S6: {}'.format(runtime, s1, s2, s3, s4, s5, s6)


def main():
    settings = saveTerminalSettings()

    rclpy.init()

    node = rclpy.create_node('learm_teleop_keyboard')
    pub = node.create_publisher(UInt16MultiArray, 'arm_control', 10)

    runtime = 100
    s1 = 500
    s2 = 500
    s3 = 500
    s4 = 500
    s5 = 500
    s6 = 500
    status = 0.0

    try:
        print(msg)
        print(vels(runtime, s1, s2, s3, s4, s5, s6))
        while True:
            key = getKey(settings)
            if key in moveBindings.keys():
                if key == 'a' or key == 'z':
                    s1 = round(s1 + moveBindings[key])
                    if s1 > 1000:
                      s1 = 1000
                    if s1 < 0:
                      s1 = 0
                elif key == 's' or key == 'x':
                    s2 = round(s2 + moveBindings[key])
                    if s2 > 1000:
                      s2 = 1000
                    if s2 < 0:
                      s2 = 0
                elif key == 'd' or key == 'c':
                    s3 = round(s3 + moveBindings[key])
                    if s3 > 1000:
                      s3 = 1000
                    if s3 < 0:
                      s3 = 0
                elif key == 'f' or key == 'v':
                    s4 = round(s4 + moveBindings[key])
                    if s4 > 1000:
                      s4 = 1000
                    if s4 < 0:
                      s4 = 0
                elif key == 'g' or key == 'b':
                    s5 = round(s5 + moveBindings[key])
                    if s5 > 1000:
                      s5 = 1000
                    if s5 < 0:
                      s5 = 0
                elif key == 'h' or key == 'n':
                    s6 = round(s6 + moveBindings[key])
                    if s6 > 1000:
                      s6 = 1000
                    if s6 < 0:
                      s6 = 0

                print(vels(runtime, s1, s2, s3, s4, s5, s6))

                if (status == 14):
                    print(msg)
                status = (status + 1) % 15

            else:
                s1 = 500
                s2 = 500
                s3 = 500
                s4 = 500
                s5 = 500
                s6 = 500
                if (key == '\x03'):
                    break

            learm_msg = UInt16MultiArray()
            learm_msg.data = [runtime, s1, s2, s3, s4, s5, s6]
            pub.publish(learm_msg)

    except Exception as e:
        print(e)

    finally:
        s1 = 500
        s2 = 500
        s3 = 500
        s4 = 500
        s5 = 500
        s6 = 500
        learm_msg = UInt16MultiArray()
        learm_msg.data = [runtime, s1, s2, s3, s4, s5, s6]
        pub.publish(learm_msg)

        restoreTerminalSettings(settings)


if __name__ == '__main__':
    main()
