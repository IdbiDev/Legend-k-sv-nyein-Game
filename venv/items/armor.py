from items.item import Item

"""
    Árnyvas Páncél

Alap sebzés: -5%
Kritikus csapás: +10%
Dodge esély: +5%

    Viharvájta Vértek

Találat esély: +5%
Kritikus csapás: +15%

    Bátorító Brígandine

Alap sebzés: -3%
Dodge esély: +8%

    Sárkánysíp Páncél

Alap sebzés: -7%
Kritikus csapás: +20%
Dodge esély: +3%

    Éji Árnyak Páncélja

Kritikus csapás: +10%
Dodge esély: +10%

    Hólehelet Harnézat

Találat esély: +8%
Dodge esély: +5%

    Ezüstkard Páncél

Alap sebzés: -4%
Találat esély: +7%
Kritikus csapás: +12%

    Tűzszív Páncél

Alap sebzés: -6%
Kritikus csapás: +25%

    Védőnő Viselete

Alap sebzés: -2%
Dodge esély: +10%
Találat esély: +5%

    Csodaszárny Láncing

Dodge esély: +15%
Kritikus csapás: +10%
                        
"""

class Armor(Item):
    def __init__(self, name, base_damage=0, crit_chance=0, hit_chance=0, dodge_chance=0, health=0):
        super().__init__(name, 1)
        self.dodge_chance = dodge_chance
        self.hit_chance = hit_chance
        self.crit_chance = crit_chance
        self.base_damage = base_damage
        self.health = health