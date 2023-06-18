from PySide6 import QtCore


class BaseModel(QtCore.QAbstractTableModel):
    def __init__(self, data: list[str], header: list[str]):
        super().__init__()
        self._data = data
        self._header = header

    def get_data_by_column(
        self, index, column: int, role=QtCore.Qt.ItemDataRole.DisplayRole
    ):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][column]

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if (
            orientation == QtCore.Qt.Orientation.Horizontal
            and role == QtCore.Qt.ItemDataRole.DisplayRole
        ):
            return self._header[section]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._data[0])
