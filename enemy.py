from random import randint, choice
from time import sleep
from my_coloram import MAGENTA, BLUE, YELLOW, RED


class Enemy:
    enemy_races = {"Гоблин": {"Палка": 4, "Кинжал": 7, "Метательные Ножи": 5},
                   "Орк": {"Дубина": 10, "Секира": 15, "Молот": 12},
                   "Чернокнижник": {"Посох": 10, "Жезл": 12, "Магический Шар": 8}}

    def __init__(self, race):
        self.race = race
        match race:
            case 'Гоблин':
                self.hp = randint(5, 8)
                self.weapon = choice(list(self.enemy_races[self.race].keys()))
                self.damage = self.enemy_races[self.race][self.weapon]
                self.armor = 5 + randint(0, 8)
                self.xp = choice([5, 8, 10])
            case 'Орк':
                self.hp = randint(12, 20)
                self.weapon = choice(list(self.enemy_races[self.race].keys()))
                self.damage = self.enemy_races[self.race][self.weapon]
                self.armor = 10 + randint(2, 15)
                self.xp = choice([10, 12, 15, 20])
            case 'Чернокнижник':
                self.hp = randint(8, 12)
                self.weapon = choice(list(self.enemy_races[self.race].keys()))
                self.damage = self.enemy_races[self.race][self.weapon]
                self.armor = 0 + randint(0, 5)
                self.xp = choice([5, 8, 10, 12])
        self.gold = randint(0, 20)

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        if key == 'race' and hasattr(self, 'race'):
            print(f'{MAGENTA}Вы не можете изменять расу врага')
        else:
            object.__setattr__(self, key, value)

    def get_attack(self, player):
        if self.get_status_enemy():
            damage = self.damage - (self.damage * player.armor / 100)
            player.hp = round(player.hp - damage)
            print(
                f"{RED}{self.race}{YELLOW} наносит удар с помощью {BLUE}'{self.weapon}'"
                f"{YELLOW} по герою {BLUE}'{player.name}'{YELLOW}, урон: {RED}{round(damage)}")
            if player.hp <= 0:
                player.hp = 0
                print(f"{BLUE}'{player.name}'{YELLOW} погиб в бою от руки {RED}'{self.race}а'")
            else:
                print(f"{BLUE}{player.name}{YELLOW} у вас осталось {RED}{player.hp}{YELLOW} очков здоровья")
            print('-' * 20)
            sleep(2)

    def get_status_enemy(self):
        return not self.hp <= 0


def create_enemy():
    enemy_list = [Enemy('Гоблин'), Enemy('Орк'), Enemy('Чернокнижник')]
    return enemy_list


def get_list_enemy(enemy_list):
    print("*" * 20)
    for ind, enemy in enumerate(enemy_list, 1):
        print(f"{RED}{ind}. {enemy.race} ({enemy.hp}) ОЗ")
    print("*" * 20)


def get_status_enemy(enemy_list):
    ind = 0
    while ind < len(enemy_list):
        if enemy_list[ind].hp <= 0:
            enemy_list.pop(ind)
        ind += 1
    return enemy_list
