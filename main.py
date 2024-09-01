# ///////////////////////////////////////////////////////////////
# Developer: Mehdi Sameni
# Designer: Mehdi Sameni
# PyQt6
# Python 3.10
# ///////////////////////////////////////////////////////////////


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QApplication, QWidget, QVBoxLayout
from PyQt6.QtGui import QColor
from Arc_Loader import UseArcLoader


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout = QVBoxLayout(self)
        frame = QFrame(self)
        frame.resize(170, 170)
        layoutF = QVBoxLayout(frame)
        layout.addWidget(frame)
        loader = UseArcLoader(frame, penWidth=6, color=QColor("#D1B000"), diameter=frame.width())
        layoutF.addWidget(loader)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
