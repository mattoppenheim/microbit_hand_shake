''' locate microbit and leostick comports and connect
flash blink1m and send character to leostick when gesture
is detected '''
import serial
import serial.tools.list_ports as list_ports
import time
import webcolors
from blink1 import blink1

fade = 0.1
COLOUR_ON = 'green'
COLOUR_OFF = 'orange'
PID_LEOSTICK = 32822
VID_LEOSTICK = 9025
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

def flash(on=COLOUR_ON, off=COLOUR_OFF, duration=0.1, repeat=2, fade=0.1):
    ''' Flash the blink1. '''
    try:
        blink = blink1.Blink1()
    except Exception as e:
        print(e)
        return
    for i in range(0, repeat):
        blink.fade_to_color(fade * 1000, on)
        time.sleep(duration)
        blink.fade_to_color(fade * 1000, off)
        time.sleep(duration)
    blink.fade_to_rgb(fade * 1000, 0, 0, 0)

def handshake_leo(leoport):
    ''' Test for response from Leostick. '''
    # send 'L' to leostick. Should recieve 'S'
    print('handshaking with leostick')
    leoport.open()
    leoport.write(b'L')
    print('sent L to leostick')
    received = leoport.read().decode('utf-8')
    print('from leostick: {}'.format(received))
    if received == 'S':
        print('leostick responds')

def detect_gesture(line):
    print('{} microbit: {}'.format(time.strftime("%H:%M:%S"), line))
    if(line.strip() == "shake"):
        print('shake detected')
        return True
    return False

def write_leo(message, leoport):
    ''' Write to the Leostick. '''
    leoport.write(message.encode('utf-8'))

def main():
    print('looking for microbit')
    ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
    print('looking for leostick')
    ser_leo = find_comport(PID_LEOSTICK, VID_LEOSTICK, 9600)
    if ser_leo:
        handshake_leo(ser_leo)
    else:
        print('leostick not found')
    if not ser_micro:
        print('microbit not found')
        return
    print('opening and monitoring microbit port')
    ser_micro.open()
    while True:
        line = ser_micro.readline().decode('utf-8')
        if line:  # If it isn't a blank line
            if(detect_gesture(line)):
                flash(repeat=3, duration=0.1)
                if ser_leo:
                    write_leo('z',ser_leo)
    ser_micro.close()
    ser_leo.close()

if __name__ == '__main__':
    main()
    print('exiting')
