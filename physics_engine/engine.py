# physics_engine/engine.py
import pybullet as p
import pybullet_data

class PhysicsEngine:
    def __init__(self):
        self.physics_client = None
        self.connected = False

    def connect(self, mode=p.GUI):
        """Connect to the PyBullet physics server."""
        try:
            self.physics_client = p.connect(mode)
            p.setAdditionalSearchPath(pybullet_data.getDataPath())
            p.setGravity(0, 0, -9.81)
            self.connected = True
            print("Connected to PyBullet physics server.")
        except Exception as e:
            print(f"Failed to connect to PyBullet: {e}")

    def disconnect(self):
        """Disconnect from the PyBullet physics server."""
        if self.physics_client is not None and self.connected:
            p.disconnect(self.physics_client)
            self.physics_client = None
            self.connected = False
            print("Disconnected from PyBullet physics server.")

    def step_simulation(self):
        """Step the simulation forward."""
        if self.physics_client is not None and self.connected:
            p.stepSimulation()
        else:
            print("Cannot step simulation. Physics client is not connected.")

    def load_urdf(self, urdf_file, base_position=(0, 0, 0), base_orientation=(0, 0, 0, 1)):
        """Load a URDF file into the simulation."""
        if self.physics_client is not None and self.connected:
            return p.loadURDF(urdf_file, basePosition=base_position, baseOrientation=base_orientation)
        else:
            print("Cannot load URDF. Physics client is not connected.")
            return None

    def get_body_info(self, body_id):
        """Get information about a body in the simulation."""
        if self.physics_client is not None and self.connected:
            return p.getBodyInfo(body_id)
        else:
            print("Cannot get body info. Physics client is not connected.")
            return None

    def apply_force(self, body_id, link_index, force, position, flags=p.WORLD_FRAME):
        """Apply a force to a body in the simulation."""
        if self.physics_client is not None and self.connected:
            p.applyExternalForce(body_id, link_index, force, position, flags)
        else:
            print("Cannot apply force. Physics client is not connected.")

    def reset_simulation(self):
        """Reset the simulation."""
        if self.physics_client is not None and self.connected:
            p.resetSimulation()
            print("Simulation reset.")
        else:
            print("Cannot reset simulation. Physics client is not connected.")
