from mob import *
from random import randint, random, choice, randrange
from messages import MessageType
from maps.location import Location
from maps.portal import Portal
from maps.border import Border
from maps.villager import *
import json


class Map:
    def __init__(self, id, name: str, size_y: int, size_x: int, mob_spawn=False, is_village=False, is_spawn=False):
        # Generate blank map
        self.grid = [[0 for _ in range(0, size_x)] for _ in range(0, size_y)]
        self.mob_spawn = mob_spawn
        self.is_village = is_village
        # self.join_position = join_position
        self.name = name
        self.id = id
        self.size_y = size_y
        self.size_x = size_x
        self.is_spawn = is_spawn
        self.in_portals = []
        self.out_portals = []

    def to_dict(self):
        return {"id": self.id, "name": self.name, "size_x": self.size_x, "size_y": self.size_y,
                "is_spawn": self.is_spawn, "is_village": self.is_village, "is_mob_spawn": self.mob_spawn,
                "in_portals": [x.to_dict() for x in self.in_portals],
                "out_portals": [x.to_dict() for x in self.out_portals],
                "grid": [
                    [value.to_dict() if not isinstance(value, int) else value for value in x_list]
                    for x_list in self.grid
                ]
                }

    def set(self, position: list[int], value):
        self.grid[position[0]][position[1]] = value

    def find_player(self):
        for y, x_list in enumerate(self.grid):
            for x, value in enumerate(x_list):
                if value == 1:
                    #return Location(self,[y,x])
                    return [y, x]

    def get_mobs(self):
        ret = 0
        for y, x_list in enumerate(self.grid):
            for x, value in enumerate(x_list):
                if isinstance(value, Mob):
                    ret += 1
        return ret

    def calc_freepos(self) -> float:
        free_pos: int = 0
        for y, x_list in enumerate(self.grid):
            for x, value in enumerate(x_list):
                if value == 0:
                    free_pos += 1
        return free_pos / (self.size_x * self.size_y)

    def generate_map(self):
        # Generate borders
        for y, yv in enumerate(self.grid):
            self.grid[y][0] = Border(Location(self, [y, 0]))
            self.grid[y][len(yv) - 1] = Border(Location(self, [y, len(yv) - 1]))
            for x, xv in enumerate(yv):
                self.grid[0][x] = Border(Location(self, [0, x]))
                self.grid[len(self.grid) - 1][x] = Border(Location(self, [len(self.grid) - 1, x]))
        if self.is_spawn:
            self.place_player()
        if self.mob_spawn:
            self.place_mobs(randint(5, 15))
        if self.is_village:
            self.place_npc()

        self.generate_obstacles()

    def generate_obstacles(self):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # , (-1, -1), (1, -1), (-1, 1), (1, 1)
        while self.calc_freepos() > 0.75:
            random_center = self.find_clear(is_random=True)
            if random_center is not None:
                random_chance = 1
                random_direction = choice(directions)
                while random_chance >= random.random():

                    new_y, new_x = random_center[0] + random_direction[0], random_center[1] + random_direction[1]
                    if self.grid[new_y][new_x] == 0:
                        self.grid[new_y][new_x] = Border(Location(self, [new_y, new_x]), True)
                        random_chance -= 0.08
                        random_center = [new_y, new_x]
                        if not (self.calc_freepos() > 0.75):
                            break
                    else:
                        random_direction = choice(directions)

    def place_npc(self):
        for i in range(randint(1, 3)):
            pos = self.find_clear(is_random=True)
            loc = Location(self, pos)
            loc.set(Blacksmith(loc))
        for i in range(randint(1, 3)):
            pos = self.find_clear(is_random=True)
            loc = Location(self, pos)
            loc.set(Armorer(loc))
        for i in range(randint(1, 3)):
            pos = self.find_clear(is_random=True)
            loc = Location(self, pos)
            loc.set(Farmer(loc))
        for i in range(randint(1, 3)):
            pos = self.find_clear(is_random=True)
            loc = Location(self, pos)
            loc.set(Hunter(loc))
        for i in range(randint(1, 3)):
            pos = self.find_clear(is_random=True)
            loc = Location(self, pos)
            loc.set(Wizard(loc))
        # for i in range(randint(1,3)):
        #     pos = self.find_clear(is_random=True)
        #     loc = Location(self,pos)
        #     loc.set(Blacksmith("cat",loc))

    def find_clear(self, is_random):
        if not is_random:
            for y, x_list in enumerate(self.grid):
                for x, value in enumerate(x_list):
                    if value == 0:
                        return [y, x]
        else:
            maxY = len(self.grid) - 1
            maxX = len(self.grid[0]) - 1
            while True:
                y = randint(1, maxY)
                x = randint(1, maxX)
                if self.grid[y][x] == 0:
                    return [y, x]

    def place_player(self):
        maxY = len(self.grid) - 1
        maxX = len(self.grid[0]) - 1
        while True:
            y = randint(1, maxY)
            x = randint(1, maxX)
            if self.grid[y][x] == 0:
                self.grid[y][x] = 1
                break

    def place_mobs(self, amount: int):
        mobs = [Zombie, Goblin, Dragon, Ghost, Gorgon, Goldenbug, Giant, Elf, Golem, Wolf, Snake]
        maxY = len(self.grid) - 1
        maxX = len(self.grid[0]) - 1
        already_placed = 0
        while already_placed < amount:
            y = randint(0, maxY)
            x = randint(0, maxX)
            if self.grid[y][x] == 0:
                mob = choice(mobs)
                #print(mob)
                loc = Location(self, [y, x])
                # location, health: int, base_damage: int, crit_chance: float, dodge_chance: float, hit_chance: float
                if mob == Zombie:
                    self.grid[y][x] = Zombie(loc, randint(200, 300), randint(7, 15), randint(0, 5) / 100,
                                             randint(5, 10) / 100, randint(15, 25) / 100)
                elif mob == Goblin:
                    self.grid[y][x] = Goblin(loc, randint(75, 200), randint(3, 8), randint(5, 10) / 100,
                                             randint(20, 40) / 100, randint(45, 65) / 100)
                elif mob == Dragon:
                    self.grid[y][x] = Dragon(loc, randint(250, 370), randint(15, 22), randint(0, 5) / 100,
                                             randint(25, 45) / 100, randint(25, 45) / 100)
                elif mob == Ghost:
                    self.grid[y][x] = Ghost(loc, randint(50, 100), randint(50, 75), randint(0, 1) / 100,
                                            randint(50, 70) / 100, randint(12, 30) / 100)
                elif mob == Gorgon:
                    self.grid[y][x] = Gorgon(loc, randint(150, 200), randint(2, 9), randint(65, 100) / 100,
                                             randint(0, 5) / 100, randint(70, 80) / 100)
                elif mob == Goldenbug:  # health                dmg            crit        dodge             hit
                    self.grid[y][x] = Goldenbug(loc, randint(10, 15), randint(1000, 5000), 0, randint(40, 75) / 100, 0)
                elif mob == Giant:  # health                dmg                crit                 dodge                         hit
                    self.grid[y][x] = Giant(loc, randint(450, 650), randint(12, 23), randint(0, 20) / 100,
                                            randint(0, 2) / 100, randint(50, 80) / 100)
                elif mob == Elf:  # health                dmg                crit                 dodge                         hit
                    self.grid[y][x] = Elf(loc, randint(250, 400), randint(22, 33), randint(10, 23) / 100,
                                          randint(14, 30) / 100, randint(30, 43) / 100)
                elif mob == Golem:  # health                  dmg                   crit                    dodge                         hit
                    self.grid[y][x] = Golem(loc, randint(750, 1000), randint(5, 10), randint(7, 14) / 100,
                                            randint(0, 10) / 100, randint(7, 20) / 100)
                elif mob == Wolf:  # health                  dmg                   crit                    dodge                         hit
                    self.grid[y][x] = Wolf(loc, randint(150, 225), randint(15, 23), randint(30, 47) / 100,
                                           randint(15, 30) / 100, randint(15, 30) / 100)
                elif mob == Snake:  # health                  dmg                   crit                    dodge                         hit
                    self.grid[y][x] = Snake(loc, randint(75, 300), randint(5, 17), randint(27, 38) / 100,
                                            randint(5, 15) / 100, randint(20, 33) / 100)
                already_placed += 1

    def get_map(self):

        ret = f"Terület: {self.name}\n\n"
        for y, _ in enumerate(self.grid):
            for x, __ in enumerate(_):
                if isinstance(self.grid[y][x], Border):
                    ret += "█"  # ■█
                elif self.grid[y][x] == 0:
                    ret += " "  # "☐"
                elif self.grid[y][x] == 1:
                    ret += "○"
                elif self.grid[y][x] == 2:
                    ret += "H"
                elif self.grid[y][x] == 3:
                    ret += "⸕"  # ⚒ ⚔
                elif isinstance(self.grid[y][x], Portal):
                    ret += "Ⓟ"
                # elif isinstance(self.grid[y][x], Mob):
                #     ret += "!"
                elif isinstance(self.grid[y][x], Villager):
                    ret += "⌂"
                else:
                    ret += "!"  # ⌂ ⌂
            ret += "\n"
        return ret


class MapManager:
    def __init__(self, map_amount: int):
        map = Map(0, MessageType.SPAWN_NAMES.value.get_message(), randint(15, 30), randint(30, 100), False, False, True)
        map.generate_map()
        self.maps = [map]
        self.amount = map_amount
        self.mob_count = 0

    def to_dict(self):
        return {"maps": [i.to_dict() for i in self.maps]}

    def load_maps(self, map_data):
        self.maps.clear()
        self.amount = 0
        self.mob_count = 0
        for d in map_data["maps"]:
            temp_map = Map(d["id"], d["name"], d["size_y"], d["size_x"], d["is_mob_spawn"], d["is_village"],
                           d["is_spawn"])
            for y, _ in enumerate(d["grid"]):
                for x, __ in enumerate(_):
                    if isinstance(__, dict):
                        loc = Location(temp_map, [y, x])
                        if "break" in __:
                            # We assume its a wall lol
                            temp_border = Border(loc, __["break"])
                            temp_border.break_status = __["status"]
                            temp_map.grid[y][x] = temp_border
                        elif "bounty" in __:
                            match __["name"]:
                                case "Zombi":
                                    temp_map.grid[y][x] = Zombie(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])
                                case "Goblin":
                                    temp_map.grid[y][x] = Goblin(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])
                                case "Sárkány":
                                    temp_map.grid[y][x] = Dragon(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])
                                case "Szellem":
                                    temp_map.grid[y][x] = Ghost(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])
                                case "Medúza":
                                    temp_map.grid[y][x] = Gorgon(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])
                                case "Aranybogár":
                                    temp_map.grid[y][x] = Goldenbug(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])
                                case "Óriás":
                                    temp_map.grid[y][x] = Giant(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])
                                case "Farkas":
                                    temp_map.grid[y][x] = Wolf(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])
                                case "Kígyó":
                                    temp_map.grid[y][x] = Snake(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])
                                case "Fekete Mágus":
                                    temp_map.grid[y][x] = Witch(loc, __["health"], __["base_dmg"], __["crit_chance"], __["dodge_chance"], __["hit_chance"])

                        elif "curr_location" in __:
                            continue
                        else:
                            # NPC
                            match get_type_by_name(__["name"]):
                                case "Blacksmith":
                                    temp_villager = Blacksmith(loc)
                                    temp_villager.name = __["name"]
                                    loc.set(temp_villager)
                                case "Armorer":
                                    temp_villager = Armorer(loc)
                                    temp_villager.name = __["name"]
                                    loc.set(temp_villager)
                                case "Hunter":
                                    temp_villager = Hunter(loc)
                                    temp_villager.name = __["name"]
                                    loc.set(temp_villager)
                                case "Wizard":
                                    temp_villager = Wizard(loc)
                                    temp_villager.name = __["name"]
                                    loc.set(temp_villager)
                                case "Farmer":
                                    temp_villager = Farmer(loc)
                                    temp_villager.name = __["name"]
                                    loc.set(temp_villager)
                    elif isinstance(__, int):
                        temp_map.grid[y][x] = __
            self.maps.append(temp_map)
        for d in map_data["maps"]:
            temp_map = self.maps[d["id"]]
            for out_portals in d["out_portals"]:
                temp_map.out_portals.append(Portal(
                    Location(temp_map, out_portals["curr_location"]["pos"]),
                    Location(self.maps[out_portals["next_loc"]["map"]], out_portals["next_loc"]["pos"])
                ))
            for in_portals in d["in_portals"]:
                temp_map.in_portals.append(Portal(
                    Location(self.maps[in_portals["curr_location"]["map"]], in_portals["curr_location"]["pos"]),
                    Location(temp_map, in_portals["next_loc"]["pos"])
                ))

    def get_mobs(self):
        ret = 0
        for x in self.maps:
            ret += x.get_mobs()
        self.mob_count = ret
        return self.mob_count

    def generate_maps(self):
        for x in range(1, self.amount + 1):
            is_village = x % 3 == 0
            is_dungeon = False
            if not is_village:
                is_dungeon = True
                size_y = randint(15, 30)
                size_x = randint(30, 100)
            else:
                size_y = randint(15, 30)
                size_x = randint(25, 52)

            name = MessageType.VILLAGE_NAMES.value.get_message() if is_village else MessageType.DUNGEON_NAMES.value.get_message()
            # print(f"Generated map: village:{is_village}, dungeon: {is_dungeon}, name: {name}")
            map = Map(x, name, size_y, size_x, is_dungeon, is_village)
            map.generate_map()

            self.maps.append(map)
        self.place_portals()
        self.get_mobs()

    def place_portals(self):
        placed_portals = 0
        for map in self.maps:
            for i in range(randrange(1, 3)):
                tp_worlds = [m for m in self.maps.copy() if not m == map and not m.is_spawn]
                next_map = choice(tp_worlds)

                current_loc = Location(map, map.find_clear(is_random=True))
                next_loc = Location(next_map, next_map.find_clear(is_random=True))

                portal = Portal(current_loc, next_loc, placed_portals)

                map.out_portals.append(portal)
                next_map.in_portals.append(portal)
                placed_portals += 1
