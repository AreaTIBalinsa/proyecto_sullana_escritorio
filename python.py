import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
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

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def populateTable(self):
        for key_name in dir(Qt):
            if key_name.startswith('Key_'):
                key_code = getattr(Qt, key_name)
                key_letter = chr(key_code) if 32 <= key_code <= 126 else ''  # Obtén la letra solo si es imprimible
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(key_name))
                self.table.setItem(row_position, 1, QTableWidgetItem(str(key_code)))
                self.table.setItem(row_position, 2, QTableWidgetItem(key_letter))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyTableWidget()
    
    window.setGeometry(100, 100, 500, 400)
    window.setWindowTitle("Tabla de Teclas en PyQt")
    
    window.show()
    sys.exit(app.exec_())
