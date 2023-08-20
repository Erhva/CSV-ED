import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Editor")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.file_label = QLabel("Drag and Drop CSV File Here")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setAcceptDrops(True)
        self.file_label.setFixedSize(300, 100)  # Set the fixed size here
        
        self.select_button = QPushButton("Select File")
        self.select_button.clicked.connect(self.open_file_dialog)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.file_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.submit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_submit(self):
        username = self.username_input.text()
        password = self.password_input.text()
        file_path = self.file_label.text()
        print("Username:", username)
        print("Password:", password)
        print("File Path:", file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            for url in mime_data.urls():
                file_path = url.toLocalFile()
                self.file_label.setText("File Selected: " + file_path)
                event.acceptProposedAction()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.file_label.setText("File Selected: " + file_path)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
