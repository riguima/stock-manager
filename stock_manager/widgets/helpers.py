from PySide6 import QtWidgets


class Button(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet('background-color: #187bcd; color: white')


class HorizontalLayout(QtWidgets.QHBoxLayout):
    def __init__(
        self, label: QtWidgets.QLabel, input_widget: QtWidgets.QLineEdit
    ) -> None:
        super().__init__()
        self.addWidget(label, 1)
        self.addWidget(input_widget, 3)
