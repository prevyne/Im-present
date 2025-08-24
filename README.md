# Im-present: Class Attendance System
Im-present is a modern, intuitive desktop application designed to simplify the process of tracking student attendance. Built with Python and PyQt6, it provides a clean, colorful interface for managing students, classes, and attendance records efficiently.

 ## Features
Full Student Management: Add, edit, and delete student profiles with ease.

Complete Class Management: Create, update, and delete classes.

Daily Attendance Tracking: Mark attendance for each student with "Present," "Absent," or "Late" statuses for any given day.

Powerful Reporting: Generate detailed attendance reports for specific classes within a selected date range.

Export to CSV: Export generated reports to a .csv file for easy use in spreadsheet software like Excel or Google Sheets.

Modern Themed UI: A visually appealing dark theme with vibrant colors makes the application pleasant to use.

Persistent Storage: All data is saved locally in an SQLite database (attendance.db), ensuring your information is preserved between sessions.

# Getting Started
Follow these instructions to get the application running on your local machine.

## Prerequisites
You will need the following software installed on your system:

Python 3: Version 3.6 or newer.

PyQt6: The UI framework used by the application.

You can install the required Python library using pip:

pip install PyQt6

## How to Run
Clone or download the project files (main.py and database.py) into a single directory.

Open your terminal or command prompt.

Navigate to the directory where you saved the files.

cd path/to/your/project/folder

Run the application using the Python 3 interpreter:

python3 main.py

The application window should now appear on your screen. The first time you run it, a new database file named attendance.db will be created automatically in the same folder.

 ## Usage Guide
 Managing Students
Go to the "Manage Students" tab.

Add: Click the "Add New Student" button, fill in the details in the dialog, and click "Ok".

Edit/Delete: Right-click on a student in the table to bring up a context menu with "Edit Student" and "Delete Student" options.

### Managing Classes
Go to the "Manage Classes" tab.

Add: Type the class name into the input field and click the "Add Class" button.

Edit/Delete: Right-click on a class in the table to open a context menu with "Edit Class" and "Delete Class" options.

### Taking Attendance
Go to the "Take Attendance" tab.

Select the desired class from the dropdown menu.

Choose the correct date.

For each student, select their status ("Present", "Absent", "Late") from the dropdown in the "Status" column.

Click the "Save Attendance" button to record the data.

### Generating Reports
Go to the "Reports" tab.

Select the class you want a report for.

Choose the start and end dates for the report period.

Click the "Generate Report" button. The attendance records will appear in the table.

To save the report, click the "Export to CSV" button and choose a location to save the file.

 Project Files
main.py: Contains all the code for the user interface, application logic, and event handling.

database.py: Manages all interactions with the SQLite database, including creating tables and performing CRUD operations.

attendance.db: The SQLite database file where all student, class, and attendance data is stored. This file is created automatically when you first run the application.