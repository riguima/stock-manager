from PySide6 import QtCore, QtGui, QtWidgets

from stock_manager.domain.product import Product
from stock_manager.repositories.product import ProductRepository
from stock_manager.widgets.helpers import Button, HorizontalLayout
from stock_manager.widgets.models import ProductModel


class ProductRegistrationWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setWindowTitle('Estoque')

        self.message_box = QtWidgets.QMessageBox()
        self.message_box.setWindowTitle('Aviso')

        self.code_label = QtWidgets.QLabel('Código:')
        self.code_input = QtWidgets.QLineEdit()
        self.code_input.setValidador(QtGui.QIntValidator())
        self.code_layout = HorizontalLayout(self.code_label, self.code_input)

        self.purchase_price_label = QtWidgets.QLabel('Preço de compra:')
        self.purchase_price_input = QtWidgets.QLineEdit()
        self.purchase_price_input.setValidator(QtGui.QDoubleValidator())
        self.purchase_price_layout = HorizontalLayout(
            self.purchase_price_label,
            self.purchase_price_input,
        )

        self.sale_price_label = QtWidgets.QLabel('Preço de venda:')
        self.sale_price_input = QtWidgets.QLineEdit()
        self.sale_price_input.setValidator(QtGui.QDoubleValidator())
        self.sale_price_layout = HorizontalLayout(
            self.sale_price_label,
            self.sale_price_input,
        )

        self.amount_label = QtWidgets.QLabel('Quantidade:')
        self.amount_input = QtWidgets.QLineEdit()
        self.amount_input.setValidator(QtGui.QIntValidator())
        self.amount_layou = HorizontalLayout(
            self.amount_label,
            self.amount_input,
        )

        self.minimum_stock_label = QtWidgets.QLabel('Estoque mínimo:')
        self.minimum_stock_input = QtWidgets.QLineEdit()
        self.minimum_stock_input.setValidator(QtGui.QIntValidator())
        self.minimum_stock_layout = HorizontalLayout(
            self.minimum_stock_label,
            self.minimum_stock_input,
        )

        self.description_label = QtWidgets.QLabel('Descrição:')
        self.description_text_edit = QtWidgets.QTextEdit()

        self.add_product_button = Button('Cadastrar Produto')
        self.add_product_button.clicked.connect(self.add_product)

        self.registration_layout = QtWidgets.QVBoxLayout()
        self.registration_layout.addLayout(self.code_layout)
        self.registration_layout.addLayout(self.purchase_price_layout)
        self.registration_layout.addLayout(self.sale_price_layout)
        self.registration_layout.addLayout(self.amount_layout)
        self.registration_layout.addLayout(self.minimum_stock_layout)
        self.registration_layout.addWidget(self.description_label)
        self.registration_layout.addWidget(self.description_text_edit)
        self.registration_layout.addWidget(self.add_product_button)

        self.product_table_label = QtWidgets.QLabel('Tabela de produtos')
        self.product_table = QtWidgets.QTableView()
        self.delete_product_button = Button('Remover produto')
        self.delete_product_button.clicked.connect(self.remove_product)

        self.product_table_layout = QtWidgets.QVBoxLayout()
        self.product_table_layout.addWidget(self.product_table_label)
        self.product_table_layout.addWidget(self.product_table)
        self.product_table_layout.addWidget(self.delete_product_button)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addLayout(self.registration_layout)
        self.layout.addLayout(self.product_table_layout)

    @QtCore.Slot()
    def add_product(self) -> None:
        product = Product(
            code=int(self.code_input.text()),
            purchase_price=float(self.purchase_price_input.text()),
            sale_price=float(self.sale_price_input.text()),
            minimum_stock=int(self.minimum_stock_input.text()),
            description=self.description_text_edit.toPlainText(),
        )
        ProductRepository().create(product)
        self.update_product_table()
        self.message_box.setText('Produto adicionado!')
        self.message_box.show()

    @QtCore.Slot()
    def delete_product(self) -> None:
        for index in self.product_table.selectedIndexes():
            ProductRepository().delete(
                self.product_table.model().get_data_by_column(index, 0)
            )
        self.update_product_table()
        self.message_box.setText('Produto removido!')
        self.message_box.show()

    def update_product_table(self) -> None:
        data = [
            [
                p.id,
                p.code,
                p.purchase_price,
                p.sale_price,
                p.minimum_stock,
                p.description,
            ]
            for p in ProductRepository().all()
        ]
        headers = [
            'ID',
            'Código',
            'Preço de compra',
            'Preço de venda',
            'Estoque mínimo',
            'Descrição',
        ]
        if not data:
            data = [''] * len(headers)
        self.product_table.setModel(ProductModel(data, headers))