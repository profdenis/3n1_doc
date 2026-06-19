# Managing Background Tasks in PyQt6

## Why Background Tasks Matter

In GUI applications, the main thread (also called the UI thread or event thread) is responsible for:

- Handling user interactions (clicks, keyboard input)
- Updating the user interface
- Processing events from the operating system

When you perform a long-running task directly in the main thread, the entire application becomes unresponsive. Users
can't click buttons, the window might not redraw properly, and the application appears "frozen."

## The Problem: Blocking the Main Thread

Here's what happens when you run a long task on the main thread:

```python
import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class BlockingExample(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("Ready")
        self.start_button = QPushButton("Start Long Task")
        self.counter_button = QPushButton("Click Me! (0)")

        self.start_button.clicked.connect(self.blocking_task)
        self.counter_button.clicked.connect(self.increment_counter)

        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.counter_button)

        self.setLayout(layout)
        self.setWindowTitle("Blocking Example - BAD!")
        self.counter = 0

    def blocking_task(self):
        """This blocks the main thread - DON'T DO THIS!"""
        self.status_label.setText("Working... (App will freeze!)")

        # Simulate a long task - this blocks everything!
        time.sleep(5)

        self.status_label.setText("Task completed!")

    def increment_counter(self):
        self.counter += 1
        self.counter_button.setText(f"Click Me! ({self.counter})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlockingExample()
    window.show()
    sys.exit(app.exec())
```

**Try this example:** Click "Start Long Task" and then try to click the counter button. The entire application freezes!

## The Solution: QThread

PyQt6 provides `QThread` to run tasks in separate threads. Here's the proper way to handle background tasks:

```python
import sys
import time
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class WorkerThread(QThread):
    """Separate thread for long-running tasks"""

    # Define signals to communicate with the main thread
    progress_update = pyqtSignal(str)  # Send status messages
    task_finished = pyqtSignal(str)  # Send completion message

    def run(self):
        """This method runs in the separate thread"""
        # Emit a signal to update the UI
        self.progress_update.emit("Starting task...")

        # Simulate a long task with progress updates
        for i in range(5):
            time.sleep(1)  # Simulate work
            self.progress_update.emit(f"Working... Step {i + 1}/5")

        # Task completed
        self.task_finished.emit("Task completed successfully!")


class NonBlockingExample(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker_thread = None

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("Ready")
        self.start_button = QPushButton("Start Long Task")
        self.counter_button = QPushButton("Click Me! (0)")

        self.start_button.clicked.connect(self.start_background_task)
        self.counter_button.clicked.connect(self.increment_counter)

        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.counter_button)

        self.setLayout(layout)
        self.setWindowTitle("Non-Blocking Example - GOOD!")
        self.counter = 0

    def start_background_task(self):
        """Start the task in a separate thread"""
        # Disable the button to prevent multiple tasks
        self.start_button.setEnabled(False)

        # Create and configure the worker thread
        self.worker_thread = WorkerThread()

        # Connect signals to update the UI
        self.worker_thread.progress_update.connect(self.update_status)
        self.worker_thread.task_finished.connect(self.task_completed)

        # Start the thread
        self.worker_thread.start()

    def update_status(self, message):
        """Called when the worker thread sends a progress update"""
        self.status_label.setText(message)

    def task_completed(self, message):
        """Called when the worker thread finishes"""
        self.status_label.setText(message)
        self.start_button.setEnabled(True)  # Re-enable the button

        # Clean up the thread
        self.worker_thread = None

    def increment_counter(self):
        """This works even while the background task is running!"""
        self.counter += 1
        self.counter_button.setText(f"Click Me! ({self.counter})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NonBlockingExample()
    window.show()
    sys.exit(app.exec())
```

**Try this example:** Click "Start Long Task" and then immediately click the counter button. The counter works while the
background task runs!

## Key Concepts Explained

### 1. Thread Communication with Signals

- Threads cannot directly update GUI elements
- Use `pyqtSignal` to send data from worker thread to main thread
- Main thread receives signals and updates the GUI

### 2. Signal and Slot Connection

```python
# In the worker thread class
progress_update = pyqtSignal(str)  # Define the signal

# In the main thread
self.worker_thread.progress_update.connect(self.update_status)  # Connect to slot
```

### 3. Thread Lifecycle

- Create thread instance
- Connect signals before starting
- Call `start()` to begin execution
- Clean up when finished

## Best Practices

1. **Always use signals for thread communication**
2. **Disable UI elements during background tasks** to prevent conflicts
3. **Provide user feedback** about task progress
4. **Handle thread cleanup** properly
5. **Don't create too many threads** - they consume system resources

## Common Mistakes to Avoid

- **Never** update GUI directly from worker thread
- **Don't forget** to re-enable buttons after task completion
- **Always check** if thread is still running before creating a new one
- **Remember** to connect signals before starting the thread

## Next Steps

This basic pattern can be extended for:

- File processing with progress bars
- Network downloads with progress indicators
- Data processing with cancellation support
- Multiple concurrent tasks

The key principle remains the same: keep the main thread free for UI updates, and use separate threads for heavy work.

---------------

??? info "Use of AI"

    Page written in part with the help of an AI assistant, mainly using Perplexity AI. The AI was used to generate
    explanations, examples and/or structure suggestions. All information has been verified, edited and completed by
    the author.