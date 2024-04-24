from items.item import Item

class Food(Item):
    def __init__(self, name, base_damage=0, crit_chance=0, hit_chance=0, dodge_chance=0, health=0):
        super().__init__(name, 1)
        self.dodge_chance = dodge_chance
        self.hit_chance = hit_chance
        self.crit_chance = crit_chance
        self.base_damage = base_damage
        self.health = health
