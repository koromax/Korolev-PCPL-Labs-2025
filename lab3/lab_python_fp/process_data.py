import json

from field import field
from gen_random import gen_random
from unique import Unique
from cm_timer import cm_timer_1
from print_result import print_result

path = "lab3/lab_python_fp/data_light.json"

# Необходимо в переменную path сохранить путь к файлу, который был передан при запуске сценария

with open(path) as f:
    data = json.load(f)

# Далее необходимо реализовать все функции по заданию, заменив `raise NotImplemented`
# Предполагается, что функции f1, f2, f3 будут реализованы в одну строку
# В реализации функции f4 может быть до 3 строк

@print_result
def f1(data):
    return list(Unique(field(data, "job-name"), ignore_case=True))


@print_result
def f2(data):
    return list(filter(lambda x: x.lower().startswith("программист"), data))


@print_result
def f3(data):
    return list(map(lambda x: f"{x} с опытом Python", data))


@print_result
def f4(data):
    return list(map(lambda x: f"{x[0]}, зарплата {x[1]} руб", zip(data, gen_random(len(data), 100000, 200000))))

if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))