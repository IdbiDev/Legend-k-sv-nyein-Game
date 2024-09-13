import random


class Mob:
    def __init__(self, name: str, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        self.name: str = name
        self.health: int = health
        self.base_damage = base_damage
        self.crit_chance = crit_chance
        self.dodge_chance = dodge_chance
        self.hit_chance = hit_chance
        self.location = location
        self.bounty = max(10000, self.base_damage * self.health)

    def to_dict(self):
        return {"name": self.name, "health": self.health, "base_dmg": self.base_damage, "crit_chance": self.crit_chance,
                "dodge_chance": self.dodge_chance, "hit_chance": self.hit_chance, "location": self.location.position, "bounty": self.bounty}

    def kys_ilydodo(self):
        if self.location is not None:
            self.location.map.set(self.location.position, 0)

    def is_crit(self):
        return random.random() < self.crit_chance

    def is_dodge(self):
        return random.random() < self.dodge_chance

    def is_hit(self):
        return random.random() < self.hit_chance

    def is_dead(self):
        return self.health <= 0

    def attack(self, player):
        attack = self.base_damage
        is_dodge = player.is_dodge()
        is_hit = self.is_hit()
        is_crit = self.is_crit()
        #print("Mob res: ", is_dodge, is_hit, is_crit)
        if is_dodge or not is_hit:
            return {"player_dodge": is_dodge, "mob_hit": is_hit, "is_crit": False, "is_dead": False}
        if is_crit:
            attack *= 2
        if player.health - attack <= 0:
            # dead
            player.health = 0
            return {"player_dodge": is_dodge, "mob_hit": is_hit, "is_crit": is_crit, "is_dead": True}

        player.health -= attack
        return {"player_dodge": is_dodge, "mob_hit": is_hit, "is_crit": is_crit, "is_dead": False}


class Zombie(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        name = "Zombi"
        super().__init__(name, location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Goblin(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        name = "Goblin"
        super().__init__(name, location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Dragon(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        name = "Sárkány"
        super().__init__(name, location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Ghost(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        name = "Szellem"
        super().__init__(name, location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Gorgon(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        name = "Medúza"
        super().__init__(name, location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Goldenbug(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        super().__init__("Aranybogár", location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Giant(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        super().__init__("Óriás", location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Elf(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        super().__init__("Tündér", location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Golem(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        super().__init__("Gólem", location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Wolf(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        super().__init__("Farkas", location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Snake(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        super().__init__("Kígyó", location, health, base_damage, crit_chance, dodge_chance, hit_chance)


class Witch(Mob):
    def __init__(self, location, health: int, base_damage: int, crit_chance: float, dodge_chance: float,
                 hit_chance: float):
        super().__init__("Fekete Mágus", location, health, base_damage, crit_chance, dodge_chance, hit_chance)
