from stock_manager.domain.product import Product
from stock_manager.domain.stock import Stock
from stock_manager.repositories.product import ProductRepository
from stock_manager.repositories.stock import StockRepository
from stock_manager.widgets.stock_window import StockWindow
from stock_manager.widgets.main_window import MainWindow


def test_add_stock(qtbot, widget: MainWindow) -> None:
    product = Product(
        code=1,
        name='Creme',
        purchase_price=100,
        sale_price=150,
        minimum_stock=10,
        description='Qualquer descrição',
    )
    product = ProductRepository().create(product)
    qtbot.addWidget(widget)
    widget.stock_window.product_combobox.setCurrentIndex(0)
    widget.stock_window.amount_input.setText('100')
    widget.stock_window.add_stock_button.click()
    expected = Stock(
        id=1,
        product=product,
        amount=100,
    )
    assert widget.stock_window.message_box.text() == 'Estoque adicionado!'
    assert widget.stock_window.message_box.isVisible()
    assert StockRepository().all()[0] == expected
    assert len(widget.stock_window.stock_table.model()._data) == 1
    assert widget.stock_window.stock_table.model()._headers == [
        'ID',
        'Produto',
        'Quantidade',
    ]


def test_delete_stock(qtbot, widget: MainWindow) -> None:
    qtbot.addWidget(widget)
    widget.stock_window.product_combobox.setCurrentIndex(0)
    widget.stock_window.amount_input.setText('50')
    widget.stock_window.delete_stock_button.click()
    assert widget.stock_window.stock_table.model()._data[0][1] == '50'
    assert widget.stock_window.message_box.text() == 'Estoque removido!'
    assert widget.stock_window.message_box.isVisible()


def test_minimum_stock(qtbot, widget: MainWindow) -> None:
    qtbot.addWidget(widget)
    widget.stock_window.product_combobox.setCurrentIndex(0)
    widget.stock_window.amount_input.setText('40')
    widget.stock_window.delete_stock_button.click()
    assert widget.stock_window.stock_table.model()._data[0][1] == '10'
    assert widget.stock_window.message_box.text() == 'Estoque mínimo atingido!'
    assert widget.stock_window.message_box.isVisible()


def test_delete_stock_without_amount_avaliable(
    qtbot, widget: MainWindow
) -> None:
    qtbot.addWidget(widget)
    widget.stock_window.product_combobox.setCurrentIndex(0)
    widget.stock_window.amount_input.setText('100')
    widget.stock_window.delete_stock_button.click()
    assert widget.stock_window.stock_table.model()._data[0][1] == '10'
    assert widget.stock_window.message_box.text() == (
        'Não é possivel retirar mais que a quantidade em estoque!'
    )
    assert widget.stock_window.message_box.isVisible()
