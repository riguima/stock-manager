from stock_manager.domain.product import Product
from stock_manager.domain.stock import Stock
from stock_manager.repositories.product import ProductRepository
from stock_manager.repositories.stock import StockRepository
from stock_manager.widgets.stock_window import StockWindow


def test_add_stock(qtbot) -> None:
    product = Product(
        code=1,
        name='Creme',
        purchase_price=100,
        sale_price=150,
        minimum_stock=10,
        description='Qualquer descrição',
    )
    ProductRepository().create(product)
    widget = StockWindow()
    qtbot.addWidget(widget)
    widget.product_combobox.setCurrentIndex(0)
    widget.amount_input.setText('100')
    widget.add_stock_button.click()
    expected = Stock(
        id=1,
        product=product,
        amount=100,
    )
    assert widget.message_box.text() == 'Estoque adicionado!'
    assert widget.message_box.isVisible()
    assert StockRepository().all()[0] == expected
    assert len(widget.stock_table._data) == 1
    assert widget.stock_table._header == ['ID', 'Produto', 'Quantidade']


def test_delete_stock(qtbot) -> None:
    widget = StockWindow()
    qtbot.addWidget(widget)
    widget.product_combobox.setCurrentIndex(0)
    widget.amount_input.setText('50')
    widget.delete_stock_button.click()
    assert widget.stock_table._data[0][1] == '50'
    assert widget.message_box.text() == 'Estoque removido!'
    assert widget.message_box.isVisible()


def test_minimum_stock(qtbot) -> None:
    widget = StockWindow()
    qtbot.addWidget(widget)
    widget.product_combobox.setCurrentIndex(0)
    widget.amount_input.setText('40')
    widget.delete_stock_button.click()
    assert widget.stock_table._data[0][1] == '10'
    assert widget.message_box.text() == 'Estoque mínimo atingido!'
    assert widget.message_box.isVisible()


def test_delete_stock_without_amount_avaliable(qtbot) -> None:
    widget = StockWindow()
    qtbot.addWidget(widget)
    widget.product_combobox.setCurrentIndex(0)
    widget.amount_input.setText('100')
    widget.delete_stock_button.click()
    assert widget.stock_table._data[0][1] == '10'
    assert widget.message_box.text() == (
        'Não é possivel retirar mais que a quantidade em estoque!'
    )
    assert widget.message_box.isVisible()
