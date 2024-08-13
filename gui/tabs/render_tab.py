from PyQt5.QtWidgets import QWidget, QVBoxLayout
from gui.object_renderer import ObjectRenderer

class RenderTab(QWidget):
    def __init__(self, simulation):
        super().__init__()
        self.simulation = simulation
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.renderer = ObjectRenderer(self.simulation)
        layout.addWidget(self.renderer.view_widget)

        self.setLayout(layout)

    def update_render(self):
        self.renderer.render_robot()