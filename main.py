import sys

from PySide6 import QtWidgets

from stock_manager.widgets.main_window import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
