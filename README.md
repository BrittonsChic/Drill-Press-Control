# Drill Press VFD Control GUI

This project provides a **PyQt5-based GUI** for controlling a Delta VFD-B (VFD015B21A) variable frequency drive over **RS-485**.  
It allows you to:

- Start/Stop the spindle.
- Set spindle speed (RPM → converted to frequency).
- Monitor real-time values (RPM, torque, current, voltage).
- Log cycles to CSV using `pandas`.

---

## 📂 Project Structure

```
vfd_project/
│── main.py                 # Entry point of the program
│
├── vfd/
│   ├── rs485_base.py       # RS485 connection wrapper using pymodbus
│   ├── vfd_controller.py   # VFD-specific commands (start, stop, set speed, read values)
│   ├── vfd_gui.py          # PyQt5 GUI interface
│   ├── logger.py           # Cycle logging (CSV/Pandas)
│
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

---

## ⚙️ Installation

### 1. Clone or copy the project into your home directory:
```bash
cd ~
git clone https://github.com/your-repo/vfd_project.git
cd vfd_project
```

### 2. Install dependencies (system-wide with `--break-system-packages` if needed):
```bash
pip install -r requirements.txt --break-system-packages
```

### 3. Requirements include:
- `pymodbus` (RS-485 communication)
- `pyserial`
- `PyQt5`
- `pandas`

---

## ▶️ Running the Program

From the project root:
```bash
cd ~/vfd_project
python main.py
```

The GUI should launch in **fullscreen kiosk mode** on the reTerminal DM.  
- **Start** button → Sends VFD "Run" command.  
- **Stop** button → Sends VFD "Stop" command.  
- **Speed control** → Adjusts spindle RPM.  
- **Status fields** → Show real-time feedback (RPM, torque, etc.).  
- **Name** -> Enter name for file save
- **Enter** -> Closes entry in text box

---

## 🔧 Configuration

### RS-485 Settings
Default RS-485 config (in `main.py`):
```python
rs485 = Rs485Base(
    baudrate=9600,
    bytesize=8,
    parity="N",
    stopbits=2,
    timeout=0.5,
    framer="rtu",
    slave_id=1
)
```
Update these if your VFD uses different serial parameters.

### VFD Registers
- **Start/Stop** → Register `0x2000`
- **Frequency Command** → Register `0x2001`
- **Feedback (RPM, torque, current, voltage)** → Read from `0x2100` and above (see Delta VFD-B Modbus manual).

---

## 📝 Logging

Cycles are logged automatically once:
- Spindle speed ≥ 200 RPM  
- Torque ratio ≥ 1  

Logs are saved in timestamped and named files CSV files inside `~/vfd_project/logs/`.

---

## Drive Parameters

Parameters may need adjusted for control and communication over RS485. Currently this is on a Jet drill press and the max frequency is set to 70Hz with the program only going to 68 Hz as the max. Otherwise, the drive was factory reset and then adjusted to make it work the way it was needed. Refer to https://deltaacdrives.com/Delta-VFD-E-User-Manual.pdf for this drive to determine how parameters need to be set. 

## 🚀 Next Steps
- Add configurable refresh rate for display updates.
- Add error handling for Modbus timeouts.
- Implement config file (`config.json`) for RS485 and register mappings.
- Detrermine how parameters should be set in order to drive Z-Axis feed
- Torque should be the parameter used to determine the feed rate and be the multiplier for feed
- Allows for use of basic stepper motor drive with control from a raspberry pi with futher programming 
