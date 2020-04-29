''' Locate micro:bit and send a software keystroke when the micro:bit 
 sends a trigger. This goes on the desktop as part of the hand_shake
 system. 
 https://www.seismicmatt.com/handshake/
 Matthew Oppenheim 2020 '''

import keyboard
import serial
import serial.tools.list_ports as list_ports
import time

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1


def find_comport(pid, vid, baud):
    ''' Open the serial port with device with <pid> and <vid> connected. '''
    ser_port = serial.Serial(timeout = TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print('pid: {} vid: {}'.format(p.pid, p.vid))
        if (p.pid == pid) and (p.vid == vid):
            print('found target device pid: {} vid: {} port: {}'.format(p.pid, p.vid, p.device))
            ser_port.port = str(p.device)
            return ser_port
    return None


def detect_gesture(line):
    print('{} microbit: {}'.format(time.strftime("%H:%M:%S"), line))
    if(line.strip() == "shake"):
        print('shake detected')
        return True
    return False


def send_f1_keystroke():
  ''' Send a software F1 keypress and release. '''
  keyboard.press_and_release('F1')


def send_1_keystroke():
  ''' Send a software 1 keypress and release. '''
  keyboard.press_and_release('1')


def main():
    print('looking for microbit')
    ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
    if not ser_micro:
        print('microbit not found')
        return
    print('opening and monitoring microbit port')
    ser_micro.open()
    while True:
        line = ser_micro.readline().decode('utf-8')
        if line:  # If it isn't a blank line
            if(detect_gesture(line)):
              # F1 is the default key for control with Grid 3
              send_f1_keystroke() 
              # For testing
              # send_1_keystroke() 
    ser_micro.close()
    ser_leo.close()


if __name__ == '__main__':
    main()
    print('exiting')

