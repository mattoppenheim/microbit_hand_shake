""" receive shake and write to serial port
update shake threshold to shake_detector """

from microbit import *

radio.config(address=0x101000, group=40, channel=2, data_rate=radio.RATE_1MBIT)
print("shake receive started")
display.show(Image.DIAMOND)
radio.on()


def decrease_sensitivity():
    """ send message to decrease sensitivity """
    display.show("-")
    radio.send("decrease")
    pause()


def increase_sensitivity():
    """ send message to increase sensitivity """
    display.show("+")
    radio.send("increase")
    pause()


def pause():
    """ pause and clear display """
    sleep(100)
    display.show(Image.DIAMOND)


def shake_detected():
    print("shake")
    display.show(Image.CHESSBOARD)
    pause()


def update_status():
    ''' Update micro:bit status in main superloop. '''
    if button_a.was_pressed():
        decrease_sensitivity()
    if button_b.was_pressed():
        increase_sensitivity()
    incoming = radio.receive()
    sleep(10)
    if incoming == "shake":
        shake_detected()

def main():
    while True:
        # helper function to enable testing
        update_status()


if __name__ == '__main__':
    main()