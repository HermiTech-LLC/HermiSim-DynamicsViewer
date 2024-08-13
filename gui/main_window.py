from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QFileDialog, QMessageBox
from gui.tabs.render_tab import RenderTab
from gui.tabs.simulation_tab import SimulationTab
from gui.tabs.log_tab import LogTab
from gui.tabs.sensor_tab import SensorTab
from gui.file_loader import FileLoader
from physics_engine.simulation import Simulation
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robotics Simulation Suite")
        self.setGeometry(100, 100, 1200, 800)

        self.simulation = Simulation()
        self.file_loader = FileLoader(self.simulation)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.add_tabs()
        self.create_menu()

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def add_tabs(self):
        self.render_tab = RenderTab(self.simulation)
        self.simulation_tab = SimulationTab(self.simulation)
        self.log_tab = LogTab()
        self.sensor_tab = SensorTab(self.simulation)

        self.tab_widget.addTab(self.render_tab, "Render")
        self.tab_widget.addTab(self.simulation_tab, "Simulation")
        self.tab_widget.addTab(self.log_tab, "Logs")
        self.tab_widget.addTab(self.sensor_tab, "Sensors")

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        load_action = QAction('Load URDF/XML', self)
        load_action.triggered.connect(self.load_file)
        file_menu.addAction(load_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load URDF/XML File", "", "URDF Files (*.urdf);;XML Files (*.xml);;All Files (*)", options=options)
        if file_path:
            try:
                self.file_loader.load_file(file_path)
                self.logger.info(f"Loaded file: {file_path}")
                QMessageBox.information(self, "Success", f"Successfully loaded file: {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to load file: {file_path}, Error: {e}")
                QMessageBox.critical(self, "Error", f"Failed to load file: {e}")