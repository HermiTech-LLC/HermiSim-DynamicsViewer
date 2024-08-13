import pyqtgraph.opengl as gl
import pybullet as p
import numpy as np

class ObjectRenderer:
    def __init__(self, simulation):
        self.simulation = simulation
        self.view_widget = gl.GLViewWidget()
        self.init_view()

    def init_view(self):
        self.view_widget.opts['distance'] = 20
        grid = gl.GLGridItem()
        self.view_widget.addItem(grid)
        self.robot_items = []

    def render_robot(self):
        if self.simulation.robot is not None:
            self._clear_robot()
            self._render_robot()

    def _clear_robot(self):
        for item in self.robot_items:
            self.view_widget.removeItem(item)
        self.robot_items = []

    def _render_robot(self):
        for link_index in range(p.getNumJoints(self.simulation.robot)):
            link_state = p.getLinkState(self.simulation.robot, link_index)
            pos, orn = link_state[4], link_state[5]
            self._draw_sphere(pos)

    def _draw_sphere(self, pos):
        pos = np.array(pos)
        sphere = gl.GLScatterPlotItem(pos=[pos], size=0.1, color=(1, 0, 0, 1))
        self.view_widget.addItem(sphere)
        self.robot_items.append(sphere)
    
    def update_view(self):
        self.render_robot()
        self.view_widget.update()

    def reset_view(self):
        self._clear_robot()
        self.init_view()