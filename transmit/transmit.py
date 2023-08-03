''' Shake detector.
When the board is shaken harder than an adjustable threshold:
    Transmit a message to the receiver by radio.
    Activate haptic buzzer on GPIO 2.
    Play tune.
Threshold value for shake detection adjusted using a/b buttons.
button a: makes board more sensitive, lower shake needed to activate.
button b: makes board less sensitive, harder shake needed to activate.
Threshold value stored in threshold_value.txt.
There's a bug in the music library. The micro:bit freezes after a time.
Put a reset function into the main loop to compensate.
https://www.mattoppenheim.com/handshake/
Matthew Oppenheim
Last update: 2023_08_03 '''

from microbit import *
import music
import radio

ACC_DIVISOR = 100000

# Intensity of the LEDs
BRIGHT = '9'
FAINT = '4'

# number of accelerometer values to average over
FILTER_LENGTH = 10

# How many LEDs to turn on or off per button push
INCREMENT = 1
LEDS = 25
MAX_THRESH = 25
THRESH_BRIGHT = '5'
THRESHOLD = 13
THRESHOLD_VALUE = 'threshold_value.txt'

# Reset the board after this numer of milliseconds due to the music library bug
TIMEOUT = 10000

# Frequencies to play for sound prompt.
# C#
FREQ_3 = 139

# E
FREQ_2 = 165

# A
FREQ_1 = 221

radio.config(address=0x101000, group=40, channel=2, data_rate=radio.RATE_1MBIT)
print('monitoring accelerometer')


def average(list):
    ''' return the average of <list> '''
    average = sum(list)/len(list)
    return average


def detection():
    print('*** shake detected ***')
    haptic('on')
    display.show(Image.CHESSBOARD)
    radio.send('shake')
    # Play three tones, takes 210ms
    play_tone(FREQ_1)
    play_tone(FREQ_2)
    play_tone(FREQ_3)
    haptic('off')


def increase_sensitivity(threshold, inc):
    display.show('+')
    threshold = limit(threshold+inc, MAX_THRESH)
    sleep(250)
    return threshold


def decrease_sensitivity(threshold, inc):
    display.show('-')
    threshold = limit(threshold-inc, MAX_THRESH)
    sleep(250)
    return threshold


def haptic(state):
    ''' Turn haptic on/off '''
    if (state == 'on'):
        pin2.write_digital(1)
        return
    pin2.write_digital(0)


def initialise_list():
    return [1] * FILTER_LENGTH


def limit(val, limit):
    ''' limit <val> between 0 and <limit>'''
    if val > limit:
        val = limit
    if val < 0:
        val = 0
    return int(val)


def leds_string2(bright, faint):
    ''' return led string '''
    bright = limit(bright, LEDS)
    faint = limit(faint, LEDS)
    if faint <= bright:
        faint = 0
    leds_string = BRIGHT*bright + FAINT*(faint-bright) + \
        '0' * (LEDS-(bright+faint))
    leds_string = ":".join(leds_string[i:i+5]
                           for i in range(0, len(leds_string), 5))
    leds_image = Image(leds_string + ':')
    return leds_image


def play_tone(frequency):
    ''' Play frequency for 70ms. '''
    # pitch(frequency, ms)
    music.pitch(frequency, 70)


def read_file(filename):
    with open(filename, 'r') as my_file:
        read_value = my_file.read()
        return read_value


def startup():
    ''' Display a pattern '''
    display.show(Image.YES)
    sleep(100)


def write_file(filename, value):
    with open(filename, 'w') as my_file:
        my_file.write(str(value))
        my_file.close()


def main():
    # startup()
    acc_list = initialise_list()
    radio.on()
    # initialise haptic feed control pin low
    pin2.write_digital(0)
    try:
        thresh = int(read_file(THRESHOLD_VALUE))
        print('threshold from file: {}'.format(thresh))
    except Exception as e:
        print('couldn\'t find threshold file: {} {}'.format(THRESHOLD_VALUE, e))
        thresh = THRESHOLD
        write_file(THRESHOLD_VALUE, THRESHOLD)
        print('created threshold file with value: {}'.format(THRESHOLD))
    while True:
        incoming = radio.receive()
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        acc = int((x**2 + y**2 + z**2)/ACC_DIVISOR)
        acc_list.pop(0)
        acc_list.append(acc)
        if average(acc_list) > thresh:
            detection()
            acc_list = initialise_list()
        if button_a.was_pressed() or incoming == 'decrease':
            thresh = (decrease_sensitivity(thresh, INCREMENT))
            write_file(THRESHOLD_VALUE, thresh)
            print('threshold: {}'.format(thresh))
        if button_b.was_pressed() or incoming == 'increase':
            thresh = (increase_sensitivity(thresh, INCREMENT))
            write_file(THRESHOLD_VALUE, thresh)
            print('threshold: {}'.format(thresh))
        display.show(leds_string2(acc, thresh))
        # There's a bug in the music library. The micro:bit freezes after a time.
        # Reset the board to compensate. Stopgap fix.
        if running_time() > TIMEOUT:
            reset()
        sleep(10)


main()
