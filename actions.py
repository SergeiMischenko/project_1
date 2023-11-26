"""Файл связанный с выбором действий в различных ситуациях"""

from time import sleep

from my_coloram import MAGENTA, YELLOW, RED, CYAN, BLUE
import events
import enemy
import main


class Action:
    """
        Класс для представления и обработки выбранных действий в том или ином случае.
        Attribute:
            ACTIONS: dict[int: str] Словарь ключи это номер действия, значение это название действия.
            XP_FOR_FIGHT: int Общее количество опыта за бой
            GOLD_FOR_FIGHT: int Общее количество золота за бой
        Public Methods:
            print_list_actions(cls)
            get_action(enemy_list, player, text=None)
            valid_target(value, enemy_list)
            end_fight(cls, player)
            healing_at_the_medic(player, choice=None)
        """
    ACTIONS = {1: "Атаковать противника", 2: "Встать в защитную стойку (+40 Брони на 1 ход)",
               3: "Осмотреть противника", 4: "О себе", 5: "Сбежать с поля боя"}

    XP_FOR_FIGHT = 0
    GOLD_FOR_FIGHT = 0

    @staticmethod
    def _handler_action(value, enemy_list, player):
        """
        Обработчик действий, на вход получает введённое действие, список объектов Enemy и объект Player.
        :param value: str
            Значение в строке введённое с клавиатуры
        :param enemy_list: list[Enemy]
            Список объектов Enemy
        :param player: Player
            Объект Player
        """
        match value:
            case "1" | "Атаковать противника" | "Атаковать" | "Атака":
                enemy.Enemy.print_list_enemy(enemy_list)
                Action._do_attack(enemy_list, player)
                if player.hp and enemy_list:
                    main.print_press_enter()
                player.stand = False
            case "2" | "Встать в защитную стойку" | "Встать" | "Стойка":
                if player.stand:
                    print(f"{MAGENTA}Вы уже в защитной стойке")
                else:
                    player.stand = True
                    enemy.Enemy.enemy_attacks(enemy_list, player)
                main.print_press_enter()
            case "3" | "Осмотреть противника" | "Осмотреть":
                enemy.Enemy.print_stats_enemy(enemy_list)
                main.print_press_enter()
            case "4" | "О себе" | "Я":
                player.print_stats_player()
                main.print_press_enter()
            case "5" | "Сбежать с поля боя" | "Бежать":
                enemy.Enemy.enemy_attacks(enemy_list, player)
                player.escaped = True
            case _:
                print(f"\n{MAGENTA}Такого действия ты не можешь совершить, возможно ты ошибся")
                Action.get_action(enemy_list, player, text=f"{YELLOW}Попробуй ещё разок: ")

    @classmethod
    def print_list_actions(cls):
        """Метод выводит список действий из словаря ACTIONS (Порядковый номер, Имя)"""
        print("-*" * 20)
        for ind, action in cls.ACTIONS.items():
            print(f"\t{YELLOW}{ind}. {action}")
        print("-*" * 20)

    @staticmethod
    def get_action(enemy_list, player, text=None):
        """
        Метод получает на вход список Enemy, Player и выводимый текст
        (по-умолчанию: "Выберите ваше действие из списка выше: "), возвращает обработчик с переданными аргументами
        :param enemy_list: list[Enemy]
            Список объектов Enemy
        :param player: Player
            Объект Player
        :param text: None | str
        :return: Возвращает обработчик с переданными аргументами
        """
        if text is None:
            text = "Выберите ваше действие из списка выше: "
        return Action._handler_action(input(f"{YELLOW}{text}").capitalize(),
                                      enemy_list, player)

    @staticmethod
    def _do_attack(enemy_list, player):
        """
        Обработчик который, вызывается после того как пользователь выбирает действие Атаковать.
        Пользователь вводит цель, она проверяется на валидность. Герой атакует, затем атакует живой противник
        """
        target = Action.valid_target(input(f"{YELLOW}Выберите кого атаковать: ").capitalize(), enemy_list)
        player.attack(enemy_list[target])
        enemy.Enemy.enemy_attacks(enemy_list, player)

    @staticmethod
    def valid_target(value, enemy_list):
        """
        Проверка валидности введённой цели, нахождение его в списке Enemy, возвращает индекс в списке
        :param value: str
            На входе получает строку с числом либо именем расы
        :param enemy_list: list[Enemy]
            Список объектов Enemy
        Variables:
            enemy_len: list[str]
                Список номеров живых Enemy
            enemy_race_list: list[str]
                Список рас объектов Enemy
        :return: Возвращает - индекс введённой цели
        """
        enemy_len = list(map(str, range(1, len(enemy_list) + 1)))
        enemy_race_list = [enemy_.race for enemy_ in enemy_list]
        while True:
            if not value.strip():
                print(f"\n{MAGENTA}Ты же ничего не ввёл")
            elif value not in enemy_race_list and value not in enemy_len:
                print(f"\n{MAGENTA}Такого врага тут нет, возможно ты ошибся")
            else:
                break
            value = input(f"{YELLOW}Попробуй ещё разок: ").capitalize()
        if value.isalpha():
            value = enemy_race_list.index(value) + 1
        return int(value) - 1

    @classmethod
    def end_fight(cls, player):
        """
        Метод для вывода информации в конце боя: Сколько было получено опыта, золота, был ли выполнен квест,
        был ли поднят уровень Героя
        """
        print(f"{YELLOW}*" * 43)
        print(f"{CYAN}Вы одолели всех своих врагов и за этот бой получили "
              f"{YELLOW}['{cls.XP_FOR_FIGHT}' Опыта и '{cls.GOLD_FOR_FIGHT}' Золота]")
        print(f"{YELLOW}*" * 43)
        if player.quest:  # Если квест выполнен выдаётся дополнительно 75% опыта и 2х золота
            player.quest = False
            quest_reward = (cls.XP_FOR_FIGHT * 0.75, cls.GOLD_FOR_FIGHT * 2)
            cls.XP_FOR_FIGHT += quest_reward[0]
            cls.GOLD_FOR_FIGHT += quest_reward[1]
            print(f"{CYAN}За выполненное задание вы получили в награду: "
                  f"{YELLOW}['{quest_reward[0]}' Опыта и '{quest_reward[1]}' Золота]")
        player.check_and_change_lvl_up()
        cls.XP_FOR_FIGHT, cls.GOLD_FOR_FIGHT = 0, 0
        while True:
            choice = input(f"\n{YELLOW}Хотите продолжить? {RED}(Да/Нет){YELLOW}: ").capitalize()
            if choice == "Нет":
                events.Event.die()
            elif choice == "Да":
                break

    @staticmethod
    def healing_at_the_medic(player):
        """
        Метод для обработки случая когда игрок заходит к Травнику, тут происходят все проверки есть ли ещё золото
        у игрока, полное ли здоровье и хочет ли он ещё излечиться.
        """
        while True:
            print(f"{BLUE}У вас в кармане {YELLOW}[{player.gold} Золота]{BLUE} ваше здоровье: "
                  f"{RED}[{int(player.hp)}/{int(player.max_hp)}]")
            value = input(f"{YELLOW}Сколько здоровья хотите вылечить? ({RED}1 ОЗ {YELLOW}- {YELLOW}1 Золотая): ")
            sleep(1)
            if player.gold < int(value):
                print(f"{MAGENTA}У вас не достаточно золота в кармане\n")
                continue
            if int(value) >= int(player.max_hp - player.hp):
                print(f"\n{YELLOW}Ваше здоровье полностью восстановлено")
                player.gold -= (player.max_hp - player.hp)
                player.hp = player.max_hp
                break
            player.hp += int(value)
            player.gold -= int(value)
            print(f"\n{YELLOW}Травник излечил вас на {RED}[{value} ОЗ]{YELLOW} у вас {RED}[{int(player.hp)} ОЗ]"
                  f"{YELLOW} и [{int(player.gold)} Золота] в кармане")
            if player.gold and (int(player.hp) != int(player.max_hp)):
                choice = None
                while choice != "Уйти":
                    choice = input(f"{CYAN}Желаете продолжить путешествие или приобрести дополнительные очки здоровья? "
                                   f"{RED}(Купить/Уйти): ").capitalize()
                    print()
                    if choice == "Купить":
                        Action.healing_at_the_medic(player)
                        break
            break
