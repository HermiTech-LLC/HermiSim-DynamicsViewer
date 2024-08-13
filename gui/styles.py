from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

def apply_styles(app):
    palette = QPalette()
    
    # Set the general background color
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)

    # Highlight colors
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(palette)

    # Additional stylesheet for widget customization
    app.setStyleSheet("""
        QMainWindow {
            background-color: #353535;
        }
        QTabWidget::pane {
            border: 1px solid #444;
            padding: 5px;
            margin: 0px;
        }
        QTabBar::tab {
            background: #555;
            border: 1px solid #444;
            padding: 10px;
            margin: 1px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background: #777;
            margin-bottom: 0px;
        }
        QPushButton {
            background-color: #444;
            border: 1px solid #666;
            padding: 5px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #555;
        }
        QLabel {
            color: #FFF;
        }
        QSlider::groove:horizontal {
            background: #555;
            height: 8px;
        }
        QSlider::handle:horizontal {
            background: #777;
            border: 1px solid #666;
            width: 20px;
            margin: -5px 0;
            border-radius: 4px;
        }
        QToolTip {
            color: #FFF;
            background-color: #353535;
            border: 1px solid #444;
        }
        QMenuBar {
            background-color: #353535;
        }
        QMenuBar::item {
            background-color: #353535;
            color: #FFF;
        }
        QMenuBar::item:selected {
            background-color: #777;
        }
        QMenu {
            background-color: #353535;
            color: #FFF;
        }
        QMenu::item:selected {
            background-color: #777;
        }
        QLineEdit {
            background-color: #555;
            border: 1px solid #444;
            padding: 5px;
            border-radius: 4px;
            color: #FFF;
        }
    """)
