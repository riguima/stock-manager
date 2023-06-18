from PySide6 import QtCore


class ProductModel(QtCore.QAbstractTableModel):
    def __init__(self, data: list[str], headers: list[str]) -> None:
        super().__init__()
        self._data = data
        self._headers = headers

    def get_data_by_column(
        self, index, column: int, role=QtCore.Qt.ItemDataRole.DisplayRole
    ) -> str:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][column]

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def headersData(self, section, orientation, role):
        if (
            orientation == QtCore.Qt.Orientation.Horizontal
            and role == QtCore.Qt.ItemDataRole.DisplayRole
        ):
            return self._headers[section]

    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()) -> int:
        return len(self._data[0])
