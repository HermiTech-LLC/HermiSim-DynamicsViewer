import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction, QFileDialog, QMessageBox
from gui.styles import apply_styles
from gui.tabs.render_tab import RenderTab
from gui.tabs.simulation_tab import SimulationTab
from gui.tabs.log_tab import LogTab
from gui.tabs.sensor_tab import SensorTab
from gui.simulation_controls import SimulationControls
from gui.object_renderer import ObjectRenderer
from gui.file_loader import FileLoader
from gui.sensor_data_viewer import SensorDataViewer
from physics_engine.engine import PhysicsEngine
from physics_engine.sensor import Sensor
from physics_engine.simulation import Simulation
import logging
import subprocess  # For launching the URDF design tool
import os  # For working with file paths

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HermiSim Simulation Suite")
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

        urdf_design_action = QAction('Launch URDF Design Tool', self)  # New Action for URDF Design
        urdf_design_action.triggered.connect(self.launch_urdf_design_tool)
        file_menu.addAction(urdf_design_action)  # Add it to the File menu

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

    def launch_urdf_design_tool(self):
        """Launch the URDF design tool as a separate process."""
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'utils', 'urdf.py')
            subprocess.Popen([sys.executable, script_path])
        except Exception as e:
            self.logger.error(f"Failed to launch URDF design tool: {e}")
            QMessageBox.critical(self, "Error", f"Failed to launch URDF design tool: {e}")

def initialize_tabs(simulation):
    """Initialize and return the tabs for the main window."""
    render_tab = RenderTab(simulation)
    simulation_tab = SimulationTab(simulation)
    log_tab = LogTab()
    sensor_tab = SensorTab(simulation)
    return render_tab, simulation_tab, log_tab, sensor_tab

def initialize_components():
    """Initialize and return the main components of the application."""
    simulation = Simulation()
    simulation_controls = SimulationControls(simulation)
    object_renderer = ObjectRenderer(simulation)
    file_loader = FileLoader(simulation)
    sensor_data_viewer = SensorDataViewer()
    engine = PhysicsEngine()
    sensor = Sensor()
    return simulation_controls, object_renderer, file_loader, sensor_data_viewer, engine, sensor, simulation

def configure_simulation(file_loader, simulation, engine, sensor):
    """Configure the simulation with initial data and engine settings."""
    try:
        initial_data = file_loader.load_initial_data()
        simulation.load_robot(initial_data.get('robot_urdf', 'r2d2.urdf'))
        engine.connect()
        engine.set_simulation(simulation)
        engine.set_sensor(sensor)
    except Exception as e:
        print(f"Error configuring simulation: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    app = QApplication(sys.argv)
    apply_styles(app)
    
    main_window = MainWindow()
    
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
