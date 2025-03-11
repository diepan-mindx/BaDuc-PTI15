import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from views import Login, Signup, Home, Search, Account

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        root_ui_path = "app/ui/"

        # Show all windows for testing
        # login = Login(root_ui_path)
        # login.show()

        home_window = Home(
            root_ui_path, "user1"
        )  # Replace with actual parameters if needed
        home_window.show()

        #   search_window = Search(root_ui_path)  # Replace with actual parameters if needed
        #   search_window.show()

        #   account_window = Account(root_ui_path)  # Replace with actual parameters if needed
        #   account_window.show()

        sys.exit(app.exec())
    except Exception as e:
        print(e)
