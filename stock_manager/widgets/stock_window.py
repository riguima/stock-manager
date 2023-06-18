from PySide6 import QtCore, QtGui, QtWidgets

from stock_manager.domain.stock import Stock
from stock_manager.repositories.product import ProductRepository
from stock_manager.repositories.stock import StockRepository
from stock_manager.widgets.helpers import Button, HorizontalLayout
from stock_manager.widgets.tables_models import BaseModel


class StockWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setWindowTitle('Produtos')

        self.message_box = QtWidgets.QMessageBox()
        self.message_box.setWindowTitle('Aviso')

        self.product_label = QtWidgets.QLabel('Produto:')
        self.product_combobox = QtWidgets.QComboBox()
        self.product_layout = HorizontalLayout(
            self.product_label,
            self.product_combobox,
        )
        self.update_product_combobox()

        self.amount_label = QtWidgets.QLabel('Quantidade:')
        self.amount_input = QtWidgets.QLineEdit()
        self.amount_input.setValidator(QtGui.QIntValidator())
        self.amount_layout = HorizontalLayout(
            self.amount_label,
            self.amount_input,
        )

        self.add_stock_button = Button('Adicionar estoque')
        self.add_stock_button.clicked.connect(self.add_stock)

        self.delete_stock_button = Button('Remover estoque')
        self.delete_stock_button.clicked.connect(self.delete_stock)

        self.stock_layout = QtWidgets.QVBoxLayout()
        self.stock_layout.addLayout(self.product_layout)
        self.stock_layout.addLayout(self.amount_layout)
        self.stock_layout.addWidget(self.add_stock_button)
        self.stock_layout.addWidget(self.delete_stock_button)

        self.stock_table_label = QtWidgets.QLabel('Tabela de produtos')
        self.stock_table = QtWidgets.QTableView()
        self.stock_table_layout = QtWidgets.QVBoxLayout()
        self.stock_table_layout.addWidget(self.stock_table_label)
        self.stock_table_layout.addWidget(self.stock_table)

        self.update_stock_table()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addLayout(self.stock_layout)
        self.layout.addLayout(self.stock_table_layout)

    @QtCore.Slot()
    def add_stock(self) -> None:
        product = ProductRepository().all()[
            self.product_combobox.currentIndex()
        ]
        stock = Stock(product=product, amount=int(self.amount_input.text()))
        StockRepository().create(stock)
        self.update_stock_table()
        self.message_box.setText('Estoque adicionado!')
        self.message_box.show()

    @QtCore.Slot()
    def delete_stock(self) -> None:
        StockRepository().delete(
            self.product_combobox.currentText(),
            int(self.amount_input.text()),
        )
        self.update_stock_table()
        self.message_box.setText('Estoque removido!')
        self.message_box.show()

    def update_stock_table(self) -> None:
        data = [
            [
                p.id,
                p.name,
                StockRepository().get_amount(p),
            ]
            for p in ProductRepository().all()
        ]
        headers = ['ID', 'Produto', 'Quantidade']
        if not data:
            data = [''] * len(headers)
        self.stock_table.setModel(BaseModel(data, headers))
