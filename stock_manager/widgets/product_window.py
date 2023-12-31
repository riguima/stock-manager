from PySide6 import QtCore, QtGui, QtWidgets

from stock_manager.domain.product import Product
from stock_manager.repositories.product import ProductRepository
from stock_manager.widgets.helpers import Button, HorizontalLayout
from stock_manager.widgets.tables_models import BaseModel


class ProductWindow(QtWidgets.QWidget):
    def __init__(self, parent_window: QtWidgets.QWidget) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setWindowTitle('Insumos')

        self.message_box = QtWidgets.QMessageBox()
        self.message_box.setWindowTitle('Aviso')

        self.parent_window = parent_window

        self.code_label = QtWidgets.QLabel('Código:')
        self.code_input = QtWidgets.QLineEdit()
        self.code_input.setValidator(QtGui.QIntValidator())
        self.code_layout = HorizontalLayout(self.code_label, self.code_input)

        self.name_label = QtWidgets.QLabel('Insumo:')
        self.name_input = QtWidgets.QLineEdit()
        self.name_layout = HorizontalLayout(self.name_label, self.name_input)

        self.minimum_stock_label = QtWidgets.QLabel('Estoque mínimo:')
        self.minimum_stock_input = QtWidgets.QLineEdit()
        self.minimum_stock_input.setValidator(QtGui.QIntValidator())
        self.minimum_stock_layout = HorizontalLayout(
            self.minimum_stock_label,
            self.minimum_stock_input,
        )

        self.description_label = QtWidgets.QLabel('Descrição:')
        self.description_text_edit = QtWidgets.QTextEdit()

        self.add_product_button = Button('Cadastrar Insumo')
        self.add_product_button.clicked.connect(self.add_product)

        self.return_to_parent_window_button = Button('Voltar')
        self.return_to_parent_window_button.clicked.connect(
            self.return_to_parent_window
        )

        self.registration_layout = QtWidgets.QVBoxLayout()
        self.registration_layout.addLayout(self.code_layout)
        self.registration_layout.addLayout(self.name_layout)
        self.registration_layout.addLayout(self.minimum_stock_layout)
        self.registration_layout.addWidget(self.description_label)
        self.registration_layout.addWidget(self.description_text_edit)
        self.registration_layout.addWidget(self.add_product_button)
        self.registration_layout.addWidget(self.return_to_parent_window_button)

        self.product_table = QtWidgets.QTableView()
        self.delete_product_button = Button('Remover produto')
        self.delete_product_button.clicked.connect(self.delete_product)

        self.product_table_layout = QtWidgets.QVBoxLayout()
        self.product_table_layout.addWidget(self.product_table)
        self.product_table_layout.addWidget(self.delete_product_button)

        self.update_product_table()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addLayout(self.registration_layout)
        self.layout.addLayout(self.product_table_layout)

    @QtCore.Slot()
    def add_product(self) -> None:
        product = Product(
            code=int(self.code_input.text()),
            name=self.name_input.text(),
            minimum_stock=int(self.minimum_stock_input.text()),
            description=self.description_text_edit.toPlainText(),
        )
        ProductRepository().create(product)
        self.update_product_table()
        self.message_box.setText('Insumo adicionado!')
        self.message_box.show()
        self.clear_inputs()

    def clear_inputs(self) -> None:
        inputs = [
            self.code_input,
            self.name_input,
            self.minimum_stock_input,
        ]
        for i in inputs:
            i.setText('')
        self.description_text_edit.clear()

    @QtCore.Slot()
    def return_to_parent_window(self) -> None:
        self.parent_window.show()
        self.close()

    @QtCore.Slot()
    def delete_product(self) -> None:
        for index in self.product_table.selectedIndexes():
            ProductRepository().delete(
                int(self.product_table.model().get_data_by_column(index, 0))
            )
        self.update_product_table()
        self.message_box.setText('Insumo removido!')
        self.message_box.show()

    def update_product_table(self) -> None:
        data = [
            [
                p.id,
                p.code,
                p.name,
                p.minimum_stock,
                p.description,
            ]
            for p in ProductRepository().all()
        ]
        headers = [
            'ID',
            'Código',
            'Insumo',
            'Estoque mínimo',
            'Descrição',
        ]
        if not data:
            data = [['' for i in range(len(headers))]]
        self.product_table.setModel(BaseModel(data, headers))
