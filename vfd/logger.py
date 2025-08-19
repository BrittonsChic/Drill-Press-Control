import pandas as pd
from datetime import datetime
import os
from .vfd_controller import VFDController
import time

class Logger:
    def __init__(self, vfd_controller: VFDController, base_path="/home/holesaw/vfd_logs", log_callback=None):
        self.vfd = vfd_controller
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)
        self.holesaw_name = None
        self.data = pd.DataFrame(columns=["Cycle", "Time", "Torque", "Voltage", "Current", "RPM"])
        self.cycle_count = 0
        self.in_cycle = False
        self.last_file = None
        self.log_callback = log_callback  # function provided by GUI to display logs

    def log_message(self, msg): # Works
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {msg}"
        print(full_msg)  # always print to console
        if self.log_callback:
            self.log_callback(full_msg)  # send to GUI log window

    def set_holesaw_name(self, name): #Works
        self.holesaw_name = name
        self.last_file = None
        self.log_message(f"Holesaw set to: {name}")

    def _generate_filename(self): 
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return os.path.join(self.base_path, f"vfd_cycles_{date_str}_{self.holesaw_name}.csv")

    def log_once(self):
        readings = self.vfd.read_all()
        if readings["torque_ratio"] is not None and readings["rpm"] is not None:
            now = datetime.now().strftime("%H:%M:%S")

            # Cycle start detection (>=200 rpm and torque > 1)
            if readings["torque_ratio"] > 1 and readings["rpm"] >= 200 and not self.in_cycle:
                self.cycle_count += 1
                self.in_cycle = True
                self.log_message(f"Cycle {self.cycle_count} started")

            # Cycle end detection
            elif readings["torque_ratio"] <= 1 and self.in_cycle:
                self.in_cycle = False
                self.log_message(f"Cycle {self.cycle_count} ended")
                self.save_to_file()

            # Log data row
            self.data.loc[len(self.data)] = [
                self.cycle_count, now,
                readings["torque_ratio"], readings["voltage"],
                readings["current"], readings["rpm"]
            ]

    def save_to_file(self):
        if not self.holesaw_name:
            self.log_message("⚠️ No holesaw name set. Skipping save.")
            return
        if not self.last_file:
            self.last_file = self._generate_filename()
        self.data.to_csv(self.last_file, index=False)
        self.log_message(f"Data saved to {self.last_file}")
        print(f"it worked")
    
    def start_stop(self, started: bool):
        if started:
            self.log_message("VFD started")
        else:
            self.log_message("VFD stopped")
