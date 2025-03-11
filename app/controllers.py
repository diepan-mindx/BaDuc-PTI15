from models import User, Motor
from DAO import DAO


class UserController:
    """Controller to manage users"""

    def __init__(self):
        self.__user_list = []
        self.__generate_user_list()

    # Private methods
    def __generate_user_list(self):
        self.__user_list = DAO.load_json_data("user")
        self.__convert_dict_to_objects()

    def __convert_dict_to_objects(self):
        self.__user_list = [
            User(user["email"], user["password"], user["username"])
            for user in self.__user_list
        ]

    def __convert_users_to_dict(self):
        return [
            {
                "email": user.get_email(),
                "password": user.get_password(),
                "username": user.get_username(),
            }
            for user in self.__user_list
        ]

    def __save_user_data(self):
        DAO.save_json_data("user", self.__convert_users_to_dict())

    # Public methods
    def retrieve_user_list(self):
        return self.__user_list

    def find_user_by_username(self, username):
        for user in self.__user_list:
            if user.get_username() == username:
                return user
        return None

    def find_user_by_email(self, email):
        for user in self.__user_list:
            if user.get_email() == email:
                return user
        return None

    def add_user(self, user):
        self.__user_list.append(user)
        self.__save_user_data()

    def remove_user_by_email(self, deleted_email):
        self.__user_list = [
            user for user in self.__user_list if user.get_email() != deleted_email
        ]
        self.__save_user_data()

    def sort_users_by_username(self):
        self.__user_list.sort(key=lambda user: user.get_username())

    def sort_users_by_email(self):
        self.__user_list.sort(key=lambda user: user.get_email())


class MotorController:
    """Controller to manage motors"""

    def __init__(self):
        self.__motor_list = []
        self.__generate_motor_list()

    # Private methods
    def __generate_motor_list(self):
        self.__motor_list = DAO.load_json_data("motor")
        self.__convert_dict_to_objects()

    def __convert_dict_to_objects(self):
        self.__motor_list = [
            Motor(
                motor["id"],
                motor["name"],
                motor["img"],
                motor["publish_year"],
                motor["motor_type"],
            )
            for motor in self.__motor_list
        ]

    def __convert_motors_to_dict(self):
        return [
            {
                "id": motor.get_id(),
                "name": motor.get_name(),
                "img": motor.get_img(),
                "publish_year": motor.get_publish_year(),
                "motor_type": motor.get_motor_type(),
            }
            for motor in self.__motor_list
        ]

    def __save_motor_data(self):
        DAO.save_json_data("motor", self.__convert_motors_to_dict())

    # Public methods
    def get_motor_types(self):
        return ["Tay ga", "Tay côn", "Xe số", "Xe điện"]

    def retrieve_motor_list(self):
        return self.__motor_list

    def find_motor_by_name(self, name):
        return [
            motor
            for motor in self.__motor_list
            if name.lower() in motor.get_name().lower()
        ]

    def find_motor_by_id(self, motor_id):
        for motor in self.__motor_list:
            if motor.get_id() == motor_id:
                return motor
        return None

    def add_motor(self, motor):
        self.__motor_list.append(motor)
        self.__save_motor_data()

    def remove_motor_by_id(self, motor_id):
        self.__motor_list = [
            motor for motor in self.__motor_list if motor.get_id() != motor_id
        ]
        self.__save_motor_data()

    def sort_motors_by_id(self):
        self.__motor_list.sort(key=lambda motor: motor.get_id())

    def sort_motors_by_name(self):
        self.__motor_list.sort(key=lambda motor: motor.get_name().lower())

    def sort_motors_by_publish_year(self):
        self.__motor_list.sort(key=lambda motor: motor.get_publish_year())

    def sort_motors_by_motor_type(self):
        self.__motor_list.sort(key=lambda motor: motor.get_motor_type().lower())

    def update_motor(self, new_motor):
        motor = self.find_motor_by_id(motor_id=new_motor.get_id())
        if motor:
            self.__motor_list = [
                new_motor if motor.get_id() == new_motor.get_id() else motor
                for motor in self.__motor_list
            ]
            self.__save_motor_data()
            return "Motor updated successfully."
        return "Motor not found."
