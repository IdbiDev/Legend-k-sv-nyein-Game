import os, platform, time,random
from mob import Mob
from mob import Zombie
from fight import Fight
from dialog import Dialog
from maps.map import Map
from maps.border import Border
from maps.portal import Portal
from items.food import Food
from items.inventory import Inventory
from maps.villager import Villager
from menu import ConfirmMenu

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

class Player:
    def __init__(self, name, current_map: Map):
        self.health: int = 150
        self.current_map: Map = current_map
        self.position = current_map.find_player()
        self.name: str = name
        self.balance = 10000 #10000
        self.base_damage = 5
        self.crit_chance = 0.1
        self.dodge_chance = 0.1
        self.hit_chance = 0.75
        self.inventory: Inventory = Inventory(self,  [])
        self.hand_slot = None
        self.armor_slot = None
        self.is_fighting = False
        self.current_fight = None



    def get_calculated_stats(self) -> dict[str, float]:
        data = {"base_damage": self.base_damage, "crit_chance": self.crit_chance, "dodge_chance": self.dodge_chance, "hit_chance": self.hit_chance,"health":self.health}
        if self.hand_slot is not None:
            if not isinstance(self.hand_slot, Food):
                data["base_damage"] += self.hand_slot.base_damage
                data["crit_chance"] += self.hand_slot.crit_chance
                data["dodge_chance"] += self.hand_slot.dodge_chance
                data["hit_chance"] += self.hand_slot.hit_chance
            elif isinstance(self.hand_slot, Food):
                data["health"] += self.hand_slot.health
        if self.armor_slot is not None:
            data["base_damage"] += self.armor_slot.base_damage
            data["crit_chance"] += self.armor_slot.crit_chance
            data["dodge_chance"] += self.armor_slot.dodge_chance
            data["hit_chance"] += self.armor_slot.hit_chance
            data["health"] += self.armor_slot.health

        for t in self.inventory.talismans:
            data["base_damage"] += t.base_damage
            data["crit_chance"] += t.crit_chance
            data["dodge_chance"] += t.dodge_chance
            data["hit_chance"] += t.hit_chance
            data["health"] += t.health

        data["crit_chance"] = min(data["crit_chance"], 1)
        data["dodge_chance"] = min(data["dodge_chance"], 1)
        data["hit_chance"] = min(data["hit_chance"], 1)
        return data

    def replace_placeholders(self, text: str):
        data = self.get_calculated_stats()
        if self.current_fight is not None:
            text = text.replace("%mob_health%", str(self.current_fight.opponent.health))

            text = text.replace("%is_mob_hit%", "" if self.current_fight.next_round else "⚔") # ⚔
            text = text.replace("%is_player_hit%", "⚔" if self.current_fight.next_round else "")

        text = text.replace("%crit_chance%", str(int(data["crit_chance"] * 100)))
        text = text.replace("%dodge_chance%", str(int(data["dodge_chance"] * 100)))
        text = text.replace("%hit_chance%", str(int(data["hit_chance"] * 100)))
        text = text.replace("%health%", str(data["health"]))
        text = text.replace("%base_damage%", str(data["base_damage"]))
        text = text.replace("%player%", str(self.name))
        text = text.replace("%balance%", str(self.balance))
        return text


    def is_crit(self):
        data = self.get_calculated_stats()
        return random.random() < data["crit_chance"]


    def is_dodge(self):
        data = self.get_calculated_stats()
        return random.random() < data["dodge_chance"]


    def is_hit(self):
        data = self.get_calculated_stats()
        return random.random() < data["hit_chance"]


    def attack(self, opponent):
        data = self.get_calculated_stats()
        attack = data["base_damage"]
        is_dodge = opponent.is_dodge()
        is_hit = self.is_hit()
        is_crit = self.is_crit()
        #print("Player res: ",is_dodge,is_hit,is_crit)
        if is_dodge or not is_hit:
            return {"mob_dodge": is_dodge, "player_hit": is_hit, "is_crit": False, "is_dead": False}
        if is_crit:
            attack *= 2
        if opponent.health - attack <= 0:
            # dead
            opponent.health = 0
            return {"mob_dodge": is_dodge, "player_hit": is_hit, "is_crit": is_crit, "is_dead": True}

        opponent.health -= attack
        return {"mob_dodge": is_dodge, "player_hit": is_hit, "is_crit": is_crit, "is_dead": False}


    def update_map(self, old, old_map):
        if old_map == self.current_map:
            self.current_map.grid[old[0]][old[1]] = 0
            self.current_map.grid[self.position[0]][self.position[1]] = 1
        else:
            old_map.grid[old[0]][old[1]] = 0
            clear()


    def move_x(self, forward):
        if forward:
            loc_number = self.current_map.grid[self.position[0]][self.position[1] + 1]
            if loc_number == 0:
                self.position[1] += 1
            else:
                self.check_number(loc_number, [self.position[0], self.position[1] + 1])
        else:
            loc_number = self.current_map.grid[self.position[0]][self.position[1] - 1]
            if loc_number == 0:
                self.position[1] -= 1
            else:
                self.check_number(loc_number, [self.position[0], self.position[1] - 1])


    def move_y(self, forward):
        if forward:
            loc_number = self.current_map.grid[self.position[0] + 1][self.position[1]]
            if loc_number == 0:
                self.position[0] += 1
            else:
                self.check_number(loc_number, [self.position[0] + 1, self.position[1]])
        else:
            loc_number = self.current_map.grid[self.position[0] - 1][self.position[1]]
            if loc_number == 0:
                self.position[0] -= 1
            else:
                self.check_number(loc_number,[self.position[0] - 1,self.position[1]])


    def check_number(self, loc, new_pos):
        if isinstance(loc, Border):
            loc.border_break()
        elif isinstance(loc, Portal):
            if loc.is_next(new_pos) and loc.next_location.map == self.current_map:
                # ToDo: teleport to loc.current_location
                new_pos = loc.current_location.get_nearest_free()
                self.current_map.set(self.position, 0)
                self.position = new_pos
                self.current_map = loc.current_location.map
                self.current_map.set(self.position, 1)
            elif loc.is_current(new_pos) and loc.current_location.map == self.current_map:
                # ToDo: teleport to loc.next_location
                new_pos = loc.next_location.get_nearest_free()

                self.current_map.set(self.position, 0)
                self.position = new_pos

                self.current_map = loc.next_location.map
                self.current_map.set(self.position, 1)


            # case 2:
            #     self.current_map = self.maps[0]
            #     self.position = self.last_positions[self.current_map]
            #     clear()
            #     Dialog(f"{self.name}: Ahogy kiértem, újra megnyílt előttem a világ szépsége... de meddig?").print()
            #     #print_dialog(f"{self.name}: Ahogy kiértem, újra megnyílt előttem a világ szépsége.. de meddig?")
            # case 3:
            #     self.current_map = self.maps[1]
            #     self.position = self.last_positions[self.current_map]
            #     clear()
            #     Dialog(f"{self.name}: Ahogy elsötétült körülöttem a világ, éreztem, hogy nem vagyok egyedül itt...").print()
            #     #print_dialog(f"{self.name}: Ahogy elsötétült körülöttem a világ, éreztem hogy nem vagyok egyedül itt..")
        elif isinstance(loc, Mob):
            clear()
            # Dialog(f"{self.name}: Ahogy mentem találkoztam egy zombival... és megindult felém!").print()
            res = ConfirmMenu(f"{self.name}: Ahogy mentem találkoztam egy szörnnyel.. Ez egy {loc.name}!")
            res = res.show_menu()
            if res:
                self.is_fighting = True
                self.current_fight = Fight(self, loc)
            else:
                Dialog(f"{self.name} elfutott!").print()
        elif isinstance(loc, Villager):
            clear()
            res = ConfirmMenu(f"Találkoztál {loc.name} polgárral!")
            res = res.show_menu()
            if res:
                loc.interact(self)


