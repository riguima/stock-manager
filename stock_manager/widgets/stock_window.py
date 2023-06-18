from PySide6 import QtCore, QtGui, QtWidgets

from stock_manager.domain.stock import Stock
from stock_manager.repositories.product import ProductRepository
from stock_manager.repositories.stock import StockRepository
from stock_manager.widgets.helpers import Button, HorizontalLayout
from stock_manager.widgets.tables_models import BaseModel


class StockWindow(QtWidgets.QWidget):
    def __init__(self, parent_window: QtWidgets.QWidget) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setWindowTitle('Insumos')

        self.message_box = QtWidgets.QMessageBox()
        self.message_box.setWindowTitle('Aviso')

        self.parent_window = parent_window

        self.product_label = QtWidgets.QLabel('Insumo:')
        self.product_combobox = QtWidgets.QComboBox()
        self.product_layout = HorizontalLayout(
            self.product_label,
            self.product_combobox,
        )

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

        self.return_to_parent_window_button = Button('Voltar')
        self.return_to_parent_window_button.clicked.connect(
            self.return_to_parent_window
        )

        self.stock_layout = QtWidgets.QVBoxLayout()
        self.stock_layout.addLayout(self.product_layout)
        self.stock_layout.addLayout(self.amount_layout)
        self.stock_layout.addWidget(self.add_stock_button)
        self.stock_layout.addWidget(self.delete_stock_button)
        self.stock_layout.addWidget(self.return_to_parent_window_button)
        self.stock_layout.addStretch()

        self.stock_table = QtWidgets.QTableView()
        self.stock_table_layout = QtWidgets.QVBoxLayout()
        self.stock_table_layout.addWidget(self.stock_table)

        self.update_stock_table()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addLayout(self.stock_layout)
        self.layout.addLayout(self.stock_table_layout)

    def update_product_combobox(self) -> None:
        self.product_combobox.clear()
        self.product_combobox.addItems(
            [p.name for p in ProductRepository().all()]
        )

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
        self.amount_input.setText('0')

    @QtCore.Slot()
    def delete_stock(self) -> None:
        product = ProductRepository().all()[
            self.product_combobox.currentIndex()
        ]
        amount = int(self.amount_input.text())
        if StockRepository().get_amount(product) < amount:
            self.message_box.setText(
                'Não é possivel retirar mais que a quantidade em estoque!'
            )
        else:
            if (
                StockRepository().get_amount(product) - amount
                <= product.minimum_stock
            ):
                self.message_box.setText('Estoque mínimo atingido!')
            else:
                self.message_box.setText('Estoque removido!')
            stock = Stock(
                product=product,
                amount=-int(self.amount_input.text()),
            )
            StockRepository().create(stock)
            self.update_stock_table()
        self.message_box.show()
        self.amount_input.setText('0')

    def update_stock_table(self) -> None:
        data = [
            [
                p.id,
                p.name,
                StockRepository().get_amount(p),
            ]
            for p in ProductRepository().all()
        ]
        headers = ['ID', 'Insumo', 'Quantidade']
        if not data:
            data = [['' for i in range(len(headers))]]
        self.stock_table.setModel(BaseModel(data, headers))

    @QtCore.Slot()
    def return_to_parent_window(self) -> None:
        self.parent_window.show()
        self.close()
