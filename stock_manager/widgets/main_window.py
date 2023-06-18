from PySide6 import QtCore, QtWidgets

from stock_manager.widgets.helpers import Button
from stock_manager.widgets.product_window import ProductWindow
from stock_manager.widgets.stock_window import StockWindow


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(150, 100)
        self.setWindowTitle('Janela principal')

        self.product_window = ProductWindow(self)
        self.stock_window = StockWindow(self)

        self.message_box = QtWidgets.QMessageBox()
        self.message_box.setWindowTitle('Aviso')

        self.show_product_window_button = Button('Produtos')
        self.show_product_window_button.clicked.connect(
            self.show_product_window
        )

        self.show_stock_window_button = Button('Estoque')
        self.show_stock_window_button.clicked.connect(self.show_stock_window)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.show_product_window_button)
        self.layout.addWidget(self.show_stock_window_button)

    @QtCore.Slot()
    def show_product_window(self) -> None:
        self.product_window.show()
        self.close()

    @QtCore.Slot()
    def show_stock_window(self) -> None:
        self.stock_window.update_product_combobox()
        self.stock_window.show()
        self.close()
