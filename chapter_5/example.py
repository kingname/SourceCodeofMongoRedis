import redis

client = redis.Redis(host='xx.xx.xx.xx')
all_class = ['algorithm',
             'computer',
             'history',
             'circuit_design',
             'math']


def all_student():
    students = client.sunion(*all_class)
    return len(students)


def in_a_and_in_b(class_a, class_b):
    students = client.sinter(class_a, class_b)
    return len(students)


def in_a_not_in_b(class_a, class_b):
    students = client.sdiff(class_a, class_b)
    return len(students)


def in_a_or_in_b(class_a, class_b):
    students = client.sunion(class_a, class_b)
    return len(students)


if __name__ == '__main__':
    print(f'当前一共有{all_student()}名学生至少选了一门课。')
    print(f'当前选了math，没有选computer的学生有：{in_a_not_in_b("math", "computer")}名学生至少选了一门课。')
    print(f'当前选了math，也选computer的学生有：{in_a_and_in_b("math", "computer")}名学生至少选了一门课。')
    print(f'当前选了math，或者选computer的学生有：{in_a_or_in_b("math", "computer")}名学生至少选了一门课。')


