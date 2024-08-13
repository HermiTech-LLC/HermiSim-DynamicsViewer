# A Robotics Simulation Suite

## Overview

This Robotics Simulation Suite is a sophisticated application designed for loading URDF/XML files, rendering objects in a 3D space, and running robotic simulations using a physics engine. The application supports multiple tabs and functionalities to provide a comprehensive simulation environment.

## Features

- **Load URDF/XML Files**: Load and parse URDF/XML files to simulate robots.
- **3D Rendering**: Visualize robots and environments in 3D using PyQt and PyBullet.
- **Physics Engine**: Leverage PyBullet for realistic physics simulations.
- **Sensor Data**: Simulate and display data from various sensors like IMU, Lidar, and Camera.
- **Simulation Controls**: Start, stop, reset simulations, and control simulation speed.
- **Logs and Debugging**: View logs for debugging and simulation insights.
- **Modular Design**: The application is modular, allowing easy extension and maintenance.

## Directory Structure

```
HERMISIM/
│
├──gui/
│   ├── styles.py
│   ├── main_window.py
│   ├── file_loader.py
│   ├── object_renderer.py
│   ├── simulation_controls.py
│   ├── sensor_data_viewer.py
│   ├── tabs/
│   │   ├── render_tab.py
│   │   ├── simulation_tab.py
│   │   ├── log_tab.py
│   │   ├── sensor_tab.py
physics_engine/
│   ├── engine.py
│   ├── simulation.py
│   ├── sensor.py
tests/
main.py
README.md


## Installation and Usage

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the application**:
    ```bash
    python main.py
    ```

## Components

### `main.py`
- Entry point of the application. Initializes the PyQt application, applies styles, and creates the main window.

### `gui/styles.py`
- Defines and applies the application's styles using PyQt.

### `gui/main_window.py`
- Main window of the application, integrates all tabs and handles file loading.

### `gui/file_loader.py`
- Handles loading and parsing of URDF/XML files.

### `gui/object_renderer.py`
- Renders the robot and environment objects in a 3D space.

### `gui/simulation_controls.py`
- Provides controls for starting, stopping, and resetting the simulation, as well as adjusting the simulation speed.

### `gui/sensor_data_viewer.py`
- Displays sensor data in a tabular format, updating in real-time.

### `gui/tabs/render_tab.py`
- Contains the render view for visualizing the robot and environment.

### `gui/tabs/simulation_tab.py`
- Contains simulation control elements.

### `gui/tabs/log_tab.py`
- Displays logs and debugging information.

### `physics_engine/engine.py`
- Manages the connection to the PyBullet physics engine and handles simulation stepping.

### `physics_engine/simulation.py`
- Controls the simulation, including starting, stopping, resetting, and updating sensors.

### `physics_engine/sensor.py`
- Simulates various sensors (IMU, Lidar, Camera) and provides realistic data.

## Additional Notes

- Ensure that PyBullet and PyQt5 are correctly installed.
- The application is designed to be modular, so new features and sensors can be easily added.
