''' Locate micro:bit and send a software keystroke when the micro:bit 
 sends a trigger. This goes on the desktop as part of the hand_shake
 system. 
 https://www.seismicmatt.com/handshake/
 May '20 - the microbit base station is now hot pluggable
 Matthew Oppenheim 2020 '''

import keyboard
import logging
import serial
import serial.tools.list_ports as list_ports
import time

BAUD = 115200
PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1


logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S')

class Serial_Con():
    ''' Create a serial connection in a context manager. '''

    def __init__(self, comport, baud=BAUD):
        self.comport = comport
        self.baud = baud
        logging.info('creating a serial connection')

    
    def __enter__(self):
        ''' Return a serial port connection. '''
        try:
            self.serial_connection = serial.Serial(self.comport, self.baud,
                rtscts=True, dsrdtr=True, timeout=TIMEOUT)
            return self.serial_connection
        except Exception as e:
            logging.info('serial_connect error {}'.format(e))
            return None


    def __exit__(self, *args):
        try:
            self.serial_connection.close()
        except Exception as e:
            logging.info('failed to close serial_connection: {}'.format(e))
        logging.info('Serial_Con closed')

    
def find_comport(pid, vid, baud):
    ''' Open the serial port with device with <pid> and <vid> connected. '''
    ser_port = serial.Serial(timeout = TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    logging.debug('scanning ports')
    for p in ports:
        logging.debug('pid: {} vid: {}'.format(p.pid, p.vid))
        if (p.pid == pid) and (p.vid == vid):
            logging.debug('found target device pid: {} vid: {} port: {}'.format(p.pid, p.vid, p.device))
            return str(p.device)
    return None


def get_comport(pid, vid, baud):
    ''' Get a serial connection to pid, vid. '''
    comport = find_comport(pid, vid, baud)
    while True:
        if comport:
            return comport
        comport = find_comport(pid, vid, baud)
        time.sleep(0.5)


def detect_gesture(line):
    if(line.strip() == "shake"):
        return True
    return False


def send_f1_keystroke():
  ''' Send a software F1 keypress and release. '''
  keyboard.press_and_release('F1')


def send_1_keystroke():
  ''' Send a software 1 keypress and release. '''
  keyboard.press_and_release('1')


def main():
    logging.info('*** looking for a microbit')
    while True:
        mbit_port = get_comport(PID_MICROBIT, VID_MICROBIT, 115200)
        logging.info('microbit found at comport: {}'.format(mbit_port))
        with Serial_Con(mbit_port) as mbit_serial:
        # occassionally mbit_serial is not created, so is None
            if not mbit_serial:
                logging.info('failed to create mbit_serial')
                time.sleep(0.5)
                continue
            logging.info('waiting to detect a shake')
            while True:
                try:
                    line = mbit_serial.readline().decode('utf-8')
                except serial.SerialException as e:
                    logging.info('connection broken')
                    logging.debug('exception: {}'.format(e))
                    break
                if line:  # If it isn't a blank line
                    logging.debug('line: {}'.format(line))
                if(detect_gesture(line)):
                    # F1 is the default key for control with Grid 3
                    send_f1_keystroke() 
                    logging.info('*** shake detected')
                    # For testing
                    # python pythsend_1_keystroke() 
                mbit_serial.flushInput()
                time.sleep(0.1)


if __name__ == '__main__':
    main()
    print('exiting')

