# rs485_base.py
from pymodbus.client import ModbusSerialClient
from pymodbus import FramerType

class Rs485Base:
    def __init__(self, **kwargs):
        self.client = ModbusSerialClient(
            framer=FramerType.RTU,
            port="/dev/ttyCH343USB1",
            baudrate=kwargs.get("baudrate", 9600),
            bytesize=kwargs.get("bytesize", 8),
            parity=kwargs.get("parity", "N"),
            stopbits=kwargs.get("stopbits", 2),
            timeout=kwargs.get("timeout", 0.5)
        )
        self.client.connect()

    def close(self):
        self.client.close()
