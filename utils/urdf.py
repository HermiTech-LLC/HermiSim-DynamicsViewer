import sys
import pybullet as p
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from robodk import robolink, robomath

class URDFGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.robodk = robolink.Robolink()
        self.robot_item = None
        self.physics_client = None

    def initUI(self):
        self.setWindowTitle('Comprehensive URDF Generator with Real-Time Preview')
        self.setGeometry(100, 100, 1200, 600)

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Horizontal layout for the main interface and PyBullet view
        content_layout = QHBoxLayout()

        # Interface Layout
        interface_layout = QVBoxLayout()
        content_layout.addLayout(interface_layout)

        # Load Robot button
        self.btn_load_robot = QPushButton('Load Robot', self)
        self.btn_load_robot.clicked.connect(self.load_robot)
        interface_layout.addWidget(self.btn_load_robot)

        # Tab widget to organize sections
        self.tab_widget = QTabWidget(self)
        interface_layout.addWidget(self.tab_widget)

        # Robot Properties tab
        self.tab_properties = QWidget()
        self.tab_widget.addTab(self.tab_properties, "Robot Properties")
        self.initPropertiesTab()

        # Links tab
        self.tab_links = QWidget()
        self.tab_widget.addTab(self.tab_links, "Links")
        self.initLinksTab()

        # Joints tab
        self.tab_joints = QWidget()
        self.tab_widget.addTab(self.tab_joints, "Joints")
        self.initJointsTab()

        # Sensors tab
        self.tab_sensors = QWidget()
        self.tab_widget.addTab(self.tab_sensors, "Sensors")
        self.initSensorsTab()

        # Horizontal layout for Save and Generate buttons
        button_layout = QHBoxLayout()

        self.btn_save = QPushButton('Save URDF', self)
        self.btn_save.clicked.connect(self.save_urdf)
        self.btn_save.setEnabled(False)  # Disabled until a robot is loaded
        button_layout.addWidget(self.btn_save)

        self.btn_generate = QPushButton('Generate URDF', self)
        self.btn_generate.clicked.connect(self.generate_urdf)
        self.btn_generate.setEnabled(False)  # Disabled until a robot is loaded
        button_layout.addWidget(self.btn_generate)

        interface_layout.addLayout(button_layout)

        # PyBullet View
        self.pybullet_widget = QLabel("PyBullet Side View", self)
        self.pybullet_widget.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.pybullet_widget, 1)

        main_layout.addLayout(content_layout)

        # Initialize PyBullet
        self.init_pybullet()

        # Timer to update PyBullet view
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pybullet_view)
        self.timer.start(100)  # Update every 100 ms

    def initPropertiesTab(self):
        layout = QVBoxLayout(self.tab_properties)

        self.label_name = QLabel('Robot Name:', self)
        layout.addWidget(self.label_name)
        self.input_name = QLineEdit(self)
        layout.addWidget(self.input_name)

        self.label_version = QLabel('Version:', self)
        layout.addWidget(self.label_version)
        self.input_version = QLineEdit(self)
        layout.addWidget(self.input_version)

        self.label_manufacturer = QLabel('Manufacturer:', self)
        layout.addWidget(self.label_manufacturer)
        self.input_manufacturer = QLineEdit(self)
        layout.addWidget(self.input_manufacturer)

        self.label_description = QLabel('Description:', self)
        layout.addWidget(self.label_description)
        self.input_description = QTextEdit(self)
        layout.addWidget(self.input_description)

    def initLinksTab(self):
        layout = QVBoxLayout(self.tab_links)

        self.links_table = QTableWidget(self)
        self.links_table.setColumnCount(3)
        self.links_table.setHorizontalHeaderLabels(['Link Name', 'Mass (kg)', 'Visual'])
        self.links_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.links_table)

        self.btn_add_link = QPushButton('Add Link', self)
        self.btn_add_link.clicked.connect(self.add_link)
        layout.addWidget(self.btn_add_link)

    def initJointsTab(self):
        layout = QVBoxLayout(self.tab_joints)

        self.joints_table = QTableWidget(self)
        self.joints_table.setColumnCount(4)
        self.joints_table.setHorizontalHeaderLabels(['Joint Name', 'Type', 'Parent Link', 'Child Link'])
        self.joints_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.joints_table)

        self.btn_add_joint = QPushButton('Add Joint', self)
        self.btn_add_joint.clicked.connect(self.add_joint)
        layout.addWidget(self.btn_add_joint)

    def initSensorsTab(self):
        layout = QVBoxLayout(self.tab_sensors)

        self.sensors_table = QTableWidget(self)
        self.sensors_table.setColumnCount(3)
        self.sensors_table.setHorizontalHeaderLabels(['Sensor Name', 'Type', 'Attached to Link'])
        self.sensors_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.sensors_table)

        self.btn_add_sensor = QPushButton('Add Sensor', self)
        self.btn_add_sensor.clicked.connect(self.add_sensor)
        layout.addWidget(self.btn_add_sensor)

    def init_pybullet(self):
        self.physics_client = p.connect(p.DIRECT)  # Use DIRECT mode for headless rendering
        p.setGravity(0, 0, -9.81, physicsClientId=self.physics_client)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0, physicsClientId=self.physics_client)

    def update_pybullet_view(self):
        if self.robot_item is not None and self.robot_item.Valid():
            self.refresh_pybullet_view()

    def refresh_pybullet_view(self):
        p.resetSimulation(physicsClientId=self.physics_client)
        urdf_data = self.robot_item.ExportURDFString()
        robot_id = p.loadURDF(urdf_data, physicsClientId=self.physics_client)
        p.resetBasePositionAndOrientation(robot_id, [0, 0, 0], p.getQuaternionFromEuler([0, 0, 0]), physicsClientId=self.physics_client)

        # Render side view
        width, height, rgb_img, depth_img, seg_img = p.getCameraImage(
            640, 480,
            viewMatrix=p.computeViewMatrixFromYawPitchRoll(cameraTargetPosition=[0, 0, 0], distance=2, yaw=90, pitch=-15, roll=0, upAxisIndex=2),
            projectionMatrix=p.computeProjectionMatrixFOV(fov=60, aspect=1.0, nearVal=0.1, farVal=100.0),
            physicsClientId=self.physics_client
        )
        self.display_image(rgb_img)

    def display_image(self, img):
        # Convert the image data for displaying in the PyQt label
        img = img[:, :, :3]  # Remove alpha channel
        img = img.astype('uint8')
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        qt_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.pybullet_widget.setPixmap(QPixmap.fromImage(qt_image))

    def add_link(self):
        row_count = self.links_table.rowCount()
        self.links_table.insertRow(row_count)
        self.links_table.setItem(row_count, 0, QTableWidgetItem(f'Link_{row_count+1}'))
        self.links_table.setItem(row_count, 1, QTableWidgetItem('1.0'))  # Default mass
        self.links_table.setItem(row_count, 2, QTableWidgetItem('box'))  # Default visual shape
        self.refresh_pybullet_view()

    def add_joint(self):
        row_count = self.joints_table.rowCount()
        self.joints_table.insertRow(row_count)
        self.joints_table.setItem(row_count, 0, QTableWidgetItem(f'Joint_{row_count+1}'))
        joint_type = QComboBox()
        joint_type.addItems(['revolute', 'prismatic', 'fixed', 'continuous'])
        self.joints_table.setCellWidget(row_count, 1, joint_type)
        self.joints_table.setItem(row_count, 2, QTableWidgetItem('ParentLink'))
        self.joints_table.setItem(row_count, 3, QTableWidgetItem('ChildLink'))
        self.refresh_pybullet_view()

    def add_sensor(self):
        row_count = self.sensors_table.rowCount()
        self.sensors_table.insertRow(row_count)
        self.sensors_table.setItem(row_count, 0, QTableWidgetItem(f'Sensor_{row_count+1}'))
        sensor_type = QComboBox()
        sensor_type.addItems(['camera', 'lidar', 'imu'])
        self.sensors_table.setCellWidget(row_count, 1, sensor_type)
        self.sensors_table.setItem(row_count, 2, QTableWidgetItem('AttachedLink'))
        self.refresh_pybullet_view()

    def generate_urdf(self):
        if not self.validate_inputs():
            return

        save_dialog = QFileDialog()
        save_path, _ = save_dialog.getSaveFileName(self, "Save URDF File", "", "URDF Files (*.urdf);;All Files (*)")
        if save_path:
            urdf_options = self.create_urdf_options()
            success = self.robot_item.ExportURDF(save_path, urdf_options)
            if success:
                QMessageBox.information(self, 'Success', f'URDF file generated successfully at {save_path}.')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to generate URDF file.')

    def save_urdf(self):
        if not self.validate_inputs():
            return

        save_dialog = QFileDialog()
        save_path, _ = save_dialog.getSaveFileName(self, "Save URDF File", "", "URDF Files (*.urdf);;All Files (*)")
        if save_path:
            urdf_options = self.create_urdf_options()
            success = self.robot_item.ExportURDF(save_path, urdf_options)
            if success:
                QMessageBox.information(self, 'Success', f'URDF file saved successfully at {save_path}.')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to save URDF file.')

    def validate_inputs(self):
        name = self.input_name.text().strip()
        version = self.input_version.text().strip()
        manufacturer = self.input_manufacturer.text().strip()
        description = self.input_description.toPlainText().strip()

        if not name or not version or not manufacturer or not description:
            QMessageBox.warning(self, 'Warning', 'Please fill out all the robot details before proceeding.')
            return False
        return True

    def create_urdf_options(self):
        name = self.input_name.text().strip()
        version = self.input_version.text().strip()
        manufacturer = self.input_manufacturer.text().strip()
        description = self.input_description.toPlainText().strip()

        # Example of constructing URDF options
        urdf_options = {
            "name": name,
            "version": version,
            "manufacturer": manufacturer,
            "description": description,
        }

        return urdf_options

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = URDFGeneratorApp()
    ex.show()
    sys.exit(app.exec_())
