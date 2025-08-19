from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from .vfd_controller import VFDController
from .logger import Logger


class VFDControlGUI(QWidget):
    def __init__(self, vfd_controller: VFDController, logger: Logger):
        super().__init__()
        self.vfd = vfd_controller
        self.logger = logger
        self.running = False
        self.init_ui()
        self.logger.log_callback = self.log_to_window

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_display)
        self.timer.start(200)  # Refresh every second

    def update_running_state(self):
        torqueRatio = self.vfd.read_torque_ratio()
        rpm = self.vfd.read_rpm()
        voltage = self.vfd.read_voltage()
        current = self.vfd.read_current()
        if torqueRatio is None or rpm is None:
            self.logger.log_message("Error reading VFD data")
            self.running = False
            return False
        if torqueRatio > 1 and rpm >=200:
            self.running = True
            self.logger.log_message(f"Torque Ratio: {torqueRatio}, RPM: {rpm}, Voltage: {voltage}, Current: {current}")
            name = self.holesaw_input.text()
            self.logger.set_holesaw_name
            self.logger.set_holesaw_name(name)
            return True
        else:
            self.running = False
            self.logger._generate_filename
            self.logger.save_to_file
            return False

    def init_ui(self):
        layout = QVBoxLayout()

        # Hole saw name input
        self.holesaw_input = QLineEdit(self)
        self.holesaw_input.setPlaceholderText("Enter hole saw name")
        layout.addWidget(self.holesaw_input)

        # Data displays
        # Data displays (centered)
        self.rpm_label = QLabel("RPM: 0")
        self.rpm_label.setAlignment(Qt.AlignCenter)
        self.rpm_label.setStyleSheet("""
            QLabel {
            border: 2px solid #333;
            border-radius: 10px;
            padding: 12px;
            font-size: 28px;
            background-color: #fff;
            }
        """)

        self.current_label = QLabel(f"Current: {self.vfd.read_current()} A")
        self.current_label.setAlignment(Qt.AlignCenter)
        self.voltage_label = QLabel("Voltage: 0.0 V")
        self.voltage_label.setAlignment(Qt.AlignCenter)
        self.torque_label = QLabel("Torque Ratio: 0.0")
        self.torque_label.setAlignment(Qt.AlignCenter)
        self.speed_percent_label = QLabel("Speed: 0%")
        self.speed_percent_label.setAlignment(Qt.AlignCenter)
        self.count_label = QLabel("Cycle Count: 0")
        self.count_label.setAlignment(Qt.AlignCenter)

        for label in [self.rpm_label, self.current_label, self.voltage_label, self.torque_label, self.speed_percent_label, self.count_label]:
            layout.addWidget(label, alignment=Qt.AlignHCenter)

        # Store default and green styles for RPM label
        self.rpm_default_style = """
            QLabel {
            border: 2px solid #333;
            border-radius: 10px;
            padding: 12px;
            font-size: 28px;
            background-color: #fff;
            }
        """
        self.rpm_green_style = """
            QLabel {
            border: 2px solid #333;
            border-radius: 10px;
            padding: 12px;
            font-size: 28px;
            background-color: #4CAF50;
            color: #fff;
            }
        """

        # Slider for speed
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(100)
        self.speed_slider.setFixedHeight(40)  # Make the slider taller
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
            height: 16px;
            background: #bbb;
            border-radius: 8px;
            }
            QSlider::handle:horizontal {
            background: #388E3C;
            border: 2px solid #1B5E20;
            width: 32px;
            height: 32px;
            margin: -8px 0;
            border-radius: 16px;
            }
        """)
        self.speed_slider.sliderReleased.connect(self.update_speed)
        self.update_speed()
        layout.addWidget(self.speed_slider)

        # Control buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.setFixedHeight(80)
        self.start_btn.setFixedWidth(375)
        self.start_btn.setStyleSheet("""
            QPushButton {
            background-color: green;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            }
            QPushButton:pressed {
            background-color: #006400;
            }
        """)
        self.start_btn.clicked.connect(self.vfd.start)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFixedHeight(80)
        self.stop_btn.setFixedWidth(375)
        self.stop_btn.setStyleSheet("""
            QPushButton {
            background-color: red;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            }
            QPushButton:pressed {
            background-color: #8B0000;
            }
        """)
        self.stop_btn.clicked.connect(self.vfd.stop)

        self.reset_btn = QPushButton("Reset Cycle")
        self.reset_btn.setFixedHeight(80)
        self.reset_btn.setFixedWidth(375)
        self.reset_btn.setStyleSheet("""
            QPushButton {
            background-color: yellow;
            color: black;
            font-size: 18px;
            border-radius: 8px;
            }
            QPushButton:pressed {
            background-color: #CCCC00;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_cycle)
        for btn in [self.start_btn, self.stop_btn, self.reset_btn]:
            button_layout.addWidget(btn)
        layout.addLayout(button_layout)

        # Log window
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        self.log_window.setFixedHeight(400)  # Set a smaller height for the log window
        layout.addWidget(self.log_window)

        self.setLayout(layout)

    def update_speed(self):
        percent = self.speed_slider.value()
        self.speed_percent_label.setText(f"Speed: {percent}%")
        frequency = int(percent * self.vfd.MAX_FREQ)
        self.vfd.set_frequency(frequency)
        

    def reset_cycle(self):
        name = self.holesaw_input.text()
        if name:
            self.logger.set_holesaw_name(name)
            self.logger.cycle_count = 0
            self.logger.data = self.logger.data.iloc[0:0]  # Clear table
            self.log_window.append("Cycle reset")

    def refresh_display(self):
        readings = self.vfd.read_all()
        if self.update_running_state(): 
            self.logger.log_once()  # Log data once per refresh
            print("Sent to log")
        if readings:
            self.rpm_label.setText(f"RPM: {readings['rpm']}")
            self.current_label.setText(f"Current: {readings['current']} A")
            self.voltage_label.setText(f"Voltage: {readings['voltage']} V")
            self.torque_label.setText(f"Torque Ratio: {readings['torque_ratio']}")
            self.count_label.setText(f"Cycle Count: {self.logger.cycle_count}")

    def log_to_window(self, msg):
        self.log_window.append(msg)
