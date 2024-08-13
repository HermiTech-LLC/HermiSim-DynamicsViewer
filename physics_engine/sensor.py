import pybullet as p

class Sensor:
    def __init__(self, robot, sensor_type, position, orientation):
        self.robot = robot
        self.sensor_type = sensor_type
        self.position = position
        self.orientation = orientation
        self.data = None

    def update(self):
        if self.sensor_type == 'IMU':
            self.data = self._get_imu_data()
        elif self.sensor_type == 'Lidar':
            self.data = self._get_lidar_data()
        elif self.sensor_type == 'Camera':
            self.data = self._get_camera_data()
        else:
            raise ValueError(f"Unknown sensor type: {self.sensor_type}")

    def get_data(self):
        return self.data

    def _get_imu_data(self):
        # Realistic IMU data retrieval
        linear_acceleration, angular_velocity = p.getBaseVelocity(self.robot)
        return {
            'acceleration': linear_acceleration,
            'gyro': angular_velocity
        }

    def _get_lidar_data(self):
        # Realistic Lidar data retrieval
        points = p.getClosestPoints(self.robot, 100, 0.1)
        distances = [point[8] for point in points]  # 8 is the distance
        return {
            'distances': distances
        }

    def _get_camera_data(self):
        # Realistic Camera data retrieval
        width, height, rgb_img, depth_img, seg_img = p.getCameraImage(640, 480)
        return {
            'image': rgb_img
        }