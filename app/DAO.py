# them thu vien json
import json as j


# tao class DAO
class DAO:

    # + thuoc tinh cua lop: root_path
    root_path = "data/"
    
    # + phuong thuc cua lop: load_json_data(entity_name), save_json_data(entity_name, data)
    @classmethod
    def load_json_data(cls, entity_name):
        data = list()
        # mo file json
        file_path = cls.root_path + entity_name + ".json" 
        with open(file_path, "r") as json_file:
            # doc du lieu json
            data = j.load(json_file) #chuyen json thanh python object
        return data

    @classmethod
    def save_json_data(cls, entity_name, updated_list):
        #  ghi de du lieu json
        file_path = cls.root_path + entity_name + ".json"
        with open(file_path, "w") as json_file:
            j.dump(updated_list, json_file) #chuyen python object thanh json
        print("Successful writing!")


