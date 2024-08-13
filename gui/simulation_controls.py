from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSlider, QGridLayout
from PyQt5.QtCore import Qt

class SimulationControls(QWidget):
    def __init__(self, simulation):
        super().__init__()
        self.simulation = simulation
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        self.start_button = QPushButton('Start Simulation')
        self.start_button.clicked.connect(self.simulation.start)
        layout.addWidget(self.start_button, 0, 0)

        self.stop_button = QPushButton('Stop Simulation')
        self.stop_button.clicked.connect(self.simulation.stop)
        layout.addWidget(self.stop_button, 0, 1)

        self.reset_button = QPushButton('Reset Simulation')
        self.reset_button.clicked.connect(self.simulation.reset)
        layout.addWidget(self.reset_button, 0, 2)

        self.speed_label = QLabel('Simulation Speed:')
        layout.addWidget(self.speed_label, 1, 0, 1, 2)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)
        self.speed_slider.valueChanged.connect(self.update_speed)
        layout.addWidget(self.speed_slider, 2, 0, 1, 3)

        self.speed_value_label = QLabel('50')
        layout.addWidget(self.speed_value_label, 1, 2)

        self.setLayout(layout)

    def update_speed(self):
        speed = self.speed_slider.value()
        self.simulation.set_speed(speed)
        self.speed_value_label.setText(str(speed))