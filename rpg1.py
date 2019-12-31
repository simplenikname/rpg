from worlds import world_templates, dummy, battle_classes  # объект шаблон
from random import choice
from os import system


class LevelHistory(dict):
    def __init__(self, level):
        self.level = level
        self.all_actons = []
        self.last_actions = []
        self.recent_action_length = 5
        self.recent_action: str

    def write(self, action):
        self.all_actons.append(action)

    def __getattr__(self, attr):
        self.last_actions = self.all_actons[:4:-1]
        self.recent_action = self.all_actons[-1]
        return self[attr]


# класс реализующий отображение списка для выбора элемента(-ов)
class Menu:
    def __init__(self, values: dict, item: str):
        self.values = values
        self.item = item

    def show(self):
        system('clear')
        for k, v in self.values.items():
            print(f'{k}) {v}')
        while 1:
            ans = input(f'Выберите {self.item} из списка:')
            if ans.isdigit():
                return int(ans)
            else:
                print('Некорректный ввод. Повтор.')


# шаблон для классов игры
class GameObject(dict):
    def __init__(self):
        self.max_health = 0
        self.max_energy = 0
        self.energy = self.max_energy
        self.health = self.max_health
        self.damage_rng = [0, 1]
        self.abils = []
        self.survived_turns = 0

    def upd(self, new_instances):
        self.__dict__.update(new_instances)


# класс игрока
class Player(GameObject):
    def __init__(self, name, btl_class):
        super().__init__()
        self.upd(dummy)
        self.type = 'hu'  # hu(man) - человек
        self.name = name
        self.btl_class = btl_class

    def turn(self) -> str:
        _actions = {}
        for n, i in enumerate(self.abils):
            _actions[n] = i
        _actions[99] = 'Пропустить ход'
        _actions[88] = 'Агаы'
        while 1:
            pass


# класс врага
class Enemy(GameObject):  # TODO: сделать нормальный ИИ
    def __init__(self):
        super().__init__()
        self.upd(dummy)
        self.type = 'ai'  # ai - ИИ

    def turn(self) -> str:
        pass


# иерархия игрового окружения
# класс игры
class Game:
    def __init__(self, difficult: int):
        self.worlds: list = [World(i, self) for i in world_templates]
        self.difficult = difficult

    def _setupPlayer(self):  # TODO: можно реализовать лучше?
        player_name = input('Введите имя: ')
        class_choose = {
            1: 'Воин',
            2: 'Маг',
            99: 'Бог'
        }
        self.player = Player(player_name, battle_classes[
            class_choose[Menu(class_choose).show()]
        ])

    def startGame(self, mode):
        self.mode = mode
        # создание и настройка игрока
        self._setupPlayer()
        # начало игры
        for i in self.worlds:
            i.enter()


# класс игрового мира
class World(dict):  # TODO: добавить больше настроек
    def __init__(self, instances, game: Game):
        self.name = ''                  #
        self.difficult = 0              # пустые переменные
        self.enemies = 0                # для работы
        self.bosses = 0                 # автодополнения
        self.max_enemies_per_level = 0  #
        self.__dict__.update(instances)
        self.game = game
        self.player = self.game.player
        self.levels = [Level(self, i + 1) for i in range(5)]
        self.dead_enemies = []

    def enter(self):
        for i in self.levels:
            i.start()


# класс уровня
class Level(dict):
    def __init__(self, world: World, num):
        self.num = num
        self.world = world
        self.player = self.world.player
        self.enemies = []
        self.history = LevelHistory(self)
        # заполнение листа с врагами
        _tmp = []
        for e in self.world.enemies:
            if num in e['levels']:
                _tmp.append(e)
        for i in range(self.world.max_enemies_per_level):
            self.enemies.append(choice(_tmp))
        self.objects = self.enemies + self.player

    def start(self):
        while 1:
            for i in self.objects:
                self.history.write(i.turn())
                for i in self.objects:
                    if i.health <= 0:
                        pass
                    else:
                        i.survived_turns += 1
