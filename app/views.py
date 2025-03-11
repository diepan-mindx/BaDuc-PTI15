from PyQt6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
import re, sys, os

from controllers import MotorController, UserController
from models import User, Motor


# -----------------------------------------------------------------------------
class MessageHelper:
    # tạo lớp để hiển thị thông báo lỗi khi chạy ứng dụng
    @staticmethod
    def show_message(message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        ok_button = msg_box.addButton(QMessageBox.StandardButton.Ok)
        ok_button.setStyleSheet("background-color: #598896;")
        msg_box.exec()


# -----------------------------------------------------------------------------
class Login(QMainWindow):
    def __init__(self, root_ui_path):
        super().__init__()
        self.ui = uic.loadUi(root_ui_path + "login.ui", self)
        self.setWindowTitle("Login")
        self.userController = UserController()
        self.motorController = MotorController()
        self.root_ui_path = root_ui_path
        try:
            self.login_btn.mousePressEvent = self.check_login
            self.signup_btn.mousePressEvent = self.open_signup
        except Exception as e:
            print(f"Error: {e}")

    def check_login(self, event):
        email = self.email.text()
        password = self.password.text()

        # Validation for email and password
        if email == "" or password == "":
            MessageHelper.show_message("Vui lòng điền đầy đủ thông tin đăng nhập!")
            return
        try:
            # Check if the account exists in the system
            currentUser = self.userController.find_user_by_email(email)

            if not currentUser:
                MessageHelper.show_message("Tài khoản chưa tồn tại, vui lòng đăng ký!")
                return
            else:
                # Check password
                if currentUser.get_password() == password:
                    # Login successful
                    try:
                        home = Home(self.root_ui_path, currentUser.get_username())
                        home.show()
                        self.close()
                    except Exception as e:
                        print("Failed to open home window: " + str(e))
                else:
                    # Incorrect password
                    MessageHelper.show_message("Thông tin đăng nhập không chính xác!")
                    return
        except Exception as e:
            print("Error login", e)

    def open_signup(self, event):
        try:
            signup_window = Signup(self.root_ui_path)  # Updated to use Signup
            signup_window.show()
            self.close()
        except Exception as e:
            print(e)


# -----------------------------------------------------------------------------
class Account(QMainWindow):
    def __init__(self, root_ui_path):
        super().__init__()
        self.ui = uic.loadUi(root_ui_path + "account.ui", self)
        self.setWindowTitle("Account")
        self.userController = UserController()
        self.motorController = MotorController()
        self.root_ui_path = root_ui_path
        self.home_btn.clicked.connect(self.open_home)
        self.logout_btn.clicked.connect(self.logout)

    def open_home(self):
        try:
            home_window = Home(self.root_ui_path, '')
            home_window.show()
            self.close()
        except Exception as e:
            print(f"Error opening home window: {e}")

    def logout(self):
        """Log out and open the login window."""
        try:
            self.close()  # Close the account window

            # Open login screen
            login_window = Login(self.root_ui_path)
            login_window.show()
        except Exception as e:
            MessageHelper.show_message(f"Error logging out: {e}")


# -----------------------------------------------------------------------------
class Home(QMainWindow):
    def __init__(self, root_ui_path, current_username=""):
        super().__init__()
        try:
            self.ui = uic.loadUi(root_ui_path + "home.ui", self)
            self.setWindowTitle("Home")
            self.current_username = current_username
            self.userController = UserController()
            self.motorController = MotorController()
            self.root_ui_path = root_ui_path

            # Load data for UI
            self.load_motor_list()

            # Event for search button
            self.search_btn.clicked.connect(self.search)
            self.edit_btn.clicked.connect(self.openEditWindow)
            self.delete_btn.clicked.connect(self.confirm_delete)
            self.rating_btn.clicked.connect(self.openRatingWindow)
            self.account_btn.clicked.connect(self.openAccountWindow)
            self.create_btn.clicked.connect(self.gotoSearch)

            # Connect the itemClicked signal to the on_item_clicked method
            self.danhsachxe.itemClicked.connect(self.on_item_clicked)
        except Exception as e:
            print(f"Error initializing Home window: {e}")

    def openAccountWindow(self):
        try:
            account_window = Account(self.root_ui_path)
            account_window.show()
        except Exception as e:
            print(f"Error opening account window: {e}")
        self.close()

    def load_current_motor(self, motor_id):
        try:
            motor = self.motorController.find_motor_by_id(motor_id)
            self.current_motor = motor
            if motor:
                # Change data in widget
                self.ten.setText(motor.get_name())
                self.nam.setText(str(motor.get_publish_year()))
                self.loai.setText(motor.get_motor_type())

                pixmap = QPixmap(motor.get_img())
                if not pixmap.isNull():
                    self.hinh.setPixmap(pixmap)
                else:
                    self.hinh.clear()  # Clear the image if loading fails
            else:
                MessageHelper.show_message("Không tìm thấy xe!", success=False)
        except Exception as e:
            print(f"Error loading motor details: {e}")

    def load_motor_list(self):
        try:
            motor_list = self.motorController.retrieve_motor_list()
            self.danhsachxe.clear()  # Clear the list before adding new items
            if motor_list:
                self.load_current_motor(motor_list[0].get_id())  # Load first motor
                self.danhsachxe.clear()  # Clear the list before adding new items
                for motor in motor_list:
                    item = QListWidgetItem(f"{motor.get_id()}: {motor.get_name()}")
                    self.danhsachxe.addItem(item)
            else:
                MessageHelper.show_message("Danh sách xe trống!", success=False)
        except Exception as e:
            print(f"Error loading motor list: {e}")

    def on_item_clicked(self, item):
        try:
            motor_id = int(item.text().split(":")[0])
            self.load_current_motor(motor_id)
        except Exception as e:
            print(f"Error handling item click: {e}")

    def openEditWindow(self):
        """Close Home and open Edit window."""
        try:
            # Open Edit window
            edit_window = Edit(
                root_ui_path=self.root_ui_path, current_motor=self.current_motor
            )
            edit_window.show()
            self.close()  # Close Home window
        except Exception as e:
            print(f"Error opening edit window: {e}")

    def confirm_delete(self):
        """Show confirmation dialog before deleting."""
        try:
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                "Are you sure you want to proceed?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.delete_item()
        except Exception as e:
            print(f"Error showing confirmation dialog: {e}")

    def delete_item(self):
        """Delete the item, close Home, and open a new Home window."""
        try:
            self.motorController.remove_motor_by_id(self.current_motor.get_id())
            print("Item deleted.")
            # restart list of home
            self.load_motor_list()
        except Exception as e:
            print("Error deleting item:", e)

    def openRatingWindow(self):
        try:
            # Open Rating window
            rating_window = Rating(
                root_ui_path=self.root_ui_path, current_motor=self.current_motor
            )
            rating_window.show()
        except Exception as e:
            print(f"Error opening rating window: {e}")

    def gotoSearch(self):
        try:
            account_window = Search(self.root_ui_path, "")
            account_window.show()
        except Exception as e:
            print(f"Error opening account window: {e}")

    def search(self):
        try:
            query = self.search_input.text().strip()
            if not query:
                MessageHelper.show_message("Vui lòng nhập từ khóa tìm kiếm!")
                return
            # mở cửa sổ tìm kiếm
            search = Search(self.root_ui_path, query)
            search.show()
        except Exception as e:
            print(f"Error in search function: {e}")


# -----------------------------------------------------------------------------
class Search(QMainWindow):
    def __init__(self, root_ui_path, query):
        super().__init__()
        self.ui = uic.loadUi(root_ui_path + "search.ui", self)
        self.setWindowTitle("Search")
        self.userController = UserController()
        self.motorController = MotorController()
        self.root_ui_path = root_ui_path
        self.search_input = query


# -----------------------------------------------------------------------------
class Rating(QMainWindow):
    def __init__(self, root_ui_path, current_motor):
        super().__init__()
        self.ui = uic.loadUi(root_ui_path + "rating.ui", self)
        self.setWindowTitle("Search")
        self.current_motor = current_motor
        self.userController = UserController()
        self.motorController = MotorController()
        self.root_ui_path = root_ui_path

        # Connect buttons to functions
        self.cancel_btn.clicked.connect(self.back_to_home)
        self.save_btn.clicked.connect(self.save_and_back)

    def back_to_home(self):
        """Close Rating window and return to Home."""
        try:
            self.close()  # Close Rating window

            # Open Home window
            home_window = Home(self.root_ui_path)
            home_window.show()
        except Exception as e:
            print(f"Error returning to home: {e}")

    def save_and_back(self):
        """Save rating (no action needed) and return to Home."""
        self.back_to_home()


# -----------------------------------------------------------------------------
class Edit(QMainWindow):
    def __init__(self, root_ui_path, current_motor):
        super().__init__()
        self.ui = uic.loadUi(root_ui_path + "edit.ui", self)
        self.setWindowTitle("Edit Motor")
        self.current_motor = current_motor
        self.userController = UserController()
        self.motorController = MotorController()
        self.root_ui_path = root_ui_path

        # Connect buttons to functions
        self.cancel_btn.clicked.connect(self.back_to_home)
        self.save_btn.clicked.connect(self.save_and_back)
        self.layanh_btn.clicked.connect(
            self.open_file_dialog
        )  # Open file dialog for image selection

        # Load data into UI
        self.load_motor_data()
        self.load_motor_types()

    def load_motor_data(self):
        """Populate UI fields with existing motor data."""
        try:
            if self.current_motor:
                self.ten.setText(self.current_motor.get_name())
                self.hinh.setText(
                    self.current_motor.get_img()
                )  # Assuming text field for image path
                self.namsanxuat.setText(str(self.current_motor.get_publish_year()))
                self.hang.setText("Honda")
                # Set current type in the combo box
                motor_type = self.current_motor.get_motor_type()
                index = self.loai.findText(motor_type)  # Find index of the motor type
                if index != -1:
                    self.loai.setCurrentIndex(index)  # Set current motor type
        except Exception as e:
            print(f"Error loading motor data: {e}")

    def load_motor_types(self):
        """Load available motor types into combo box."""
        try:
            motor_types = (
                self.motorController.get_motor_types()
            )  # Get list of available motor types
            self.loai.addItems(motor_types)  # Add types to combo box
        except Exception as e:
            print(f"Error loading motor types: {e}")

    def open_file_dialog(self):
        """Open file dialog to select an image."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            self.hinh.setText(file_path)  # Set selected image path to input field

    def validate_form(self):
        """Validate form before saving."""
        ten = self.ten.text().strip()
        hinh = self.hinh.text().strip()
        namsanxuat = self.namsanxuat.text().strip()
        loai = self.loai.currentText().strip()
        hang = self.hang.text().strip()

        if not ten or not hinh or not namsanxuat or not loai or not hang:
            MessageHelper.show_message("All fields must be filled.")
            return False

        if not namsanxuat.isdigit() or int(namsanxuat) < 1900 or int(namsanxuat) > 2100:
            MessageHelper.show_message(
                "Publish year must be a valid number between 1900 and 2100."
            )
            return False

        return True

    def save_and_back(self):
        """Validate, save data, and return to Home."""
        if not self.validate_form():
            return

        try:
            # Update motor data
            updated_data = Motor(
                id=self.current_motor.get_id(),
                name=self.ten.text().strip(),
                img=self.hinh.text().strip(),
                publish_year=int(self.namsanxuat.text().strip()),
                motor_type=self.loai.currentText().strip(),
            )

            self.motorController.update_motor(updated_data)
            print(f"Motor {self.current_motor.get_id()} updated successfully.")

            self.back_to_home()
        except Exception as e:
            print(f"Error saving motor data: {e}")

    def back_to_home(self):
        """Close Edit window and return to Home."""
        try:
            self.close()

            # Open Home window
            home_window = Home(self.root_ui_path)
            home_window.show()
        except Exception as e:
            print(f"Error returning to home: {e}")


# -----------------------------------------------------------------------------
class Signup(QMainWindow):
    def __init__(self, root_ui_path):
        super().__init__()
        self.ui = uic.loadUi(root_ui_path + "signup.ui", self)
        self.setWindowTitle("Signup")
        self.userController = UserController()
        self.motorController = MotorController()
        self.root_ui_path = root_ui_path

        try:
            self.signup_btn.clicked.connect(self.register_user)
            self.login_btn.clicked.connect(self.open_login)
        except Exception as e:
            print(f"Error: {e}")

    def register_user(self):
        username = self.username.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        confirm_password = self.confirmPassword.text().strip()

        # Validate empty fields
        if not (username and email and password and confirm_password):
            MessageHelper.show_message("Vui lòng điền đầy đủ thông tin đăng ký!")
            return

        # Validate email format
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            MessageHelper.show_message("Email không hợp lệ!")
            return

        # Validate password length
        if len(password) < 6:
            MessageHelper.show_message("Mật khẩu phải có ít nhất 6 ký tự!")
            return

        # Validate password confirmation
        if password != confirm_password:
            MessageHelper.show_message("Mật khẩu xác nhận không khớp!")
            return

        # Check if username or email already exists
        if self.userController.find_user_by_username(username):
            MessageHelper.show_message("Tên đăng nhập đã tồn tại!")
            return

        if self.userController.find_user_by_email(email):
            MessageHelper.show_message("Email đã được sử dụng!")
            return

        try:
            # Create new user
            new_user = User(username=username, email=email, password=password)
            self.userController.add_user(new_user)
            # Registration successful, open Login window
            home = Home(self.root_ui_path, new_user.get_username())
            home.show()
            self.close()  # Close signup window

        except Exception as e:
            print("Error signup", e)

    def open_login(self):
        try:
            login_window = Login(self.root_ui_path)
            login_window.show()
            self.close()
        except Exception as e:
            print(e)
