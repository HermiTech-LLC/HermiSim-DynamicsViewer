from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton

class LogTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        layout.addWidget(self.log_viewer)

        self.clear_button = QPushButton('Clear Logs')
        self.clear_button.clicked.connect(self.clear_logs)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

    def add_log(self, message):
        self.log_viewer.append(message)

    def clear_logs(self):
        self.log_viewer.clear()
