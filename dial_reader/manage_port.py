import serial.tools.list_ports


def open_port(device_name):
    """Return serial port matching device name."""
    try:
        return serial.Serial(port=device_name, baudrate=9600, timeout=1)
    except serial.serialutil.SerialException:
        print('Device can not be found or can not be configured: ' + device_name)
        exit(1)
