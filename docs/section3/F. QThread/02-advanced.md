# Advanced Example

??? note "Full Code"

    ```python
    import sys
    import time
    from PyQt6.QtCore import QThread, pyqtSignal, QTimer
    from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                                 QLabel, QProgressBar, QTextEdit)
    
    class AdvancedWorkerThread(QThread):
        """Enhanced worker thread with progress reporting and cancellation support"""
        
        # Signals for communication with main thread
        progress_update = pyqtSignal(int)        # Progress percentage (0-100)
        status_update = pyqtSignal(str)          # Status message
        task_finished = pyqtSignal(str)          # Completion message
        log_message = pyqtSignal(str)            # Log entry
        
        def __init__(self, task_duration=10):
            super().__init__()
            self.task_duration = task_duration
            self.is_cancelled = False
        
        def cancel(self):
            """Request cancellation of the task"""
            self.is_cancelled = True
        
        def run(self):
            """Main work method - runs in separate thread"""
            self.log_message.emit("Task started...")
            self.status_update.emit("Initializing...")
            
            total_steps = self.task_duration
            
            for step in range(total_steps):
                # Check if cancellation was requested
                if self.is_cancelled:
                    self.status_update.emit("Task cancelled")
                    self.task_finished.emit("Task was cancelled by user")
                    self.log_message.emit("Task cancelled at step " + str(step + 1))
                    return
                
                # Simulate work
                time.sleep(1)
                
                # Calculate and report progress
                progress = int(((step + 1) / total_steps) * 100)
                self.progress_update.emit(progress)
                self.status_update.emit(f"Processing step {step + 1} of {total_steps}")
                self.log_message.emit(f"Completed step {step + 1}")
            
            # Task completed successfully
            self.status_update.emit("Task completed!")
            self.task_finished.emit("All work completed successfully!")
            self.log_message.emit("Task finished successfully")
    
    class AdvancedBackgroundExample(QWidget):
        def __init__(self):
            super().__init__()
            self.worker_thread = None
            self.init_ui()
            self.setup_timer()
        
        def init_ui(self):
            layout = QVBoxLayout()
            
            # Status display
            self.status_label = QLabel("Ready to start task")
            layout.addWidget(self.status_label)
            
            # Progress bar
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            layout.addWidget(self.progress_bar)
            
            # Control buttons
            self.start_button = QPushButton("Start Background Task")
            self.cancel_button = QPushButton("Cancel Task")
            self.cancel_button.setEnabled(False)
            
            self.start_button.clicked.connect(self.start_task)
            self.cancel_button.clicked.connect(self.cancel_task)
            
            layout.addWidget(self.start_button)
            layout.addWidget(self.cancel_button)
            
            # Interactive counter to show UI remains responsive
            self.counter_button = QPushButton("UI Test Counter (0)")
            self.counter_button.clicked.connect(self.increment_counter)
            layout.addWidget(self.counter_button)
            
            # Log display
            log_label = QLabel("Task Log:")
            layout.addWidget(log_label)
            
            self.log_display = QTextEdit()
            self.log_display.setMaximumHeight(150)
            self.log_display.setReadOnly(True)
            layout.addWidget(self.log_display)
            
            self.setLayout(layout)
            self.setWindowTitle("Advanced Background Task Example")
            self.resize(400, 350)
            
            # Initialize counter
            self.counter = 0
        
        def setup_timer(self):
            """Setup a timer to show elapsed time during task execution"""
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_elapsed_time)
            self.start_time = None
        
        def start_task(self):
            """Start the background task"""
            # Reset UI state
            self.progress_bar.setValue(0)
            self.log_display.clear()
            
            # Update button states
            self.start_button.setEnabled(False)
            self.cancel_button.setEnabled(True)
            
            # Create and configure worker thread
            self.worker_thread = AdvancedWorkerThread(task_duration=8)
            
            # Connect all signals
            self.worker_thread.progress_update.connect(self.update_progress)
            self.worker_thread.status_update.connect(self.update_status)
            self.worker_thread.task_finished.connect(self.task_completed)
            self.worker_thread.log_message.connect(self.add_log_message)
            
            # Start the thread and timer
            self.start_time = time.time()
            self.timer.start(1000)  # Update every second
            self.worker_thread.start()
            
            self.add_log_message("Background task started")
        
        def cancel_task(self):
            """Cancel the running task"""
            if self.worker_thread and self.worker_thread.isRunning():
                self.worker_thread.cancel()
                self.add_log_message("Cancellation requested...")
        
        def update_progress(self, value):
            """Update the progress bar"""
            self.progress_bar.setValue(value)
        
        def update_status(self, message):
            """Update the status label"""
            elapsed = ""
            if self.start_time:
                elapsed_seconds = int(time.time() - self.start_time)
                elapsed = f" (Elapsed: {elapsed_seconds}s)"
            
            self.status_label.setText(message + elapsed)
        
        def task_completed(self, message):
            """Handle task completion"""
            self.status_label.setText(message)
            
            # Reset button states
            self.start_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            
            # Stop timer
            self.timer.stop()
            
            # Clean up thread
            self.worker_thread = None
            
            self.add_log_message("Task completed or cancelled")
        
        def add_log_message(self, message):
            """Add a message to the log display"""
            timestamp = time.strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}"
            self.log_display.append(log_entry)
        
        def update_elapsed_time(self):
            """Update the elapsed time display"""
            if self.start_time:
                elapsed_seconds = int(time.time() - self.start_time)
                current_text = self.status_label.text()
                # Remove old elapsed time if present
                if "(Elapsed:" in current_text:
                    current_text = current_text.split(" (Elapsed:")[0]
                self.status_label.setText(f"{current_text} (Elapsed: {elapsed_seconds}s)")
        
        def increment_counter(self):
            """Demonstrate that UI remains responsive during background task"""
            self.counter += 1
            self.counter_button.setText(f"UI Test Counter ({self.counter})")
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = AdvancedBackgroundExample()
        window.show()
        sys.exit(app.exec())
    ```

## New Concepts in the Advanced Example

### 1. **Task Cancellation**

In the basic example, once you started a task, you had to wait for it to finish. The advanced example introduces 
**cancellation**:

```python
def cancel(self):
    """Request cancellation of the task"""
    self.is_cancelled = True


def run(self):
    for step in range(total_steps):
        # Check if cancellation was requested
        if self.is_cancelled:
            self.status_update.emit("Task cancelled")
            self.task_finished.emit("Task was cancelled by user")
            return  # Exit the task early
```

**Key points:**

- We use a simple boolean flag (`self.is_cancelled`) to signal cancellation
- The worker thread checks this flag regularly during its work
- When cancelled, the thread exits early and notifies the main thread
- The main thread can request cancellation by calling `worker_thread.cancel()`

### 2. **Progress Reporting**

The basic example only showed "working" or "done". The advanced example shows **real progress**:

```python
# In worker thread
progress_update = pyqtSignal(int)  # New signal for progress percentage

# Calculate progress as percentage
progress = int(((step + 1) / total_steps) * 100)
self.progress_update.emit(progress)
```

**In the main window:**

```python
self.progress_bar = QProgressBar()
self.progress_bar.setRange(0, 100)  # 0% to 100%

# Connect progress signal to progress bar
self.worker_thread.progress_update.connect(self.update_progress)
```

**Why this matters:** Users can see how much work is left and make informed decisions about waiting or cancelling.

### 3. **Multiple Signal Types**

Instead of just one signal, we now have **four different signals** for different purposes:

```python
progress_update = pyqtSignal(int)  # Numbers (0-100)
status_update = pyqtSignal(str)  # Current status
task_finished = pyqtSignal(str)  # Final result
log_message = pyqtSignal(str)  # Detailed logging
```

**This demonstrates:** You can have as many signals as needed, each carrying different types of information.

### 4. **UI State Management**

The advanced example shows proper **button state management**:

```python
def start_task(self):
    self.start_button.setEnabled(False)  # Disable start
    self.cancel_button.setEnabled(True)  # Enable cancel


def task_completed(self, message):
    self.start_button.setEnabled(True)  # Re-enable start
    self.cancel_button.setEnabled(False)  # Disable cancel
```

**Why this matters:** Prevents users from starting multiple tasks simultaneously or trying to cancel when nothing is
running.

### 5. **Real-time Logging**

The advanced example introduces a **log display** that shows what's happening:

```python
def add_log_message(self, message):
    timestamp = time.strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    self.log_display.append(log_entry)
```

**This teaches:** How to provide detailed feedback to users and how to timestamp events.

### 6. **Elapsed Time Tracking**

New concept: **QTimer** for regular updates:

```python
def setup_timer(self):
    self.timer = QTimer()
    self.timer.timeout.connect(self.update_elapsed_time)


# Start timer when task begins
self.timer.start(1000)  # Update every 1000ms (1 second)
```

**Key insight:** You can run multiple things concurrently - the background task AND a timer for UI updates.

### 7. **Enhanced User Experience**

The advanced example shows several UX improvements:

- **Visual feedback:** Progress bar shows completion percentage
- **Detailed status:** Users know exactly what step is happening
- **Time awareness:** Elapsed time helps users decide whether to wait
- **Cancellation option:** Users aren't trapped waiting for long tasks
- **Comprehensive logging:** Users can see the full history of what happened

## The Big Picture

The progression from basic to advanced shows how real applications are built:

1. **Basic threading:** Solve the fundamental problem (don't block UI)
2. **Enhanced threading:** Add features users actually need (progress, cancellation, feedback)
3. **Professional threading:** Handle edge cases and provide excellent user experience

## Points to Take Away

1. **Threads can be as simple or complex as needed** - start basic, add features incrementally
2. **User experience matters** - progress bars and cancellation aren't just nice-to-have
3. **Signals are flexible** - you can create as many as needed for different data types
4. **State management is crucial** - always think about what buttons should be enabled/disabled
5. **Timing is important** - QTimer lets you do regular updates without blocking

The advanced example isn't just "more code": it's "more thoughtful code" that considers what users actually need when
using an application with background tasks.