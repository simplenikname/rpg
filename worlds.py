from abc import abstractmethod


class WorldTemplate(dict):
    def __init__(self, name, difficult, enemies: set, bosses, mepl):
        self.name = name
        self.difficult = difficult
        self.enemies = enemies
        self.bosses = bosses
        self.max_enemies_per_level = mepl


def r(min, max):
    return list(range(min, max))


dummy = {
    'name': 'Игровой объект',
    'max_health': 10,
    'max_energy': 10,
    'damage_rng': [0]
}

battle_classes = {
    'Воин': {
        'battle_class': 'Воин',
        'max_health': 100,
        'max_energy': 30,
        'damage_rng': r(6, 9)
    },
    'Маг': {
        'battle_class': 'Маг',
        'max_health': 70,
        'max_energy': 60,
        'damage_rng': r(5, 7)
    },
    'Бог': {
        'battle_class': 'Бог',
        'max_health': 99999999,
        'max_energy': 99999999,
        'damage_rng': r(1, 150)
    }
}

world_templates = [
    WorldTemplate(
        'Святой Лес',
        1,
        (
            {
                'levels': [1, 2, 3],
                'name': 'Злой кролик',
                'max_health': 10,
                'max_energy': -1,  # -1 == бесконечность
                'damage_rng': r(1, 3)  # диапазон чисел от числа A до числа B
            },
            {
                'levels': [4, 5],
                'name': 'Медвеволк',
                'max_health': 20,
                'max_energy': -1,
                'damage_rng': r(5, 10)
            },
            {
                'levels': [2, 3, 4, 5],
                'name': 'Малый дух леса',
                'max_health': 5,
                'max_energy': -1,
                'damage_rng': r(2, 5)
            }

        ),
        [
            {
                'name': 'Зараженный медвеволк',
                'max_health': 100,
                'max_energy': 50,
                'damage_rng': r(10, 20)
            }
        ],
        1)
]


class Abil(dict):
    def __init__(self):
        self.host: object
        self.phisical_damage = True
        self.need_energy = True

    @abstractmethod
    def use(self):
        pass


class Heal(Abil):
    # Восстанавливает 10% от максимального здоровья
    def __init__(self):
        super().__init__()
        self.info = self.__doc__

    def use(self):
        self.host.health += self.host.max_health / 100 * 10


abils = (Heal,)
