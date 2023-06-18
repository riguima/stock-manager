from stock_manager.domain.product import Product
from stock_manager.repositories.product import ProductRepository
from stock_manager.widgets.main_window import MainWindow


def test_add_product(qtbot, widget: MainWindow) -> None:
    qtbot.addWidget(widget)
    widget.product_window.code_input.setText('1')
    widget.product_window.name_input.setText('Creme')
    widget.product_window.purchase_price_input.setText('100')
    widget.product_window.sale_price_input.setText('150')
    widget.product_window.minimum_stock_input.setText('10')
    widget.product_window.description_text_edit.insertPlainText('Qualquer descrição')
    widget.product_window.add_product_button.click()
    expected = Product(
        id=1,
        code=1,
        name='Creme',
        purchase_price=100,
        sale_price=150,
        minimum_stock=10,
        description='Qualquer descrição',
    )
    assert widget.product_window.product_table.model()._headers == [
        'ID',
        'Código',
        'Nome',
        'Preço de compra',
        'Preço de venda',
        'Estoque mínimo',
        'Descrição',
    ]
    assert len(widget.product_window.product_table.model()._data) == 1
    assert widget.product_window.message_box.text() == 'Produto adicionado!'
    assert widget.product_window.message_box.isVisible()
    assert ProductRepository().all()[0] == expected


def test_delete_product(qtbot, widget: MainWindow) -> None:
    qtbot.addWidget(widget)
    widget.product_window.product_table.selectRow(0)
    widget.product_window.delete_product_button.click()
    assert widget.product_window.message_box.text() == 'Produto removido!'
    assert widget.product_window.message_box.isVisible()
    assert len(ProductRepository().all()) == 0
