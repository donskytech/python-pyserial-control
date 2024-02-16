import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QDial,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
    QHBoxLayout
)
import serial 
import time

WINDOW_SIZE = 350
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40
ERROR_MSG = "ERROR"


class ArduinoModel:
    """Model class representing the Arduino-related data and logic."""

    def __init__(self):
        self.led_state = False  # Initial state: LED is off
        self.rgb_led_color = None  # Initial state: RGB LED color is not selected
        self.servo_position = 0  # Initial state: Servo position is 0

    def toggle_led(self):
        self.led_state = not self.led_state

    def set_rgb_led_color(self, color):
        self.rgb_led_color = color

    def set_servo_position(self, position):
        self.servo_position = position

    def get_led_status(self):
        return self.led_state


class ArduinoController:
    """Controller class handling user input and updating the model."""

    def __init__(self, model):
        self.model = model
        self.serial_connection = serial.Serial('COM3', 9600)

    def handle_led_button_click(self):
        self.model.toggle_led()
        led_data = f"LED-{self.model.get_led_status()}\n"
        print(f"Toggle LED, message : {led_data}")
        self.send_serial_message(led_data)

    def handle_rgb_led_color_change(self, color):
        print(f"RGB LED Color : {color}")
        self.model.set_rgb_led_color(color)
        # Red = 1, Green = 2, Blue = 3
        color_data = None
        if (color == "Red"):
            color_data = f"RGB-1\n"
        elif(color == "Green"):
            color_data = f"RGB-2\n"
        else:
            color_data = f"RGB-3\n"
        print(f"Sending serial command : {color_data}")
        self.send_serial_message(color_data)

    def handle_servo_position_change(self, position):
        servo_data = f"SERVO-{position}\n"
        self.model.set_servo_position(position)
        print(f"Servo Position : {servo_data}")
        self.send_serial_message(servo_data)
        time.sleep(0.3)

    def send_serial_message(self, message):
        self.serial_connection.write(message.encode())
        


class PyControllerWindow(QMainWindow):
    """View class representing the user interface."""

    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle("Arduino Control")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.controller = controller
        self._create_ui_display()

    def _create_ui_display(self):
        site_label = QLabel("www.donskytech.com")
        site_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        site_label.setStyleSheet("font-size: 20px; color: blue;")

        self.layout.addWidget(site_label)

        # Group Box for LED-related widgets
        led_group = QGroupBox("LED Control")
        led_layout = QVBoxLayout()

        led_label = QLabel("Turn On LED")
        led_button = QPushButton("Toggle LED")
        led_button.clicked.connect(self.controller.handle_led_button_click)

        led_layout.addWidget(led_label)
        led_layout.addWidget(led_button)

        led_group.setLayout(led_layout)
        self.layout.addWidget(led_group)

        # Create a button group for RGB LED
        radio_group = QGroupBox("RGB LED Control")
        radio_layout = QHBoxLayout()

        red = QRadioButton("Red", self)
        green = QRadioButton("Green", self)
        blue = QRadioButton("Blue", self)

        rgb_button_group = QButtonGroup(self)
        rgb_button_group.addButton(red)
        rgb_button_group.addButton(green)
        rgb_button_group.addButton(blue)
        rgb_button_group.buttonClicked.connect(self.handle_rgb_led_color_change)

        radio_layout.addWidget(red)
        radio_layout.addWidget(green)
        radio_layout.addWidget(blue)

        radio_group.setLayout(radio_layout)
        self.layout.addWidget(radio_group)

        # Group Box for Servo-related widgets
        servo_group = QGroupBox("Servo Control")
        servo_layout = QVBoxLayout()

        servo_label = QLabel("Set servo position")
        servo_dial = QDial()
        servo_dial.setMinimum(0)
        servo_dial.setMaximum(180)
        servo_dial.valueChanged.connect(self.handle_servo_position_change)

        servo_layout.addWidget(servo_label)
        servo_layout.addWidget(servo_dial)

        servo_group.setLayout(servo_layout)
        self.layout.addWidget(servo_group)

    def handle_rgb_led_color_change(self, button):
        color = button.text()
        self.controller.handle_rgb_led_color_change(color)

    def handle_servo_position_change(self, position):
        self.controller.handle_servo_position_change(position)


def main():
    model = ArduinoModel()
    controller = ArduinoController(model)
    controllerApp = QApplication([])
    controllerWindow = PyControllerWindow(controller)
    controllerWindow.show()
    sys.exit(controllerApp.exec())

if __name__ == "__main__":
    main()
