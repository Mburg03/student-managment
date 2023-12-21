from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, QGridLayout, QPushButton, QCheckBox, QComboBox, QTableWidget, QMainWindow, QTableWidgetItem, QDialog, QVBoxLayout
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
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add subitems to menus
        # *Add student on file menu item
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # *Add about on help menu item
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # *Add search on edit menu item
        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)
        search_action.setMenuRole(QAction.MenuRole.NoRole)


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
    
    
    def load_specific_student(self, results):
        enumerated_result = enumerate(results)
        self.table.setRowCount(0)

        for row_number, row_data in enumerated_result:
            self.table.insertRow(row_number)
            self.table.setItem(row_number, 0, QTableWidgetItem(str(row_data[0])))
            self.table.setItem(row_number, 1, QTableWidgetItem(str(row_data[1])))
            self.table.setItem(row_number, 2, QTableWidgetItem(str(row_data[2])))
            self.table.setItem(row_number, 3, QTableWidgetItem(str(row_data[3])))


    
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student Information
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student's name")
        layout.addWidget(self.student_name)
        
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Student's mobile number")
        layout.addWidget(self.mobile)


        # Add submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)


    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()

        connection = sqlite3.connect("./database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student's Name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student's name")
        layout.addWidget(self.student_name)
        
        # Add search button
        search_button = QPushButton("Search")   
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)

        self.setLayout(layout)


    def search_student(self):
        connection = sqlite3.connect("./database.db")
        cursor = connection.cursor()
        name = self.student_name.text()
        cursor.execute("SELECT * FROM students WHERE name =?", (name,))
        results = cursor.fetchall()

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_specific_student(results)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())

# 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