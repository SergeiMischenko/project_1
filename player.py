from random import randint
from time import sleep
from my_coloram import MAGENTA, BLUE, YELLOW, RED
from string import digits


class Player:
    CLASSES = {"Воин": {"Двуручный меч": 20, "Топорик": 15, "Кувалда": 18, "Меч и щит": 10},
               "Рейнджер": {"Кинжал": 8, "Меч": 12, "Лук": 16, "Арбалет": 18},
               "Маг": {"Посох": 12, "Жезл": 15, "Магический шар": 10}}

    def __init__(self, name, class_, weapon):
        self.name = name
        self.class_ = class_
        self.hp = 100
        self.weapon = weapon
        self.damage = self.CLASSES[self.class_][self.weapon]
        match class_:
            case "Воин":
                match weapon:
                    case "Меч и Щит":
                        self.armor = 20 + randint(5, 15)
                    case _:
                        self.armor = 20
            case "Рейнджер":
                self.armor = 8
            case "Маг":
                self.armor = 5
        self.xp = 0
        self.level = 1
        self.gold = 0

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        if key == 'name' and hasattr(self, 'name') or key == 'class_' and hasattr(self, 'class_'):
            print(f'{MAGENTA}Вы не можете изменять имя и класс вашего героя')
        else:
            object.__setattr__(self, key, value)

    @classmethod
    def create_player(cls):
        name = cls._valid_name(input(f"{YELLOW}Введи имя своего героя: ").strip())
        cls._print_list()
        class_ = cls._valid_class(input(f"{BLUE}{name}{YELLOW} выбери класс из списка выше: ").capitalize())
        cls._print_list(class_=class_)
        weapon = cls._valid_weapon(input(f"{BLUE}{name}{YELLOW} выбери оружие из списка выше: ").capitalize(), class_)
        return Player(name, class_, weapon)

    def attack(self, enemy):
        damage_resist = self.damage * enemy.armor / 100
        damage = round(self.damage - damage_resist)
        enemy.hp -= damage
        print('-' * 20)
        print(f"{BLUE}{self.name}{YELLOW} наносит удар с помощью {BLUE}'{self.weapon}'"
              f"{YELLOW} по {RED}'{enemy.race}у'{YELLOW}, урон: {RED}{damage}")
        if enemy.hp <= 0:
            self.xp, self.gold = self.xp + enemy.xp, self.gold + enemy.gold
            enemy.hp, enemy.xp, enemy.gold = 0, 0, 0
            print(f"{RED}'{enemy.race}' {YELLOW}повержен от вашей руки")
        else:
            print(f"{YELLOW}У {RED}'{enemy.race}а'{YELLOW} осталось {RED}{enemy.hp} {YELLOW}ОЗ")
        print('-' * 20)
        sleep(2)

    @staticmethod
    def _valid_name(name):
        while True:
            if not name:
                print(f"\n{MAGENTA}Имя не может быть пустым")
            elif name.startswith(tuple(digits)):
                print(f"\n{MAGENTA}Имя не может начинаться с цифр")
            else:
                break
            name = input(f"{YELLOW}Попробуй другое имя: ").strip()
        return name

    @classmethod
    def _valid_class(cls, amount):
        classes_len = list(map(str, range(1, len(cls.CLASSES) + 1)))
        while True:
            if not amount.strip():
                print(f"\n{MAGENTA}Ты же ничего не ввёл")
            elif amount not in cls.CLASSES and amount not in classes_len:
                print(f"\n{MAGENTA}Такого класса не существует, возможно ты ошибся")
            else:
                break
            amount = input(f"{YELLOW}Попробуй ещё разок: ").capitalize()
        if amount.isdigit():
            amount = list(cls.CLASSES.keys())[int(amount) - 1]
        return amount

    @classmethod
    def _valid_weapon(cls, amount, class_):
        class_weapon_len = list(map(str, range(1, len(cls.CLASSES[class_]) + 1)))
        while True:
            if not amount.strip():
                print(f"\n{MAGENTA}Ты же ничего не ввёл")
            elif amount not in cls.CLASSES[class_] and amount not in class_weapon_len:
                print(f"\n{MAGENTA}Такого оружия не существует, возможно ты ошибся")
            else:
                break
            amount = input(f"{YELLOW}Попробуй ещё разок: ").capitalize()
        if amount.isdigit():
            amount = list(cls.CLASSES[class_].keys())[int(amount) - 1]
        return amount

    @classmethod
    def _print_list(cls, class_=None):
        match class_:
            case None:
                classes = cls.CLASSES
            case _:
                classes = cls.CLASSES[class_]
        print('-' * 20)
        for ind, amount in enumerate(classes, 1):
            print(f"{RED}\t{ind}. {amount}")
        print('-' * 20)
        sleep(1)
