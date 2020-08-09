''' Locate micro:bit and send a software keystroke when the micro:bit 
 sends a trigger. This goes on the desktop as part of the hand_shake
 system. 
 https://www.seismicmatt.com/handshake/
 Windows only as the target software is Windows only.
 May '20 - the microbit base station is now hot pluggable.
 Aug'20 - command line options to change keystroke.
 e.g. to broadcast F2 keystroke:
 python -u base.py --keystroke="F2"
 Matthew Oppenheim 2020 '''

import click
import keyboard
import logging
import serial
import serial.tools.list_ports as list_ports
import sys
import time
try:
    import win32gui
except ModuleNotFoundError:
    print('you need to install win32gui\npip install pywin32')
    pass

ADMIN_SOFTWARE = ['grid']
BAUD = 115200
# keystroke to broadcast when a shake is detected
KEYSTROKE='F1'
PID_MICROBIT = 516
# software that requires this script to run in Administrator mode 
VID_MICROBIT = 3368
TIMEOUT = 0.1

try:
    # need the windll library to elevate to Administrator mode in windows
    from ctypes import windll
except ImportError:
    print('need to run this on Windows if you want to use: {}'.format(ADMIN_SOFTWARE))
    pass

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


def target_admin_sware(software=ADMIN_SOFTWARE):
    ''' Check if target software requires this script to run as Administrator. '''
    toplist, winlist = [], []
    logging.info('Looking for software that requires elevation to Aministrator: {}'
        .format(ADMIN_SOFTWARE))
    def _enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(_enum_cb, toplist)
    for sware in software:
        # winlist is a list of tuples (window_id, window title)
        for hwnd, title in winlist:
            if sware in title.lower():
                logging.info('found software requiring Administrator mode {}'
                    .format(title))
                return True
    return False


def main(keystroke):
    logging.info('software keystroke is {}'.format(keystroke))
    target_admin_sware()
    service_microbit(keystroke)        


def service_microbit(keystroke=KEYSTROKE):
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
            shake_count = 1
            while True:
                try:
                    line = mbit_serial.readline().decode('utf-8')
                except serial.SerialException as e:
                    logging.info('connection broken')
                    logging.debug('exception: {}'.format(e))
                    break
                if line:  # If it isn't a blank line
                    logging.debug('serial port: {}'.format(line))
                if(detect_gesture(line)):
                    send_keystroke(keystroke) 
                    logging.info('*** shake {} detected, {} sent'.format(
                        shake_count, keystroke))
                    shake_count += 1
                mbit_serial.flushInput()
                time.sleep(0.1)


if __name__ == '__main__':
    # sys.argv line for testing
    #sys.argv = ['','--keystroke=1']
    main()
    print('exiting')
    sys.exit()