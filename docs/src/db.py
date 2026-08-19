import sys
import time
import psycopg2
from psycopg2 import Error
from textwrap import dedent
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QTabWidget,
    QProgressBar, QTextEdit, QGroupBox, QLineEdit, QSpinBox,
    QMessageBox, QHeaderView, QSplitter, QFormLayout, QSizePolicy
)

class DatabaseQueryThread(QThread):
    """Background thread for executing database queries"""

    # Signals for communication with main thread
    progress_update = Signal(int)
    status_update = Signal(str)
    data_loaded = Signal(list, list)  # headers, rows
    error_occurred = Signal(str)
    log_message = Signal(str)

    def __init__(self, connection_params, query, query_params=None):
        super().__init__()
        self.connection_params = connection_params
        self.query = query
        self.query_params = query_params or ()
        self.is_cancelled = False

    def cancel(self):
        """Request cooperative cancellation"""
        self.is_cancelled = True
        self.log_message.emit("Query cancellation requested")

    def run(self):
        """Execute the database query"""
        connection = None
        cursor = None

        try:
            if self.is_cancelled:
                return

            self.log_message.emit("Starting database query execution")
            self.status_update.emit("Connecting to database...")
            self.progress_update.emit(10)

            # Simulate connection time
            time.sleep(0.5)

            if self.is_cancelled:
                self.log_message.emit("Query cancelled before connection")
                return

            # Connect to database
            connection = psycopg2.connect(**self.connection_params)
            cursor = connection.cursor()

            self.status_update.emit("Executing query...")
            self.progress_update.emit(30)
            self.log_message.emit(f"Executing query: {self.query[:100]}...")

            # Execute query
            cursor.execute(self.query, self.query_params)

            if self.is_cancelled:
                self.log_message.emit("Query cancelled after execution")
                return

            self.status_update.emit("Fetching results...")
            self.progress_update.emit(60)

            # Get column names
            if cursor.description:
                headers = [desc[0] for desc in cursor.description]

                # Fetch all results
                rows = cursor.fetchall()

                self.progress_update.emit(90)
                self.status_update.emit("Processing results...")

                # Convert rows to strings for table display
                formatted_rows = []
                for row in rows:
                    formatted_row = []
                    for item in row:
                        if item is None:
                            formatted_row.append("")
                        else:
                            formatted_row.append(str(item))
                    formatted_rows.append(formatted_row)

                if self.is_cancelled:
                    self.log_message.emit("Query cancelled during result processing")
                    return

                self.progress_update.emit(100)
                self.status_update.emit(f"Query completed - {len(formatted_rows)} rows returned")
                self.log_message.emit(f"Successfully retrieved {len(formatted_rows)} rows")

                # Send results to main thread
                self.data_loaded.emit(headers, formatted_rows)
            else:
                # Query returned no results (like INSERT, UPDATE, DELETE)
                self.status_update.emit("Query executed successfully (no results)")
                self.log_message.emit("Query executed - no result set returned")
                self.data_loaded.emit([], [])

        except psycopg2.OperationalError as e:
            error_msg = f"Database connection error: {str(e)}"
            self.error_occurred.emit(error_msg)
            self.log_message.emit(f"Connection error: {str(e)}")

        except psycopg2.ProgrammingError as e:
            error_msg = f"SQL syntax error: {str(e)}"
            self.error_occurred.emit(error_msg)
            self.log_message.emit(f"SQL error: {str(e)}")

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.error_occurred.emit(error_msg)
            self.log_message.emit(f"Unexpected error: {str(e)}")

        finally:
            # Clean up database resources
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            self.log_message.emit("Database connection closed")


class DatabaseConnectionWidget(QWidget):
    """Widget for database connection configuration"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        # Connection parameters with defaults
        self.host_edit = QLineEdit("localhost")
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.port_spin.setValue(5432)

        self.database_edit = QLineEdit("northwind")
        self.schema_edit = QLineEdit("public")
        self.username_edit = QLineEdit("postgres")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        # Add fields to layout
        layout.addRow("Host:", self.host_edit)
        layout.addRow("Port:", self.port_spin)
        layout.addRow("Database:", self.database_edit)
        layout.addRow("Schema:", self.schema_edit)
        layout.addRow("Username:", self.username_edit)
        layout.addRow("Password:", self.password_edit)

        # Test connection button
        self.test_button = QPushButton("Test Connection")
        self.test_button.clicked.connect(self.test_connection)
        layout.addRow("", self.test_button)

        self.setLayout(layout)

    def get_connection_params(self):
        """Get connection parameters as dictionary"""
        return {
            "host": self.host_edit.text().strip(),
            "port": self.port_spin.value(),
            "database": self.database_edit.text().strip(),
            "user": self.username_edit.text().strip(),
            "password": self.password_edit.text(),
            "options": f"-c search_path={self.schema_edit.text().strip()}"
        }

    def test_connection(self):
        """Test database connection"""
        try:
            params = self.get_connection_params()
            connection = psycopg2.connect(**params)

            # Test schema access by checking if we can query pg_tables
            cursor = connection.cursor()
            cursor.execute("SELECT schemaname FROM pg_tables WHERE schemaname = current_schema() LIMIT 1;")
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            schema_name = self.schema_edit.text().strip()
            if result:
                QMessageBox.information(self, "Success",
                                        f"Database connection successful!\nActive schema: {schema_name}")
            else:
                QMessageBox.warning(self, "Connection Successful",
                                    f"Connected to database, but schema '{schema_name}' may not exist or be accessible.")

        except Exception as e:
            QMessageBox.critical(self, "Connection Failed", f"Failed to connect:\n{str(e)}")


class QueryTabWidget(QWidget):
    """Widget for a single query tab"""

    def __init__(self, title, description, query, parent_app):
        super().__init__()
        self.title = title
        self.description = description
        self.query = query
        self.parent_app = parent_app
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Query description
        desc_label = QLabel(self.description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        desc_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addWidget(desc_label)

        # Show the SQL query - give it most of the space
        query_group = QGroupBox("SQL Query:")
        query_layout = QVBoxLayout()

        query_text = QTextEdit()
        query_text.setPlainText(self.query)
        query_text.setReadOnly(True)
        query_text.setStyleSheet("font-family: 'Source Code Pro', monospace")

        # Set size policy to expand and take available space
        query_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        query_layout.addWidget(query_text)
        query_group.setLayout(query_layout)

        # Give the query group a stretch factor so it expands
        layout.addWidget(query_group, stretch=1)

        # Run button - keep it fixed size
        self.run_button = QPushButton(f"Run {self.title}")
        self.run_button.clicked.connect(self.run_query)
        self.run_button.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; font-weight: bold; padding: 8px; }")
        self.run_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.run_button)

        # Remove the addStretch() - we want the query text to take the space instead
        self.setLayout(layout)

    def run_query(self):
        """Execute this query"""
        self.parent_app.execute_query(self.query, self.title)


class NorthwindQueryApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.query_thread = None
        self.shutdown_in_progress = False

        # Predefined queries for the Northwind database
        self.queries = {
            "Categories": {
                "description": "Display all product categories with their descriptions",
                "query": "SELECT category_id, category_name, description FROM categories ORDER BY category_name;"
            },
            "Products by Category": {
                "description": "Show products grouped by category with pricing information",
                "query": dedent("""
                                SELECT c.category_name, p.product_name, p.unit_price, p.units_in_stock
                                FROM products p
                                         JOIN categories c ON p.category_id = c.category_id
                                ORDER BY c.category_name, p.product_name;""").strip()
            },
            "Customer Summary": {
                "description": "List all customers with their contact information",
                "query": dedent("""
                                SELECT customer_id, company_name, contact_name, city, country
                                FROM customers
                                ORDER BY company_name;""").strip()
            },
            "Employee Details": {
                "description": "Show employee information including their managers",
                "query": dedent("""
                                SELECT e1.employee_id,
                                       e1.first_name,
                                       e1.last_name,
                                       e1.title,
                                       e2.first_name || ' ' || e2.last_name as manager_name
                                FROM employees e1
                                         LEFT JOIN employees e2 ON e1.reports_to = e2.employee_id
                                ORDER BY e1.last_name, e1.first_name;""").strip()
            },
            "Top Products": {
                "description": "Find the most expensive products in stock",
                "query": dedent("""
                                SELECT product_name,
                                       unit_price,
                                       units_in_stock,
                                       (unit_price * units_in_stock) as inventory_value
                                FROM products
                                WHERE units_in_stock > 0
                                ORDER BY unit_price DESC
                                LIMIT 10;""").strip()
            },
            "Order Statistics": {
                "description": "Summary statistics about orders by year",
                "query": dedent("""
                                SELECT EXTRACT(YEAR FROM order_date) as order_year,
                                       COUNT(*)                      as total_orders,
                                       AVG(freight)                  as avg_freight,
                                       MIN(order_date)               as first_order,
                                       MAX(order_date)               as last_order
                                FROM orders
                                WHERE order_date IS NOT NULL
                                GROUP BY EXTRACT(YEAR FROM order_date)
                                ORDER BY order_year;""").strip()
            }
        }

        self.init_ui()

    def init_ui(self):
        # Create central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Create splitter to divide connection panel and query area
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel: Database connection
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Connection group
        conn_group = QGroupBox("Database Connection")
        self.connection_widget = DatabaseConnectionWidget()
        conn_group_layout = QVBoxLayout()
        conn_group_layout.addWidget(self.connection_widget)
        conn_group.setLayout(conn_group_layout)
        left_layout.addWidget(conn_group)

        # Log group
        log_group = QGroupBox("Query Log")
        self.log_display = QTextEdit()
        # self.log_display.setMaximumHeight(200)
        self.log_display.setReadOnly(True)
        log_group_layout = QVBoxLayout()
        log_group_layout.addWidget(self.log_display)
        log_group.setLayout(log_group_layout)
        left_layout.addWidget(log_group)

        # left_layout.addStretch()
        splitter.addWidget(left_panel)

        # Right panel: Query tabs and results with vertical splitter
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        # Top section: Query tabs
        query_panel = QWidget()
        query_layout = QVBoxLayout(query_panel)
        query_layout.setContentsMargins(0, 0, 0, 0)

        self.query_tabs = QTabWidget()
        self.create_query_tabs()
        query_layout.addWidget(self.query_tabs)

        right_splitter.addWidget(query_panel)

        # Bottom section: Status, progress, and results
        results_panel = QWidget()
        results_layout = QVBoxLayout(results_panel)
        results_layout.setContentsMargins(0, 0, 0, 0)

        # Status and progress
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Ready to execute queries")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.cancel_button = QPushButton("Cancel Query")
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(self.cancel_query)

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(self.cancel_button)
        results_layout.addLayout(status_layout)

        # Results table
        results_group = QGroupBox("Query Results")
        self.results_table = QTableWidget()
        self.results_table.setSortingEnabled(True)

        # Configure table headers
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)

        results_table_layout = QVBoxLayout()
        results_table_layout.addWidget(self.results_table)
        results_group.setLayout(results_table_layout)
        results_layout.addWidget(results_group)

        right_splitter.addWidget(results_panel)

        # Set initial proportions for right splitter (query tabs vs results)
        right_splitter.setSizes([300, 500])

        splitter.addWidget(right_splitter)

        # Set splitter proportions
        splitter.setSizes([300, 700])

        # Window settings
        self.setWindowTitle("Northwind Database Query Application")
        self.setGeometry(100, 100, 1200, 800)

        # Add initial log message
        self.add_log_message("Application started - configure database connection and select a query")

    def create_query_tabs(self):
        """Create tabs for each predefined query"""
        for title, query_info in self.queries.items():
            tab = QueryTabWidget(
                title,
                query_info["description"],
                query_info["query"],
                self
            )
            self.query_tabs.addTab(tab, title)

    def execute_query(self, query, query_name):
        """Execute a database query in background thread"""
        # Get connection parameters
        connection_params = self.connection_widget.get_connection_params()

        # Validate connection parameters
        if not all([connection_params["host"], connection_params["database"],
                    connection_params["user"]]):
            QMessageBox.warning(self, "Invalid Configuration",
                                "Please fill in all required connection fields (host, database, username).")
            return

        # Clear previous results
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(0)

        # Update UI state
        self.update_ui_for_query_start()

        # Create and start query thread
        self.query_thread = DatabaseQueryThread(connection_params, query)

        # Connect signals
        self.query_thread.progress_update.connect(self.update_progress)
        self.query_thread.status_update.connect(self.update_status)
        self.query_thread.data_loaded.connect(self.populate_results)
        self.query_thread.error_occurred.connect(self.handle_query_error)
        self.query_thread.log_message.connect(self.add_log_message)
        self.query_thread.finished.connect(self.query_finished)

        # Start the query
        self.query_thread.start()
        self.add_log_message(f"=== Starting query: {query_name} ===")

    def update_ui_for_query_start(self):
        """Update UI when query starts"""
        # Disable all run buttons
        for i in range(self.query_tabs.count()):
            tab = self.query_tabs.widget(i)
            tab.run_button.setEnabled(False)

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.cancel_button.setVisible(True)

    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)

    def update_status(self, message):
        """Update status label"""
        self.status_label.setText(message)

    def populate_results(self, headers, rows):
        """Populate results table with query data"""
        if not headers:
            self.add_log_message("Query executed successfully (no result set)")
            return

        # Set up table
        self.results_table.setColumnCount(len(headers))
        self.results_table.setRowCount(len(rows))
        self.results_table.setHorizontalHeaderLabels(headers)

        # Populate data
        for row_index, row_data in enumerate(rows):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.results_table.setItem(row_index, col_index, item)

        # Resize columns to content
        self.results_table.resizeColumnsToContents()

        self.add_log_message(f"Results displayed: {len(rows)} rows × {len(headers)} columns")

    def handle_query_error(self, error_message):
        """Handle query execution errors"""
        QMessageBox.critical(self, "Query Error", error_message)
        self.add_log_message(f"ERROR: {error_message}")

    def cancel_query(self):
        """Cancel the running query"""
        if self.query_thread and self.query_thread.isRunning():
            self.add_log_message("Requesting query cancellation...")
            self.query_thread.cancel()

    def query_finished(self):
        """Clean up after query completion"""
        # Re-enable all run buttons
        for i in range(self.query_tabs.count()):
            tab = self.query_tabs.widget(i)
            tab.run_button.setEnabled(True)

        self.progress_bar.setVisible(False)
        self.cancel_button.setVisible(False)
        self.query_thread = None

        if not self.shutdown_in_progress:
            self.status_label.setText("Ready to execute queries")
            self.add_log_message("=== Query completed ===")

    def add_log_message(self, message):
        """Add timestamped message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_display.append(log_entry)

        # Force immediate display update
        QApplication.processEvents()

    def closeEvent(self, event):
        """Handle application shutdown with graceful thread termination"""
        # If no thread is running, close immediately
        if not self.query_thread or not self.query_thread.isRunning():
            self.add_log_message("No background queries running - closing application")
            event.accept()
            return

        self.shutdown_in_progress = True
        self.add_log_message("=== APPLICATION SHUTDOWN REQUESTED ===")
        self.add_log_message("Background query detected - attempting graceful shutdown...")

        # STEP 1: Try cooperative cancellation
        self.add_log_message("Step 1: Requesting cooperative cancellation...")
        self.query_thread.cancel()

        # Wait for cooperative shutdown
        self.add_log_message("Waiting up to 3 seconds for query to stop...")
        if self.query_thread.wait(3000):  # 3 seconds
            self.add_log_message("✓ Query stopped cooperatively - closing application")
            event.accept()
            return

        self.add_log_message("✗ Cooperative cancellation failed")

        # STEP 2: Try quit() signal
        self.add_log_message("Step 2: Sending quit signal to thread...")
        self.query_thread.quit()

        # Wait for quit signal to work
        self.add_log_message("Waiting up to 2 seconds for quit signal response...")
        if self.query_thread.wait(2000):  # 2 seconds
            self.add_log_message("✓ Query stopped after quit signal - closing application")
            event.accept()
            return

        self.add_log_message("✗ Quit signal failed")

        # STEP 3: Ask user for permission to force terminate
        self.add_log_message("Step 3: Query is unresponsive - asking user for permission to force terminate")

        reply = QMessageBox.question(
            self,
            "Force Terminate Query?",
            "The database query is not responding to shutdown requests.\n\n"
            "Force terminate the query thread?\n"
            "⚠️ Warning: This may leave database connections open.\n\n"
            "Choose:\n"
            "• Yes: Force terminate and close\n"
            "• No: Cancel shutdown and wait",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # STEP 4: Force termination
            self.add_log_message("⚠️ FORCE TERMINATING QUERY THREAD ⚠️")
            self.query_thread.terminate()

            # Wait for termination to complete
            if self.query_thread.wait(1000):  # 1 second
                self.add_log_message("✓ Thread force terminated - closing application")
            else:
                self.add_log_message("⚠️ Thread termination may not have completed cleanly")

            event.accept()
        else:
            # User chose to cancel shutdown
            self.add_log_message("User cancelled shutdown - application will remain open")
            self.add_log_message("Query is still running - you may need to wait or try closing again")
            self.shutdown_in_progress = False
            event.ignore()


def main():
    app = QApplication(sys.argv)

    # Create and show the main window
    window = NorthwindQueryApp()
    window.show()

    print("Northwind Database Query Application")
    print("=====================================")
    print("1. Configure database connection in the left panel")
    print("2. Test the connection")
    print("3. Select a query tab and click 'Run'")
    print("4. View results in the table below")
    print("5. Try closing the app while a query is running to see graceful shutdown")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
