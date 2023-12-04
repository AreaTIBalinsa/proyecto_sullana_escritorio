import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class KeyTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Tecla', 'Código Qt', 'Letra'])

        self.populateTable()

        self.filter_edit = QLineEdit(self)
        self.filter_edit.setPlaceholderText("Filtrar por código Qt")
        self.filter_edit.textChanged.connect(self.filterTable)

        layout = QVBoxLayout()
        layout.addWidget(self.filter_edit)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def populateTable(self):
        for key_name in dir(Qt):
            if key_name.startswith('Key_'):
                key_code = getattr(Qt, key_name)
                key_letter = chr(key_code) if 32 <= key_code <= 126 else ''
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(key_name))
                self.table.setItem(row_position, 1, QTableWidgetItem(str(key_code)))
                self.table.setItem(row_position, 2, QTableWidgetItem(key_letter))

    def filterTable(self):
        filter_text = self.filter_edit.text()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if filter_text.lower() in item.text().lower():
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def keyPressEvent(self, event):
        key_code = event.key()
        for row in range(self.table.rowCount()):
            if int(self.table.item(row, 1).text()) == key_code:
                print(f"Tecla presionada: {self.table.item(row, 0).text()} ({key_code})")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyTableWidget()

    window.setGeometry(100, 100, 500, 400)
    window.setWindowTitle("Tabla de Teclas en PyQt")

    window.show()
    sys.exit(app.exec_())
