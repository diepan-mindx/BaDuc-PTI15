import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from views import Login

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        root_ui_path = "app/ui/"

        # Show all windows for testing
        login = Login(root_ui_path)
        login.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
