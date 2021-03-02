# microbit hand_shake

This project enables people with physical disability to communicate through gesture using BBC microbits. One microbit is worn on the wrist (the transmitter) and a second is connected to a laptop or communications device (the receiver).

When a gesture is made, the motion is detected by the microbit on the wrist. This microbit uses its radio to signal the microbit connected to the laptop.

The microbit attached to the laptop then sends a trigger signal through the USB cable connected to the laptop. This signal is detected by a program running on the laptop which generates a simulated keystroke. This keystroke controls other software running on the laptop, such as communications software like Smartbox's Grid software.

More details and a video showing the systm in use are at:

<https://www.mattoppenheim.com/handshake/>

**Repository structure**

transmit: software for the transmitter microbit

receive: software for the receiver microbit

base: software to run on the laptop that the receiver is connected to

docs: photographs and files to generate this README and the setup instruction

## Project website

The project website has full details of what this project does and a video
showing it in use.

<https://seismicmatt.com/handshake/>

## Setup instructions

Instructions on how to set up the system are at:

<https://hardwaremonkey.github.io/microbit_hand_shake/>

This contains links to videos showing how to set up the system.

## Project testing

Testing the system by using a hand shake to operate an LED.
![testing](/docs/readme_docs/microbit_testing.jpg)

## micro:bit v1 and v2 compatibility

micro:bit v1 was used for testing. The hex files in this repository also work
on v2 of the micro:bit.
