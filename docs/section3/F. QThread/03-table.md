# Example: CSV Loader

## New Concepts in This Example

### 1. **File I/O in Background Threads**

```python
# Reading CSV file in worker thread - NOT in main thread
with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Read header row
    for row in csv_reader:  # Read data rows
        data_rows.append(row)
```

**Key point:** File operations can be slow, especially for large files, so they belong in background threads.

### 2. **Progress Calculation for Real Tasks**

```python
# First pass: count rows for progress calculation
total_rows = sum(1 for row in csv_reader) - 1

# Second pass: update progress as we read
progress = 30 + int((row_index / total_rows) * 60)
self.progress_update.emit(min(progress, 90))
```

**Key point:** Real progress bars require knowing the total work upfront.

### 3. **Complex Data Transfer Between Threads**

```python
# Signal carries both headers and data
data_loaded = pyqtSignal(list, list)

# Emit complex data structure
self.data_loaded.emit(headers, data_rows)
```

**Important concept:** Signals can carry multiple parameters and complex data types.

### 4. **QTableWidget Population**

```python
def populate_table(self, headers, data_rows):
    # Set table dimensions
    self.table.setColumnCount(len(headers))
    self.table.setRowCount(len(data_rows))

    # Set headers
    self.table.setHorizontalHeaderLabels(headers)

    # Populate each cell
    for row_index, row_data in enumerate(data_rows):
        for col_index, cell_data in enumerate(row_data):
            item = QTableWidgetItem(str(cell_data))
            self.table.setItem(row_index, col_index, item)
```

**New GUI concept:** How to programmatically populate tables with dynamic data.

### 5. **File Dialog Integration**

```python
file_path, _ = QFileDialog.getOpenFileName(
    self,
    "Select CSV File",
    "",
    "CSV Files (*.csv);;All Files (*)"
)
```

**Practical skill:** Let users select files instead of hardcoding file paths.

### 6. **Error Handling in Background Threads**

```python
try:
# File operations
except FileNotFoundError:
    self.error_occurred.emit(f"File not found: {self.file_path}")
except PermissionError:
    self.error_occurred.emit(f"Permission denied: {self.file_path}")
except UnicodeDecodeError:
    self.error_occurred.emit("Unable to decode file...")
```

**Important pattern:** Handle errors in worker thread, report them via signals.

### 7. **UI State Management for File Operations**

```python
def load_csv_file(self, file_path):
    # Disable buttons during loading
    self.load_button.setEnabled(False)
    self.clear_button.setEnabled(False)

    # Show progress bar
    self.progress_bar.setVisible(True)

    # Clear existing data
    self.table.setRowCount(0)
```

**UX principle:** Always give visual feedback and prevent conflicting user actions.

## What To Learn From This Example

1. **Real-world file handling** - CSV files are common in business applications
2. **Progressive enhancement** - Start with basic threading, add file I/O, progress, error handling
3. **Data visualization** - How to display structured data in tables
4. **User experience** - File dialogs, progress bars, error messages
5. **Practical patterns** - Two-pass file reading (count then process)

## Running the Example

The app includes a `create_sample_csv()` function that generates test data, so we can run it immediately without
needing our own CSV files.

**Features to demonstrate:**

- Click "Load CSV File" to see the file dialog
- Watch the progress bar during loading
- See the data populate in the table
- Try clicking buttons while loading (they're disabled)
- Use the "Clear Table" button
- The table supports sorting by clicking column headers

## Full code

```python
import sys
import csv
import time
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QProgressBar,
                             QTableWidget, QTableWidgetItem, QFileDialog,
                             QMessageBox, QHeaderView)


class CSVLoaderThread(QThread):
    """Background thread for loading CSV files"""

    # Signals for communication with main thread
    progress_update = pyqtSignal(int)  # Progress percentage
    status_update = pyqtSignal(str)  # Status messages
    data_loaded = pyqtSignal(list, list)  # Headers and data rows
    error_occurred = pyqtSignal(str)  # Error messages

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        """Load CSV file in background thread"""
        try:
            self.status_update.emit("Opening file...")
            self.progress_update.emit(10)

            # Simulate some processing time
            time.sleep(0.5)

            # First pass: count total rows for progress calculation
            self.status_update.emit("Analyzing file structure...")
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                total_rows = sum(1 for row in csv_reader) - 1  # Subtract header row

            self.progress_update.emit(20)
            time.sleep(0.2)

            # Second pass: actually read the data
            self.status_update.emit("Reading CSV data...")
            headers = []
            data_rows = []

            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)

                # Read header row
                headers = next(csv_reader)
                self.progress_update.emit(30)

                # Read data rows with progress updates
                for row_index, row in enumerate(csv_reader):
                    data_rows.append(row)

                    # Update progress every 100 rows or so
                    if row_index % max(1, total_rows // 10) == 0:
                        progress = 30 + int((row_index / total_rows) * 60)
                        self.progress_update.emit(min(progress, 90))
                        self.status_update.emit(f"Loading row {row_index + 1} of {total_rows}")

                    # Small delay to make progress visible (remove in real apps)
                    if row_index % 50 == 0:
                        time.sleep(0.01)

            self.progress_update.emit(95)
            self.status_update.emit("Finalizing data...")
            time.sleep(0.2)

            # Send the loaded data to main thread
            self.data_loaded.emit(headers, data_rows)
            self.progress_update.emit(100)
            self.status_update.emit(f"Successfully loaded {len(data_rows)} rows")

        except FileNotFoundError:
            self.error_occurred.emit(f"File not found: {self.file_path}")
        except PermissionError:
            self.error_occurred.emit(f"Permission denied: {self.file_path}")
        except UnicodeDecodeError:
            self.error_occurred.emit("Unable to decode file. Please ensure it's a valid CSV file with UTF-8 encoding.")
        except Exception as e:
            self.error_occurred.emit(f"Error loading CSV: {str(e)}")


class CSVLoaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loader_thread = None
        self.init_ui()

    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Control panel
        control_layout = QHBoxLayout()

        self.load_button = QPushButton("Load CSV File")
        self.load_button.clicked.connect(self.select_and_load_file)

        self.clear_button = QPushButton("Clear Table")
        self.clear_button.clicked.connect(self.clear_table)
        self.clear_button.setEnabled(False)

        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.clear_button)
        control_layout.addStretch()  # Push buttons to the left

        main_layout.addLayout(control_layout)

        # Status and progress section
        self.status_label = QLabel("Ready to load CSV file")
        main_layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)  # Hide initially
        main_layout.addWidget(self.progress_bar)

        # Data table
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)  # Allow column sorting

        # Make table headers stretch to fill width
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        main_layout.addWidget(self.table)

        # File info label
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: gray; font-size: 10px;")
        main_layout.addWidget(self.info_label)

        # Window settings
        self.setWindowTitle("CSV File Loader - Background Threading Demo")
        self.setGeometry(200, 200, 800, 600)

    def select_and_load_file(self):
        """Open file dialog and load selected CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            self.load_csv_file(file_path)

    def load_csv_file(self, file_path):
        """Start loading CSV file in background thread"""
        # Update UI state
        self.load_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Clear existing table data
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        # Create and start loader thread
        self.loader_thread = CSVLoaderThread(file_path)

        # Connect signals
        self.loader_thread.progress_update.connect(self.update_progress)
        self.loader_thread.status_update.connect(self.update_status)
        self.loader_thread.data_loaded.connect(self.populate_table)
        self.loader_thread.error_occurred.connect(self.handle_error)
        self.loader_thread.finished.connect(self.loading_finished)

        # Start the background loading
        self.loader_thread.start()

        # Update info label
        self.info_label.setText(f"Loading: {file_path}")

    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)

    def update_status(self, message):
        """Update status label"""
        self.status_label.setText(message)

    def populate_table(self, headers, data_rows):
        """Populate the table with loaded data (runs in main thread)"""
        # Set up table dimensions
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(data_rows))

        # Set headers
        self.table.setHorizontalHeaderLabels(headers)

        # Populate data
        for row_index, row_data in enumerate(data_rows):
            for col_index, cell_data in enumerate(row_data):
                # Ensure we don't go beyond the number of columns
                if col_index < len(headers):
                    item = QTableWidgetItem(str(cell_data))
                    self.table.setItem(row_index, col_index, item)

        # Update info
        self.info_label.setText(
            f"Loaded {len(data_rows)} rows × {len(headers)} columns"
        )

        self.clear_button.setEnabled(True)

    def handle_error(self, error_message):
        """Handle loading errors"""
        QMessageBox.critical(self, "Error Loading CSV", error_message)
        self.status_label.setText("Error occurred while loading file")
        self.info_label.setText("No file loaded")

    def loading_finished(self):
        """Clean up after loading is complete"""
        # Reset UI state
        self.load_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        # Clean up thread
        self.loader_thread = None

    def clear_table(self):
        """Clear the table data"""
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.clear_button.setEnabled(False)
        self.status_label.setText("Table cleared")
        self.info_label.setText("No file loaded")


def create_sample_csv():
    """Create a sample CSV file for testing"""
    sample_data = [
        ["Name", "Age", "City", "Department", "Salary"],
        ["Alice Johnson", "28", "New York", "Engineering", "75000"],
        ["Bob Smith", "34", "San Francisco", "Marketing", "68000"],
        ["Carol Davis", "31", "Chicago", "Sales", "62000"],
        ["David Wilson", "29", "Boston", "Engineering", "78000"],
        ["Eva Brown", "26", "Seattle", "Design", "65000"],
        ["Frank Miller", "35", "Los Angeles", "Management", "95000"],
        ["Grace Lee", "30", "Denver", "Engineering", "72000"],
        ["Henry Taylor", "32", "Miami", "Sales", "58000"],
        ["Ivy Chen", "27", "Portland", "Marketing", "64000"],
        ["Jack Robinson", "33", "Austin", "Engineering", "76000"]
    ]

    with open("sample_employees.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)

    print("Created sample_employees.csv for testing")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create sample CSV file for testing
    create_sample_csv()

    window = CSVLoaderApp()
    window.show()

    sys.exit(app.exec())
```

---------------

??? info "Use of AI"
    Page written in part with the help of an AI assistant, mainly using Perplexity AI. The AI was used to generate
    explanations, examples and/or structure suggestions. All information has been verified, edited and completed by
    the author.