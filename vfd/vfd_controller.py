from .rs485_base import Rs485Base
from pymodbus.client import ModbusSerialClient

class VFDController:
    CURRENT_REG = 0x2104
    VOLTAGE_REG = 0x2106
    TORQUE_REG = 0x210B
    RPM_REG = 0x210C
    CMD_REG = 0x2000
    FREQ_SET_REG = 0x2001

    SCALE_FACTOR = 10
    MAX_FREQ = 68.06  # Hz

    def __init__(self, client: ModbusSerialClient):
        self.client = client

    def read_current(self) -> float | None:
        value = self.client.read_holding_registers(self.CURRENT_REG)
        return (value.registers[0] / self.SCALE_FACTOR) if value else None

    def read_voltage(self) -> float | None:
        value = self.client.read_holding_registers(self.VOLTAGE_REG)
        return (value.registers[0] / self.SCALE_FACTOR) if value is not None else None

    def read_torque_ratio(self) -> float | None:
        value = self.client.read_holding_registers(self.TORQUE_REG)
        return (value.registers[0] / self.SCALE_FACTOR) if value is not None else None

    def read_rpm(self) -> float | None:
        value =  self.client.read_holding_registers(self.RPM_REG)
        return round((value.registers[0]/9.740550769),2) if value else None

    def read_all(self):
        return {
            "current": self.read_current(),
            "voltage": self.read_voltage(),
            "torque_ratio": self.read_torque_ratio(),
            "rpm": self.read_rpm()
        }

    def set_frequency(self, hz):
        self.client.write_register(0x2001, hz)
        print(f"Set frequency to {hz/100} Hz")

    def start(self):
        self.client.write_register(0x2000, 0x0012)
        print("VFD started")

    def stop(self):
        self.client.write_register(0x2000, 0x0001)
        print("VFD stopped")
