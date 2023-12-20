from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, QGridLayout, QPushButton, QCheckBox, QComboBox, QTableWidget, QMainWindow, QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student managment system")
        grid = QGridLayout()

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add subitems to menus
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Creating table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.resize(400, self.height())



    def load_data(self):
        connection = sqlite3.connect("./database.db")
        result = connection.execute("SELECt * FROM students")
        enumerated_result = enumerate(result)
        self.table.setRowCount(0)

        for row_number, row_data in enumerated_result:
            self.table.insertRow(row_number)
            self.table.setItem(row_number, 0, QTableWidgetItem(str(row_data[0])))
            self.table.setItem(row_number, 1, QTableWidgetItem(str(row_data[1])))
            self.table.setItem(row_number, 2, QTableWidgetItem(str(row_data[2])))
            self.table.setItem(row_number, 3, QTableWidgetItem(str(row_data[3])))

        connection.close()

        

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())

# 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
