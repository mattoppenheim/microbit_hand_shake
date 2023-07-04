""" Receives shake message from transmitter.
A relay on the board acts as a switch.
Relay is closed when pin2 goes high.
Relay is opened when pin2 goes low.
GPIO2 goes high then low when the message is received.
This is used to close then open a relay, which acts as a switch.
The buttons act to increase and decrease the shake detection threshold on the transmitter unit.
button a: makes board more sensitive, lower shake needed to activate.
button b: makes board less sensitive, harder shake needed to activate.
button a and button b: activates switch.
Threshold value stored in threshold_value.txt.
last update: 2023_06_28 Matthew Oppenheim
"""
from microbit import *
import radio

radio.config(address=0x101000, group=40, channel=2, data_rate=radio.RATE_1MBIT)
print("shake receive started")
display.show(Image.DIAMOND)
radio.on()


def decrease_sensitivity():
    """ Send message to decrease sensitivity. """
    display.show("-")
    radio.send("decrease")
    pause()


def increase_sensitivity():
    """ Send message to increase sensitivity. """
    display.show("+")
    radio.send("increase")
    pause()


def pause():
    """ Pause and clear display. """
    sleep(100)
    display.show(Image.DIAMOND)


def shake_detected():
    """ Display shake detection image, close and open switch. """
    pin2.write_digital(1)
    print("shake")
    display.show(Image.CHESSBOARD)
    pause()
    pin2.write_digital(0)


def update_status():
    ''' Update micro:bit status in main superloop. '''
    if (button_a.is_pressed() and button_b.is_pressed()):
        shake_detected()
        return
    if button_a.was_pressed():
        decrease_sensitivity()
        return
    if button_b.was_pressed():
        increase_sensitivity()
        return
    incoming = radio.receive()
    sleep(10)
    if incoming == "shake":
        shake_detected()

def main():
    # set the solid state relay open
    pin2.write_digital(0)
    while True:
        # helper function to enable testing
        update_status()


if __name__ == '__main__':
    main()
