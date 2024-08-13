from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtCore import QTimer

class SensorTab(QWidget):
    def __init__(self, simulation, parent=None):
        super(SensorTab, self).__init__(parent)
        self.simulation = simulation
        self.init_ui()
        self.init_timer()

    def init_ui(self):
        layout = QVBoxLayout()
        self.sensor_label = QLabel('Sensor Data')
        layout.addWidget(self.sensor_label)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Sensor', 'Value'])
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every second

    def update_data(self):
        self.table_widget.setRowCount(0)  # Clear existing data

        sensor_data = self.simulation.get_sensor_data()
        for i, (sensor, value) in enumerate(sensor_data.items()):
            self.table_widget.insertRow(i)
            self.table_widget.setItem(i, 0, QTableWidgetItem(sensor))
            self.table_widget.setItem(i, 1, QTableWidgetItem(str(value)))
