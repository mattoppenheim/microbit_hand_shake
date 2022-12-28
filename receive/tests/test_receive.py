''' Tests for receive.py.
These tests run under Python, not micropython, using pytest.
microbit module functions are mocked in mock_microbit.py.
Matt Oppenheim Dec 2022. 
'''

import sys
sys.modules['microbit'] = __import__('mock_microbit')
from unittest.mock import Mock, Mock
from receive import * 
from unittest.mock import patch


def setup(mocker):
    ''' Setup global mocks and patches.'''
    global mock_show, mock_send, mock_pause, mock_sleep

    mock_show = mocker.Mock(name='show')
    mocker.patch('receive.display.show', new=mock_show)

    mock_send = mocker.Mock(name='send')
    mocker.patch('receive.radio.send', new=mock_send)
    
    mock_pause = mocker.Mock(name='pause')
    mocker.patch('receive.pause', new=mock_pause)
    
    mock_sleep = mocker.Mock(name='sleep')
    mocker.patch('receive.sleep', new=mock_sleep)


def test_decrease_sensitivity(mocker):
    # arrange
    # mocked dependencies
    setup(mocker)

    # act
    decrease_sensitivity()

    # assert
    mock_show.assert_called_with('-')
    mock_send.assert_called()
    mock_send.assert_called_with('decrease')
    mock_pause.assert_called()


def test_increase_sensitivity(mocker):
    setup(mocker)
    increase_sensitivity()
    mock_show.assert_called_with('+')
    mock_send.assert_called()
    mock_send.assert_called_with('increase')
    mock_pause.assert_called()


def test_pause(mocker):
    setup(mocker)
    pause()
    mock_sleep.assert_called_with(100)
    mock_show.assert_called_with(Image.DIAMOND)


def test_shake_detected(mocker, capfd):
    setup(mocker)
    shake_detected()
    out, err = capfd.readouterr()
    assert out == 'shake\n'
    mock_show.assert_called_with(Image.CHESSBOARD)
    mock_pause.assert_called()


def test_update_status_a(mocker):
    ''' Test button a. '''
# mocked dependencies
    mocker.patch.object(button_a, 'was_pressed') 
    button_a.was_pressed.return_value = True
    
    mock_decrease_sensitivity = mocker.Mock(name='decrease_sensitivity')
    mocker.patch('receive.decrease_sensitivity', new=mock_decrease_sensitivity)

    mock_increase_sensitivity = mocker.Mock(name='increase_sensitivity')
    #mocker.patch('receive.increase_sensitivity', new=mock_increase_sensitivity)

    update_status()

    mock_decrease_sensitivity.assert_called()
    mock_increase_sensitivity.assert_not_called()


def test_update_status_b(mocker):
    ''' Test button_b. '''
    mocker.patch.object(button_b, 'was_pressed') 
    button_b.was_pressed.return_value = True
    
    mock_increase_sensitivity = Mock(name='increase_sensitivity')
    mocker.patch('receive.increase_sensitivity', new=mock_increase_sensitivity)

    mock_decrease_sensitivity = mocker.Mock(name='decrease_sensitivity')

    update_status()

    mock_decrease_sensitivity.assert_not_called()
    mock_increase_sensitivity.assert_called()


def test_update_status_shake(mocker):
    ''' Test incoming = 'shake'. '''
    mock_receive = mocker.Mock(name='receive')
    mocker.patch('receive.radio.receive', new=mock_receive)
    mock_receive.return_value = 'shake'

    mock_shake_detected = mocker.Mock(name='shake_detected')
    mocker.patch('receive.shake_detected', new=mock_shake_detected)
    
    update_status()

    mock_shake_detected.assert_called()


def test_update_status_incoming(mocker):
    ''' Test radio.receive() called. '''
    mock_receive = mocker.Mock(name='receive')
    mocker.patch('receive.radio.receive', new=mock_receive)

    update_status()

    mock_receive.assert_called()


def test_update_status_sleep(mocker):
    setup(mocker)
    update_status()
    mock_sleep.assert_called_with(10)