from items.gun import Gun
from items.food import Food
from items.item import Item
from items.armor import Armor
from items.sword import Sword
from items.talisman import Talisman
from table import Table, Column, Row

from menu import ItemSelectorMenu


class Inventory:
    def __init__(self, player, items: list[Item], size: int = 5):
        self.items = items
        self.size = size
        # self.item_ids = []
        self.talismans = []
        self.player = player

    def is_full(self) -> bool:
        return len(self.items) >= self.size


    def add_item(self,item):
        if len(self.items) < self.size:
            self.items.append(item)
            self.player.hand_slot = self.items[0]
        else:
            remove_item = ItemSelectorMenu(self).show_menu()
            self.items.remove(remove_item)
            self.items.append(item)


    def get_item_by_name(self, name: str) -> Item | None:
        for item in self.items:
            if item.name == name:
                return item

    def order(self) -> dict[int, list[Item]]:
        ordered_items: dict[int, list[Item]] = {}  # 0: Sword, 1: Gun, 2: Food, 3: Egyéb
        for item in self.items:
            if isinstance(item, Sword):
                if not 0 in ordered_items:
                    ordered_items[0] = [item]
                    continue
                ordered_items[0].append(item)
            elif isinstance(item, Gun):
                if not 1 in ordered_items:
                    ordered_items[1] = [item]
                    continue
                ordered_items[1].append(item)
            elif isinstance(item, Food):
                if not 3 in ordered_items:
                    ordered_items[3] = [item]
                    continue
                ordered_items[3].append(item)
            else:
                if not 4 in ordered_items:
                    ordered_items[4] = [item]
                    continue
                ordered_items[4].append(item)
        return dict(sorted(ordered_items.items()))

    def get_inventory(self) -> Table:
        ordered_items: dict[int, list[Item]] = self.order()

        names = [Row("Hátizsák", False, False, True)]
        selected = True
        for items in sorted(list(ordered_items.values()), key=lambda item: item[0].name):
            for item in items:
                names.append(Row(item.name, True, selected, False))
                selected = False
        column = [Column(names, 20)]

        return Table(self.player, column, bars={1: "-"})

items = {
    # name, base_damage=0, crit_chance=0, hit_chance=0, dodge_chance=0, health=0
    "Árnylovag Kardja":     Sword("Árnylovag Kardja",   25, 0.1, 0.58, 0.05),
    "Tűzszikrázó Pengék":   Sword("Tűzszikrázó Pengék", 37, 0.15, 0.4, 0.08),
    "Hóvirág Kardja":       Sword("Hóvirág Kardja",     61, 0.3, 0.1, 0.07),
    "Sötétség Szablyája":   Sword("Sötétség Szablyája", 43, 0.25, 0.25, 0.06),
    "Szellemkéz Kardja":    Sword("Szellemkéz Kardja",  28, 0.12, 0.12, 0.1),
    "Viharölelés Kardja":   Sword("Viharölelés Kardja", 250, 0.35, 0.5, 0.15),
    "Csillagfényes Dárda":  Sword("Csillagfényes Dárda", 72, 0.41, 0.1, 0.03),
    "Mennydörgő Pajzsölő":  Sword("Mennydörgő Pajzsölő", 53, 0.14, 0.33, 0.06),
    "Fény Kardja":          Sword("Fény Kardja", 100, 0.15, 0.43, 0.1),
    "Átokföldi Kések":      Sword("Átokföldi Kések", 32, 0.18, 0.42, 0.09),
    "Acél Kard":            Sword("Acél Kard", 12, 0.1, 0.42, 0.03, 30),


    "Sárkányszikra Puska":  Gun("Sárkányszikra Puska", 151, 0.5, -0.15, -0.21),
    "Árnyékvető Fegyver":   Gun("Árnyékvető Fegyver", 60, 0.1, 0.35, 0.1),
    "Szellemcsapás Löveg":  Gun("Szellemcsapás Löveg", 73, 0.65, 0.05, 0),
    "Mennydörgő Ágyú":      Gun("Mennydörgő Ágyú", 401, 0.3, -0.35, -0.5),
    "Tűznyelő Puska":       Gun("Tűznyelő Puska", 173, 0.4, -0.17, -0.28),
    "Villámvető Puska":     Gun("Villámvető Puska", 213, 0.8, -0.28, -0.3),
    "Varázstűz Fegyver":    Gun("Varázstűz Fegyver", 112, 0.33, 0, 0.08),
    "Káoszköd Puska":       Gun("Káoszköd Puska", 311, -0.13, -0.05, 0.23),
    "Atombomba":            Gun("Atombomba", 99999, 1, 1, -1),
    "Árnylövő Íj":          Gun("Árnylövő Íj", 83, 0.51, 0.2, 0.1),

    "Sárkányhús Gulyás":    Food("Sárkányhús Gulyás", 1, health=100),
    "Méregszívó Raguleves": Food("Méregszívó Raguleves", 1, health=30),
    "Pusztító Pörkölt":     Food("Pusztító Pörkölt", 1, health=150),
    "Vadász Pite":          Food("Vadász Pite", 1, health=10),
    "Bájital Bableves":     Food("Bájital Bableves", 1, health=55),
    "Sárkánysör":           Food("Sárkánysör", 1, health=33),
    "Varázspálinka":        Food("Varázspálinka", 1, health=40),
    "Árnykávé":             Food("Árnykávé", 1, health=45),
    "Tündértea":            Food("Tündértea", 1, health=90),
    "Vadászbor":            Food("Vadászbor", 1, health=85),
    # name, base_damage=0, crit_chance=0, hit_chance=0, dodge_chance=0, health=0
    "Árnyvas Páncél":       Armor("Árnyvas Páncél", 10, 0.05, 0.02, -0.02, 100),
    "Sötét Sárkánypáncél":  Armor("Sötét Sárkánypáncél", 5, 0.03, 0.1, 0.15, 150),
    "Éji Árnyak Páncélja":  Armor("Éji Árnyak Páncélja", 7, 0.01, 0.25, 0.17, 60),
    "Tűzszív Páncél":       Armor("Tűzszív Páncél", 10, 0.25, -0.05, 0, 110),
    "Mágikus Palást":       Armor("Mágikus Palást", 7, 0.1, 0.07, 0.2, 0),
    "Csodaszárny Láncing":  Armor("Csodaszárny Láncing", 3, -0.25, 0.2, 0.25, 75),
    "Titánok Pajzsa":       Armor("Titánok Pajzsa", 15, -0.1, 0.05, 0.07, 250),
    "Gyémántbőr Páncél":    Armor("Gyémántbőr Páncél", 4, 0.3, 0.1, -0.1, 90),
    "Démoni Páncél":        Armor("Démoni Páncél", 13, 0.15, 0.1, 0.1, 200),
    "Újonc Láncing":        Armor("Újonc Láncing", 3, 0, 0, 0.1, 15),

    "Szellemkő Amulett":        Talisman("Szellemkő Amulett", 10, 0.05, 0.02, 0.02, 50),
    "Árnyfog Talizmán":         Talisman("Árnyfog Talizmán", 5, 0.03, 0.1, 0.15, 75),
    "Titánkard Medál":          Talisman("Titánkard Medál", 7, 0.01, 0.25, 0.17, 30),
    "Varázstűz Gyűrű":          Talisman("Varázstűz Gyűrű", 10, 0.25, 0.05, 0, 55),
    "Sárkányfog Kő":            Talisman("Sárkányfog Kő", 3, 0.25, 0.2, 0.25, 0),
    "Szirénkagyló Karperec":    Talisman("Szirénkagyló Karperec", 15, 0.1, 0.05, 0.07, 125),
    "Káoszszív Medál":          Talisman("Káoszszív Medál", 4, 0.3, 0.1, 0.1, 45),
    "Lávagyűrű":                Talisman("Lávagyűrű", 9, 0.05, 0.04, 0.1, 10),
    "Vadászszellem Fülbevaló":  Talisman("Vadászszellem Fülbevaló", 13, 0.15, 0.1, 0.1, 100),
    "Sárkányvérszív Medál":     Talisman("Sárkányvérszív Medál", 3, 0, 0, 0.1, 90),
}

blacksmith_items = {
    items["Árnylovag Kardja"]:5000,
    items["Tűzszikrázó Pengék"]: 7000,
    items["Hóvirág Kardja"]: 3000,
    items["Sötétség Szablyája"]: 6500,
    items["Szellemkéz Kardja"]: 4500,
    items["Viharölelés Kardja"]: 20000,
    items["Csillagfényes Dárda"]: 11000,
    items["Mennydörgő Pajzsölő"]: 9500,
    items["Fény Kardja"]: 17500,
    items["Átokföldi Kések"]: 6000,
}

armorer_items = {
    items["Árnyvas Páncél"]:2000,
    items["Sötét Sárkánypáncél"]: 10000,
    items["Éji Árnyak Páncélja"]: 3000,
    items["Tűzszív Páncél"]: 5000,
    items["Csodaszárny Láncing"]: 9851,
    items["Titánok Pajzsa"]: 7500,
    items["Gyémántbőr Páncél"]: 7500,
    items["Mágikus Palást"]: 7500,
    items["Démoni Páncél"]: 7500,
    items["Újonc Láncing"]: 7500
}

farmer_items = {
    items["Sárkányhús Gulyás"]:1000,
    items["Méregszívó Raguleves"]: 300,
    items["Pusztító Pörkölt"]: 1500,
    items["Vadász Pite"]: 100,
    items["Bájital Bableves"]: 550,
    items["Sárkánysör"]: 330,
    items["Varázspálinka"]: 400,
    items["Árnykávé"]: 450,
    items["Tündértea"]: 900,
    items["Vadászbor"]: 850
}

hunter_items = {
    items["Sárkányszikra Puska"]:15100,
    items["Árnyékvető Fegyver"]: 6000,
    items["Szellemcsapás Löveg"]: 7350,
    items["Mennydörgő Ágyú"]: 40100,
    items["Tűznyelő Puska"]: 17300,
    items["Villámvető Puska"]: 21300,
    items["Varázstűz Fegyver"]: 11200,
    items["Káoszköd Puska"]: 31100,
    # items["Atombomba"]: 1500,
    items["Árnylövő Íj"]: 8300
}

wizard_items = {
    items["Szellemkő Amulett"]:2500,
    items["Árnyfog Talizmán"]: 3000,
    items["Titánkard Medál"]: 1500,
    items["Varázstűz Gyűrű"]: 4000,
    items["Sárkányfog Kő"]: 3800,
    items["Szirénkagyló Karperec"]: 6000,
    items["Káoszszív Medál"]: 5000,
    items["Lávagyűrű"]: 4300,
    items["Vadászszellem Fülbevaló"]: 6500,
    items["Sárkányvérszív Medál"]: 3000
}


def get_items():
    return items

def key_to_item(item_key):
    return items[item_key]


def key_to_name(item_key):
        return key_to_item(item_key).name


def name_to_item(name):
    for k, v in items.items():
        if v.name == name:
            return v
