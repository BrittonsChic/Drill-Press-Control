# main.py

import sys
import sys
import os
from PyQt5.QtWidgets import QApplication
from vfd.rs485_base import Rs485Base
from vfd.vfd_controller import VFDController
from vfd.logger import Logger
from vfd.vfd_gui import VFDControlGUI


def main():
    # --- Step 1: Initialize RS485 connection ---
    rs485 = Rs485Base(
        baudrate=9600,
        bytesize=8,
        parity="N",
        stopbits=2,
        timeout=0.5,
    )

    # --- Step 2: Create the VFD controller object ---
    vfd = VFDController(rs485.client)

    # --- Step 3: Initialize Logger ---
    logger = Logger(vfd_controller=vfd)

    # --- Step 4: Create the Qt application ---
    app = QApplication(sys.argv)

    # --- Step 5: Create and show the GUI ---
    gui = VFDControlGUI(vfd_controller=vfd, logger=logger)
    gui.showFullScreen()

    # --- Step 6: Start event loop ---
    try:
        sys.exit(app.exec_())
    finally:
        # Clean shutdown
        rs485.close()


if __name__ == "__main__":
    main()
