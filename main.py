import sys
import csv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QTabWidget, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QComboBox, 
                             QDateEdit, QHeaderView, QMessageBox, QDialog,
                             QFormLayout, QDialogButtonBox, QMenu, QFileDialog)
from PyQt6.QtCore import QDate, Qt
import database

class StudentDialog(QDialog):
    """A dialog for adding or editing student information."""
    def __init__(self, student_id=None, full_name=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student" if student_id else "Add Student")
        layout = QFormLayout(self)
        self.student_id_input = QLineEdit(student_id)
        if student_id:
            self.student_id_input.setReadOnly(True)
        self.full_name_input = QLineEdit(full_name)
        layout.addRow("Student ID:", self.student_id_input)
        layout.addRow("Full Name:", self.full_name_input)
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        
    def get_data(self):
        return self.student_id_input.text(), self.full_name_input.text()

class ClassDialog(QDialog):
    """A dialog for editing class information."""
    def __init__(self, class_name=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Class")
        layout = QFormLayout(self)
        self.class_name_input = QLineEdit(class_name)
        layout.addRow("Class Name:", self.class_name_input)
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        
    def get_data(self):
        return self.class_name_input.text()

class AttendanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Class Attendance System")
        self.setGeometry(100, 100, 900, 700)
        database.setup_database()
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.create_attendance_tab()
        self.create_reports_tab()
        self.create_manage_students_tab()
        self.create_manage_classes_tab()
        
        self.refresh_all_data()

    def create_attendance_tab(self):
        tab, layout = QWidget(), QVBoxLayout()
        self.class_selector_att = QComboBox()
        self.class_selector_att.currentIndexChanged.connect(self.load_students_for_attendance)
        layout.addWidget(QLabel("Select Class:"))
        layout.addWidget(self.class_selector_att)
        
        self.date_edit_att = QDateEdit(calendarPopup=True, date=QDate.currentDate())
        layout.addWidget(QLabel("Select Date:"))
        layout.addWidget(self.date_edit_att)
        
        self.attendance_table = QTableWidget(columnCount=3)
        self.attendance_table.setHorizontalHeaderLabels(["Student ID", "Full Name", "Status"])
        self.attendance_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.attendance_table)
        
        save_button = QPushButton("Save Attendance")
        save_button.clicked.connect(self.save_attendance)
        layout.addWidget(save_button)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Take Attendance")

    def create_reports_tab(self):
        tab, layout = QWidget(), QVBoxLayout()
        self.class_selector_rep = QComboBox()
        layout.addWidget(QLabel("Filter by Class:"))
        layout.addWidget(self.class_selector_rep)
        
        self.start_date_rep = QDateEdit(calendarPopup=True, date=QDate.currentDate().addMonths(-1))
        self.end_date_rep = QDateEdit(calendarPopup=True, date=QDate.currentDate())
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_date_rep)
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_date_rep)
        
        generate_button = QPushButton("Generate Report")
        generate_button.clicked.connect(self.generate_report)
        layout.addWidget(generate_button)
        
        self.report_table = QTableWidget(columnCount=4)
        self.report_table.setHorizontalHeaderLabels(["Student ID", "Full Name", "Date", "Status"])
        self.report_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.report_table)
        
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_report_to_csv)
        layout.addWidget(export_button)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Reports")

    def create_manage_students_tab(self):
        tab, layout = QWidget(), QVBoxLayout()
        add_student_button = QPushButton("Add New Student")
        add_student_button.clicked.connect(self.add_student)
        layout.addWidget(add_student_button)
        
        self.students_table = QTableWidget(columnCount=2)
        self.students_table.setHorizontalHeaderLabels(["Student ID", "Full Name"])
        self.students_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.students_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.students_table.customContextMenuRequested.connect(self.open_student_menu)
        layout.addWidget(self.students_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Manage Students")

    def create_manage_classes_tab(self):
        tab, layout = QWidget(), QVBoxLayout()
        form_layout = QFormLayout()
        self.class_name_input = QLineEdit()
        form_layout.addRow("Class Name:", self.class_name_input)
        
        add_class_button = QPushButton("Add Class")
        add_class_button.clicked.connect(self.add_class)
        form_layout.addWidget(add_class_button)
        layout.addLayout(form_layout)
        
        self.classes_table = QTableWidget(columnCount=2)
        self.classes_table.setHorizontalHeaderLabels(["Class ID", "Class Name"])
        self.classes_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.classes_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.classes_table.customContextMenuRequested.connect(self.open_class_menu)
        layout.addWidget(self.classes_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Manage Classes")

    def refresh_all_data(self):
        self.load_classes()
        self.load_students()
        self.load_students_for_attendance()
    
    def load_classes(self):
        classes = database.get_classes()
        self.class_selector_att.clear()
        self.class_selector_rep.clear()
        self.classes_table.setRowCount(0)
        for class_id, class_name in classes:
            self.class_selector_att.addItem(class_name, userData=class_id)
            self.class_selector_rep.addItem(class_name, userData=class_id)
            row = self.classes_table.rowCount()
            self.classes_table.insertRow(row)
            self.classes_table.setItem(row, 0, QTableWidgetItem(str(class_id)))
            self.classes_table.setItem(row, 1, QTableWidgetItem(class_name))

    def load_students(self):
        students = database.get_students()
        self.students_table.setRowCount(0)
        for student_id, full_name in students:
            row = self.students_table.rowCount()
            self.students_table.insertRow(row)
            self.students_table.setItem(row, 0, QTableWidgetItem(student_id))
            self.students_table.setItem(row, 1, QTableWidgetItem(full_name))

    def load_students_for_attendance(self):
        class_id = self.class_selector_att.currentData()
        if not class_id:
            self.attendance_table.setRowCount(0)
            return
        
        # Simplified: shows all students. For a real app, you'd use get_students_by_class(class_id).
        students = database.get_students()
        self.attendance_table.setRowCount(len(students))
        for row, (student_id, full_name) in enumerate(students):
            self.attendance_table.setItem(row, 0, QTableWidgetItem(student_id))
            self.attendance_table.setItem(row, 1, QTableWidgetItem(full_name))
            status_combo = QComboBox()
            status_combo.addItems(["Present", "Absent", "Late"])
            self.attendance_table.setCellWidget(row, 2, status_combo)

    def add_class(self):
        class_name = self.class_name_input.text().strip()
        if not class_name:
            QMessageBox.warning(self, "Input Error", "Class Name cannot be empty.")
            return
        if database.add_class(class_name):
            QMessageBox.information(self, "Success", f"Class '{class_name}' added.")
            self.class_name_input.clear()
            self.load_classes()
        else:
            QMessageBox.critical(self, "Database Error", f"Class '{class_name}' already exists.")

    def open_class_menu(self, position):
        menu = QMenu()
        edit_action = menu.addAction("Edit Class")
        delete_action = menu.addAction("Delete Class")
        action = menu.exec(self.classes_table.mapToGlobal(position))
        if action == edit_action:
            self.edit_class()
        elif action == delete_action:
            self.delete_class()

    def edit_class(self):
        row = self.classes_table.currentRow()
        if row < 0: return
        class_id = int(self.classes_table.item(row, 0).text())
        class_name = self.classes_table.item(row, 1).text()
        dialog = ClassDialog(class_name, self)
        if dialog.exec():
            new_name = dialog.get_data().strip()
            if new_name:
                database.update_class(class_id, new_name)
                self.load_classes()
                QMessageBox.information(self, "Success", "Class updated.")

    def delete_class(self):
        row = self.classes_table.currentRow()
        if row < 0: return
        class_id = int(self.classes_table.item(row, 0).text())
        class_name = self.classes_table.item(row, 1).text()
        confirm = QMessageBox.question(self, "Confirm Delete", 
            f"Delete class '{class_name}'? All related records will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            database.delete_class(class_id)
            self.refresh_all_data()
            QMessageBox.information(self, "Success", "Class deleted.")

    def add_student(self):
        dialog = StudentDialog(parent=self)
        if dialog.exec():
            student_id, full_name = dialog.get_data()
            if not student_id or not full_name:
                QMessageBox.warning(self, "Input Error", "All fields are required.")
                return
            if database.add_student(student_id, full_name):
                self.load_students()
                self.load_students_for_attendance()
                QMessageBox.information(self, "Success", "Student added.")
            else:
                QMessageBox.critical(self, "Database Error", "Student ID already exists.")

    def open_student_menu(self, position):
        menu = QMenu()
        edit_action = menu.addAction("Edit Student")
        delete_action = menu.addAction("Delete Student")
        action = menu.exec(self.students_table.mapToGlobal(position))
        if action == edit_action:
            self.edit_student()
        elif action == delete_action:
            self.delete_student()

    def edit_student(self):
        row = self.students_table.currentRow()
        if row < 0: return
        student_id = self.students_table.item(row, 0).text()
        full_name = self.students_table.item(row, 1).text()
        dialog = StudentDialog(student_id, full_name, self)
        if dialog.exec():
            _, new_full_name = dialog.get_data()
            database.update_student(student_id, new_full_name)
            self.refresh_all_data()
            QMessageBox.information(self, "Success", "Student details updated.")

    def delete_student(self):
        row = self.students_table.currentRow()
        if row < 0: return
        student_id = self.students_table.item(row, 0).text()
        confirm = QMessageBox.question(self, "Confirm Delete", 
            f"Delete student {student_id}? All related records will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            database.delete_student(student_id)
            self.load_students()
            self.load_students_for_attendance() # This line fixes the refresh bug
            QMessageBox.information(self, "Success", "Student deleted.")

    def save_attendance(self):
        class_id = self.class_selector_att.currentData()
        if not class_id:
            QMessageBox.warning(self, "Selection Error", "Please select a class.")
            return
        date_str = self.date_edit_att.date().toString("yyyy-MM-dd")
        for row in range(self.attendance_table.rowCount()):
            student_id = self.attendance_table.item(row, 0).text()
            status = self.attendance_table.cellWidget(row, 2).currentText()
            database.mark_attendance(student_id, class_id, date_str, status)
        QMessageBox.information(self, "Success", "Attendance saved successfully.")
        
    def generate_report(self):
        class_id = self.class_selector_rep.currentData()
        if not class_id:
            QMessageBox.warning(self, "Selection Error", "Please select a class.")
            return
        start_date = self.start_date_rep.date().toString("yyyy-MM-dd")
        end_date = self.end_date_rep.date().toString("yyyy-MM-dd")
        report_data = database.get_attendance_report(class_id, start_date, end_date)
        self.report_table.setRowCount(0)
        for row_data in report_data:
            row = self.report_table.rowCount()
            self.report_table.insertRow(row)
            for col, item in enumerate(row_data):
                self.report_table.setItem(row, col, QTableWidgetItem(str(item)))

    def export_report_to_csv(self):
        if self.report_table.rowCount() == 0:
            QMessageBox.warning(self, "Export Error", "No report data to export.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if path:
            try:
                with open(path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    headers = [self.report_table.horizontalHeaderItem(i).text() for i in range(self.report_table.columnCount())]
                    writer.writerow(headers)
                    for row in range(self.report_table.rowCount()):
                        row_data = [self.report_table.item(row, col).text() for col in range(self.report_table.columnCount())]
                        writer.writerow(row_data)
                QMessageBox.information(self, "Success", "Report exported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = AttendanceApp()
    main_window.show()
    sys.exit(app.exec())