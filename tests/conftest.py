import pytest

from stock_manager.widgets.main_window import MainWindow


@pytest.fixture(scope='module')
def widget() -> MainWindow:
    return MainWindow()
