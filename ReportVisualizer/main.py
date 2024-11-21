import sys
import os
import threading
import http.server
import socketserver
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QPushButton, QLabel, QSpacerItem, QSizePolicy
)
from PySide6.QtWebEngineWidgets import QWebEngineView


class BrowserApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML File Viewer with PySide6")
        self.setGeometry(100, 100, 1024, 768)

        # Resource folder path
        self.resource_folder = os.path.join(os.path.dirname(__file__), "resource")

        # Start HTTP server in a separate thread
        self.http_server_port = 8000
        self.start_http_server()

        # Main Layout
        main_layout = QVBoxLayout(self)

        # Top layout for file selector and reload button
        top_layout = QHBoxLayout()

        # ComboBox for file selection
        self.file_selector = QComboBox(self)
        self.file_selector.addItem("Select an HTML file...")
        self.populate_file_selector()
        self.file_selector.currentIndexChanged.connect(self.load_selected_file)
        self.file_selector.setMinimumWidth(400)

        # Reload button
        self.reload_button = QPushButton("Reload", self)
        self.reload_button.clicked.connect(self.reload_current_file)

        # Add widgets to the top layout
        top_layout.addWidget(QLabel("Select an HTML file to display:", self))
        top_layout.addWidget(self.file_selector)
        top_layout.addWidget(self.reload_button)
        top_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # WebEngineView (Chromium-based browser)
        self.browser = QWebEngineView(self)

        # Add layouts to the main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.browser)

    def start_http_server(self):
        """Starts a simple HTTP server to serve files from the resource folder."""
        handler = http.server.SimpleHTTPRequestHandler
        os.chdir(self.resource_folder)

        def serve():
            with socketserver.TCPServer(("", self.http_server_port), handler) as httpd:
                print(f"Serving at http://localhost:{self.http_server_port}")
                httpd.serve_forever()

        thread = threading.Thread(target=serve, daemon=True)
        thread.start()

    def populate_file_selector(self):
        """Populates the combo box with HTML files from the resource folder."""
        if not os.path.exists(self.resource_folder):
            os.makedirs(self.resource_folder)

        html_files = [
            file for file in os.listdir(self.resource_folder)
            if file.endswith(".html")
        ]
        for file in html_files:
            self.file_selector.addItem(file)

    def load_selected_file(self):
        """Loads the selected file in the browser."""
        selected_file = self.file_selector.currentText()
        if selected_file != "Select an HTML file...":
            url = f"http://localhost:{self.http_server_port}/{selected_file}"
            print(f"Loading URL: {url}")
            self.browser.setUrl(url)

    def reload_current_file(self):
        """Reloads the currently displayed file."""
        self.browser.reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserApp()
    window.show()
    sys.exit(app.exec())
