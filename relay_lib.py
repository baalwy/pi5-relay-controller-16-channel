"""A module for interacting with the ELEGOO 16 Channel board for the Raspberry Pi."""
# =========================================================
# Raspberry Pi Relay Board Library
#
# by John M. Wargo (www.johnwargo.com)
# https://gpiozero.readthedocs.io/en/stable/
#
# by G. Shaughnessy
# =========================================================
from __future__ import print_function

import gpiod


# The number of relay ports on the relay board is now 16
NUM_RELAY_PORTS = 16
RELAY_PORTS = []
RELAY_STATUS = NUM_RELAY_PORTS * [0]

# عكس القيم للتشغيل والإيقاف 
ON_STATE = 0
OFF_STATE = 1

# إعداد الجلسة
CHIP = 'gpiochip0'
chip = gpiod.Chip(CHIP)

def init_relay(port_list):
    """Initialize the module

    Args:
        port_list: A list containing the relay port assignments
    """
    global RELAY_PORTS
    print("\nInitializing relay")
    # Get the relay port list from the main application
    # assign the local variable with the value passed into init
    RELAY_PORTS = port_list
    print("Relay port list:", RELAY_PORTS)
    return len(RELAY_PORTS) == NUM_RELAY_PORTS

def relay_on(relay_num):
    """Turn the specified relay (by relay #) on."""
    if isinstance(relay_num, int) and 0 < relay_num <= NUM_RELAY_PORTS:
        print('Turning relay', relay_num, 'ON')
        line = chip.get_line(RELAY_PORTS[relay_num - 1])
        
        # تحرير المنفذ إذا كان محجوزًا بالفعل
        if line.is_requested():
            line.release()
        
        # طلب التحكم بالمنفذ وتشغيل الريلي
        line.request(consumer="Relay Control", type=gpiod.LINE_REQ_DIR_OUT)
        line.set_value(ON_STATE)
        RELAY_STATUS[relay_num - 1] = 1


def relay_off(relay_num):
    """Turn the specified relay (by relay #) off."""
    if isinstance(relay_num, int) and 0 < relay_num <= NUM_RELAY_PORTS:
        print('Turning relay', relay_num, 'OFF')
        line = chip.get_line(RELAY_PORTS[relay_num - 1])
        
        # تحرير المنفذ إذا كان محجوزًا بالفعل
        if line.is_requested():
            line.release()
        
        # طلب التحكم بالمنفذ وإيقاف الريلي
        line.request(consumer="Relay Control", type=gpiod.LINE_REQ_DIR_OUT)
        line.set_value(OFF_STATE)
        RELAY_STATUS[relay_num - 1] = 0


def relay_all_on():
    """Turn all relays on."""
    print('Turning all relays ON')
    for pin in RELAY_PORTS:
        line = chip.get_line(pin)
        if line.is_requested():
            line.release()  # تحرير المنفذ في حال كان مستخدمًا
        line.request(consumer="Relay Control", type=gpiod.LINE_REQ_DIR_OUT)
        line.set_value(ON_STATE)
    for i in range(NUM_RELAY_PORTS):
        RELAY_STATUS[i] = 1



def relay_all_off():
    """Turn all relays off."""
    print('Turning all relays OFF')
    for pin in RELAY_PORTS:
        line = chip.get_line(pin)
        if line.is_requested():
            line.release()  # تحرير المنفذ إذا كان محجوزًا
        line.request(consumer="Relay Control", type=gpiod.LINE_REQ_DIR_OUT)
        line.set_value(OFF_STATE)
    for i in range(NUM_RELAY_PORTS):
        RELAY_STATUS[i] = 0


def relay_toggle_port(relay_num):
    """Toggle the specified relay (on to off, or off to on).

    Call this function to toggle the status of a specific relay.

    Args:
        relay_num (int): The relay number to toggle.
    """
    print('Toggling relay:', relay_num)
    if relay_get_port_status(relay_num):
        # إذا كان الريلي في وضع التشغيل، قم بإيقافه
        relay_off(relay_num)
    else:
        # إذا كان الريلي في وضع الإيقاف، قم بتشغيله
        relay_on(relay_num)



def relay_get_port_status(relay_num):
    """Returns the status of the specified relay (True for on, False for off)

    Call this function to retrieve the status of a specific relay.

    Args:
        relay_num (int): The relay number to query.
    """
    # يحدد ما إذا كان الريلي المحدد في وضع التشغيل أو الإيقاف
    print('Checking status of relay', relay_num)
    return RELAY_STATUS[relay_num - 1] == ON_STATE
