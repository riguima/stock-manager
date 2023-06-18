from stock_manager.widgets.main_window import MainWindow


def test_show_product_window(qtbot) -> None:
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.show_product_window_button.click()
    assert widget.product_window.isVisible()
    assert widget.isVisible()


def test_show_stock_window(qtbot) -> None:
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.show_stock_window_button.click()
    assert widget.stock_window.isVisible()
    assert widget.isVisible()
