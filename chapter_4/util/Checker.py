import re


class Checker(object):
    FIELD_LIST = {'name', 'age', 'birthday', 'origin_home', 'current_home'}

    def check_add_fields_exists(self, dict_tobe_inserted):
        if not dict_tobe_inserted:
            return False
        return self.FIELD_LIST == set(dict_tobe_inserted.keys())

    def check_update_fields_exists(self, dict_tobe_inserted):
        if 'people_id' not in dict_tobe_inserted:
            return False
        return self.check_add_fields_exists(dict_tobe_inserted.get('updated_info', {}))

    def check_value_valid(self, dict_tobe_inserted):
        name = dict_tobe_inserted['name']
        if not name:
            return '姓名不能为空'
        age = dict_tobe_inserted['age']
        if not isinstance(age, int) or age < 0 or age > 120:
            return '年龄必需是范围在0到120之间的整数'
        birthday = dict_tobe_inserted['birthday']
        if not re.match('\d{4}-\d{2}-\d{2}', birthday):
            return '生日格式必需为：yyyy-mm-dd'

    def transfer_people_id(self, people_id):
        if isinstance(people_id, int):
            return people_id
        try:
            people_id = int(people_id)
            return people_id
        except ValueError:
            return -1