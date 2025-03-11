class User:
    """Represents a user with email, password, and username."""

    def __init__(self, email, password, username):
        self.__email = email
        self.__password = password
        self.__username = username

    # Setters
    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_username(self, username):
        self.__username = username

    # Getters
    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_username(self):
        return self.__username

    def __str__(self):
        return f"Username: {self.__username}, Email: {self.__email}, Password: {self.__password}"


class Motor:
    """Represents a motor with ID, name, image, publish year, and motor type."""

    def __init__(self, id, name, img, publish_year, motor_type):
        self.__id = id
        self.__name = name
        self.__img = img
        self.__publish_year = publish_year
        self.__motor_type = motor_type

    # Setters
    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_img(self, img):
        self.__img = img

    def set_publish_year(self, publish_year):
        self.__publish_year = publish_year

    def set_motor_type(self, motor_type):
        self.__motor_type = motor_type

    # Getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_img(self):
        return self.__img

    def get_publish_year(self):
        return self.__publish_year

    def get_motor_type(self):
        return self.__motor_type

    def __str__(self):
        return (
            f"Motor ID: {self.__id}, Name: {self.__name}, "
            f"Image: {self.__img}, Year: {self.__publish_year}, Type: {self.__motor_type}"
        )
