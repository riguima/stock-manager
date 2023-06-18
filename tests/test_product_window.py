from stock_manager.domain.product import Product
from stock_manager.repositories.product import ProductRepository
from stock_manager.widgets.product_window import ProductWindow


def test_add_product(qtbot) -> None:
    widget = ProductWindow()
    qtbot.addWidget(widget)
    widget.code_input.setText('1')
    widget.purchase_price_input.setText('100')
    widget.sale_price_input.setText('150')
    widget.minimum_stock_input.setText('10')
    widget.description_text_edit.insertPlainText('Qualquer descrição')
    widget.add_product_button.click()
    expected = Product(
        id=1,
        code=1,
        name='Creme',
        purchase_price=100,
        sale_price=150,
        minimum_stock=10,
        description='Qualquer descrição',
    )
    assert widget.product_table.model()._headers == [
        'ID',
        'Código',
        'Nome',
        'Preço de compra',
        'Preço de venda',
        'Estoque mínimo',
        'Descrição',
    ]
    assert len(widget.product_table.model()._data) == 1
    assert widget.message_box.text() == 'Produto adicionado!'
    assert widget.message_box.isVisible()
    assert ProductRepository().all()[0] == expected


def test_delete_product(qtbot) -> None:
    widget = ProductWindow()
    qtbot.addWidget(widget)
    widget.product_table.selectRow(0)
    widget.delete_product_button.click()
    assert widget.message_box.text() == 'Produto removido!'
    assert widget.message_box.isVisible()
    assert len(ProductRepository().all()) == 0
