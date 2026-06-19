# Graduated Shutdown

The graduated shutdown approach in `closeEvent` is the professional way to handle application shutdown. Here's what 
the example demonstrates:

## The Three-Step Graceful Shutdown Process:

### **Step 1: Cooperative Cancellation (3 seconds)**

```python
self.worker_thread.cancel()  # Set the cancellation flag
if self.worker_thread.wait(3000):  # Wait 3 seconds
# Thread stopped nicely - we're done!
```

### **Step 2: Quit Signal (2 seconds)**

```python
self.worker_thread.quit()  # Send quit signal to event loop
if self.worker_thread.wait(2000):  # Wait 2 seconds
# Thread responded to quit - we're done!
```

### **Step 3: User Choice + Force Termination**

```python
# Ask user permission first!
reply = QMessageBox.question(self, "Force Terminate?", ...)

if reply == Yes:
    self.worker_thread.terminate()  # Force kill
    self.worker_thread.wait(1000)  # Wait for cleanup
```

## Key Points:

### **1. Graduated Response Times**

- **3 seconds** for cooperative (longest, most gentle)
- **2 seconds** for quit signal (shorter, more urgent)
- **1 second** for termination cleanup (just cleanup time)

### **2. User Involvement**

- Don't force terminate without asking the user
- Users should understand the consequences
- Give them the option to cancel shutdown and wait

### **3. Proper Event Handling**

```python
event.accept()  # Allow the close
event.ignore()  # Cancel the close
```

### **4. State Management**

- Track `shutdown_in_progress` to avoid duplicate logs
- Continue logging throughout the process
- Use `QApplication.processEvents()` to ensure UI updates

## Why This Approach is Superior:

**For Well-Behaved Threads:**

- Step 1 (cooperative) succeeds → fast, clean shutdown
- No force termination needed

**For Moderately Problematic Threads:**

- Step 1 fails, but Step 2 (quit) succeeds
- Still avoids dangerous force termination

**For Truly Stuck Threads:**

- Both steps fail → user gets to decide
- User understands the risk before force termination
- Application doesn't just hang forever

## Real-World Applications:

This pattern is essential for:

- **File processing applications** (don't corrupt files)
- **Network applications** (close connections cleanly)
- **Data analysis tools** (save intermediate results)
- **Any professional software** (users expect graceful shutdown)

The example shows both cooperative and stubborn workers, so we can test both scenarios and see how the graduated
approach handles each case appropriately.

## Full Code

```python
import sys
import time
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QTextEdit, QProgressBar,
                             QMessageBox)


class LongRunningWorker(QThread):
    """Worker thread that can be cancelled cooperatively"""

    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    log_message = pyqtSignal(str)

    def __init__(self, task_duration=20):
        super().__init__()
        self.task_duration = task_duration
        self.is_cancelled = False

    def cancel(self):
        """Request cooperative cancellation"""
        self.is_cancelled = True

    def run(self):
        """Long running task that checks for cancellation"""
        self.log_message.emit("Worker thread started")

        for i in range(self.task_duration):
            # Check for cancellation request
            if self.is_cancelled:
                self.log_message.emit("Worker thread cancelled cooperatively")
                self.status_update.emit("Task cancelled")
                return

            # Simulate work
            time.sleep(1)
            progress = int(((i + 1) / self.task_duration) * 100)
            self.progress_update.emit(progress)
            self.status_update.emit(f"Working... {i + 1}/{self.task_duration}")

            if i % 3 == 0:  # Log every few steps
                self.log_message.emit(f"Completed step {i + 1}")

        self.log_message.emit("Worker thread completed normally")
        self.status_update.emit("Task completed!")


class GracefulShutdownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.shutdown_in_progress = False
        self.init_ui()

    def init_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Graceful Shutdown Demo")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Status display
        self.status_label = QLabel("Ready to start task")
        layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Control buttons
        self.start_button = QPushButton("Start Long Task (20 seconds)")
        self.cancel_button = QPushButton("Cancel Task")
        self.cancel_button.setEnabled(False)

        self.start_button.clicked.connect(self.start_task)
        self.cancel_button.clicked.connect(self.cancel_task)

        layout.addWidget(self.start_button)
        layout.addWidget(self.cancel_button)

        # Instructions
        instructions = QLabel("""
Instructions:
1. Click 'Start Long Task' to begin a 20-second background task
2. Try closing the window while the task is running
3. Observe the graceful shutdown process in the log below
        """)
        instructions.setStyleSheet("margin: 10px; padding: 10px;")
        layout.addWidget(instructions)

        # Log display
        log_label = QLabel("Shutdown Process Log:")
        layout.addWidget(log_label)

        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(200)
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        # Window settings
        self.setWindowTitle("Graceful Shutdown Example")
        self.setGeometry(300, 300, 600, 500)

    def start_task(self):
        """Start the background task"""
        self.log_display.clear()
        self.add_log_message("=== Starting new task ===")

        # Update UI
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Create and start worker
        self.worker_thread = LongRunningWorker()
        # self.worker_thread = StubbornWorker()  # Uncomment to test with stubborn worker that ignores cancellation

        # Connect signals
        self.worker_thread.progress_update.connect(self.update_progress)
        self.worker_thread.status_update.connect(self.update_status)
        self.worker_thread.log_message.connect(self.add_log_message)
        self.worker_thread.finished.connect(self.task_finished)

        # Start thread
        self.worker_thread.start()

    def cancel_task(self):
        """Cancel the running task"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.add_log_message("Requesting task cancellation...")
            self.worker_thread.cancel()

    def task_finished(self):
        """Handle task completion"""
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.worker_thread = None

        if not self.shutdown_in_progress:
            self.add_log_message("=== Task ended ===")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.status_label.setText(message)

    def add_log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_display.append(log_entry)

        # Force immediate display update
        QApplication.processEvents()

    def closeEvent(self, event):
        """
        Handle application shutdown with graduated thread termination approach
        """
        # If no thread is running, close immediately
        if not self.worker_thread or not self.worker_thread.isRunning():
            self.add_log_message("No background tasks running - closing immediately")
            event.accept()
            return

        self.shutdown_in_progress = True
        self.add_log_message("=== APPLICATION SHUTDOWN REQUESTED ===")
        self.add_log_message("Background thread detected - attempting graceful shutdown...")

        # STEP 1: Try cooperative cancellation
        self.add_log_message("Step 1: Requesting cooperative cancellation...")
        self.worker_thread.cancel()

        # Wait for cooperative shutdown (give it a reasonable time)
        self.add_log_message("Waiting up to 3 seconds for cooperative shutdown...")
        if self.worker_thread.wait(3000):  # 3 seconds
            self.add_log_message("✓ Thread stopped cooperatively - closing application")
            event.accept()
            return

        self.add_log_message("✗ Cooperative cancellation failed")

        # STEP 2: Try quit() signal
        self.add_log_message("Step 2: Sending quit signal to thread...")
        self.worker_thread.quit()

        # Wait for quit signal to work
        self.add_log_message("Waiting up to 2 seconds for quit signal response...")
        if self.worker_thread.wait(2000):  # 2 seconds
            self.add_log_message("✓ Thread stopped after quit signal - closing application")
            event.accept()
            return

        self.add_log_message("✗ Quit signal failed")

        # STEP 3: Ask user if they want to force terminate
        self.add_log_message("Step 3: Thread is unresponsive - asking user for permission to force terminate")

        reply = QMessageBox.question(
            self,
            "Force Terminate Thread?",
            "The background task is not responding to shutdown requests.\n\n"
            "Force terminate the thread?\n"
            "⚠️ Warning: This may cause data loss or corruption.\n\n"
            "Choose:\n"
            "• Yes: Force terminate and close\n"
            "• No: Cancel shutdown and wait",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # STEP 4: Force termination
            self.add_log_message("⚠️ FORCE TERMINATING THREAD ⚠️")
            self.worker_thread.terminate()

            # Wait for termination to complete
            if self.worker_thread.wait(1000):  # 1 second
                self.add_log_message("✓ Thread force terminated - closing application")
            else:
                self.add_log_message("⚠️ Thread termination may not have completed cleanly")

            event.accept()
        else:
            # User chose to cancel shutdown
            self.add_log_message("User cancelled shutdown - application will remain open")
            self.add_log_message("Thread is still running - you may need to wait or try closing again")
            self.shutdown_in_progress = False
            event.ignore()  # Don't close the application


class StubbornWorker(QThread):
    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    log_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True
        self.log_message.emit("Cancellation requested (but I'll ignore it!)")

    def run(self):
        self.log_message.emit("Stubborn worker started - I ignore cancellation!")

        for i in range(30):  # Longer task
            # Deliberately NOT checking self.is_cancelled!
            time.sleep(1)
            progress = int(((i + 1) / 30) * 100)
            self.progress_update.emit(progress)
            self.status_update.emit(f"Stubbornly working... {i + 1}/30")

            if i % 5 == 0:
                self.log_message.emit(f"Still ignoring cancellation at step {i + 1}")

        self.log_message.emit("Stubborn worker completed (was never cancelled)")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window
    window = GracefulShutdownApp()

    window.show()

    print("Instructions:")
    print("1. Start a long task")
    print("2. Try to close the window")
    print("3. Watch the graceful shutdown process")

    sys.exit(app.exec())
```


---------------

??? info "Use of AI"
    Page written in part with the help of an AI assistant, mainly using Perplexity AI. The AI was used to generate
    explanations, examples and/or structure suggestions. All information has been verified, edited and completed by
    the author.