from PyQt5.QtWidgets import QWidget, QVBoxLayout
from gui.simulation_controls import SimulationControls

class SimulationTab(QWidget):
    def __init__(self, simulation):
        super().__init__()
        self.simulation = simulation
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.controls = SimulationControls(self.simulation)
        layout.addWidget(self.controls)

        self.setLayout(layout)