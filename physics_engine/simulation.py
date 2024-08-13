import pybullet as p
from physics_engine.engine import PhysicsEngine
from physics_engine.sensor import Sensor

class Simulation:
    def __init__(self):
        self.engine = PhysicsEngine()
        self.robot = None
        self.simulation_speed = 1
        self.sensors = []
        self.running = False

    def start(self):
        """Start the simulation."""
        if not self.running:
            self.engine.connect()
            self._load_environment()
            self.running = True
            try:
                while self.running:
                    self.engine.step_simulation()
                    self._update_sensors()
                    p.setTimeStep(1.0 / self.simulation_speed)
            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        """Stop the simulation."""
        if self.running:
            self.engine.disconnect()
            self.running = False

    def reset(self):
        """Reset the simulation."""
        self.stop()
        self.start()

    def load_robot(self, urdf_path, base_position=(0, 0, 1)):
        """Load a robot URDF into the simulation."""
        self.robot = self.engine.load_urdf(urdf_path, base_position)
        if self.robot is not None:
            print(f"Robot loaded: {urdf_path}")
        else:
            print(f"Failed to load robot: {urdf_path}")

    def set_speed(self, speed):
        """Set the simulation speed."""
        self.simulation_speed = speed

    def get_sensor_data(self):
        """Get data from all sensors."""
        data = {}
        for sensor in self.sensors:
            sensor.update()
            data[sensor.sensor_type] = sensor.get_data()
        return data

    def add_sensor(self, sensor):
        """Add a sensor to the simulation."""
        self.sensors.append(sensor)
        print(f"Sensor added: {sensor.sensor_type}")

    def _load_environment(self):
        """Load the simulation environment."""
        p.loadURDF("plane.urdf")
        p.loadURDF("r2d2.urdf", [0, 0, 1])
        print("Environment loaded")

    def _update_sensors(self):
        """Update all sensors."""
        for sensor in self.sensors:
            sensor.update()