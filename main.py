import os
import sys
import time
import random
import platform
import keyboard
import items.inventory as inventory

from player import Player
from dialog import Dialog
from menu import MainMenu
from messages import MessageType
from table import Table, Column, Row

from maps.map import MapManager

from maps.villager import Blacksmith
from fight import Fight
from mob import Witch

# from os import listdir
# from os.path import isfile, join


# def getListOfFiles(dirName):
#     # create a list of file and sub directories
#     # names in the given directory
#     listOfFile = os.listdir(dirName)
#     allFiles = list()
#     # Iterate over all the entries
#     for entry in listOfFile:
#         # Create full path
#         fullPath = os.path.join(dirName, entry)
#         # If entry is a directory then get the list of files in this directory
#         if os.path.isdir(fullPath):
#             allFiles = allFiles + getListOfFiles(fullPath)
#         else:
#             allFiles.append(fullPath)
#
#     return allFiles
#
# count = 0
# for f in getListOfFiles("."):
#     if str(f).endswith(".py"):
#         with open(f, encoding="utf-8") as file:
#             count += len(file.readlines())
#
# print(count)
# exit()

os.system("chcp 65001")
def move_cursor_to_top_left():
    sys.stdout.write("\033[H")  # Move cursor to top-left corner
    sys.stdout.flush()

keyboard_cooldown = 0

is_final_boss = False
debug = False

map_manager = MapManager(random.randint(3,20))
map_manager.generate_maps()


def clear():
    if platform.system() == "Windows":
        os.system("cls")
        move_cursor_to_top_left()
    else:
        os.system("clear")


main_menu = MainMenu()
main_menu.show_menu()
start_time = time.time()
clear()
name = "Idbi"
print("""
Mozgás: W, A, S, D
Valamely falakat át tudod törni, ehhez 3x kell menj a fal irányába.
A táblázatokban a nyilakkal mozoghatsz, és az ENTER lenyomásával választhatod ki.
Az ESC megnyomásával vagy elfutsz, vagy kilépsz a játékból!
A SPACE lenyomásával a dialógusokat átugorhatod!
A pályán találhatóak portálok (Ⓟ), melyekkel könnyen utazhatsz a világok között.
A pályán találhatóak szörnyek (!). A szörnyek megölésével pénzt szerzel.
A pályán találhatóak polgárok (⌂). A polgárokkal tudsz kereskedni. Vehetsz tőlük kardot, fegyvert, szettet, talizmánt, ételt és italt.
A hátizsákodban található tárgyakat az ENTER lenyomásával tudod használni.

""")
name = input("Játékosnév: ")

clear()

player = Player(name, map_manager.maps[0])
player.armor_slot = inventory.items["Újonc Láncing"]
player.inventory.add_item(inventory.items["Acél Kard"])
clear()

starter_npc_name = MessageType.STARTER_NPC_NAMES.value.get_message()

if not debug:
    Dialog(f"Ahogy a nap sugarai keresztülhasították az őszi ködöt, te, {name}, elindultál egy sűrű erdő mélyén haladó ösvényen.",True).print()
    Dialog(f"A lombok susogása és a madarak dalolása kísérte lépteidet, miközben előtted egy kis falu köszöntött.", True).print()
    Dialog(f"A falu látszólag békés volt, de az emberek arckifejezése szorongást és aggodalmat tükrözött.").print()
    print()
    Dialog(f"- Üdvözöllek a(z) {map_manager.maps[0].name} térségben, {name}! - szól hozzád {starter_npc_name}.", True).print()
    Dialog(f"- Kérlek, légy óvatos. A falunkat egyre sűrűbben támadják a szörnyek az erdőből. Segítségedre lenne szükségünk, hogy megtisztítsuk a környéket.").print()
    print()
    Dialog(f"A polgármester melléd áll, és megfogja a válladat.", True).print()
    Dialog(f"- Kérlek {name}, te vagy az egyetlen reményünk. Segíts nekünk, és jutalmat nyersz, amelyre csak vágyhatsz.").print()
    print()
    Dialog(f"- {name}: Segítek nektek városlakók, bízzátok rám ezt a feladatot! Igérem, nem fogtok csalódni bennem!").print()
    print()
    Dialog(f"Most rajtad van a sor... Tisztítsd meg a környéket a szörnyektől! Fejlődj, szerelkezz fel, mert nem tudhatod, hogy az út végén mi vár...").print()
    time.sleep(3)
    clear()
    Dialog(f"Miután elköszöntél {starter_npc_name}-tól/-től, elkezdtél vándorolni a környéken. Egy szép területen telepedtél le először.").print()
    Dialog(f"{name}: Nagy munka vár rám holnap, jobb ha most pihenek egyet...").print()
    time.sleep(2)
    clear()
    Dialog(f"*Másnap reggel*",True).print()
    Dialog(f"{name}: Na, lássunk munkához! (Feladat: Öld meg az összes szörnyet!)").print()
    clear()

#print(f"Játékos: {name}\t{player.health}❤\t{player.balance}Ft\tArmor:{player.armor_slot.name}")
move_cursor_to_top_left()
print(player.current_map.get_map())
while True:

    if player.is_fighting:
        player_stats_data = player.get_calculated_stats()
        player_column = Column([
            Row(f"{name} %is_player_hit%", False, False, True),
            Row(f"• Életerő: %health%❤", False),
            #Row(f"• Egyenleg: {player.balance} Ft", False),
            Row(f"• Sebzés: ❁ %base_damage%", False),
            Row(" ", False),
            Row(f"🗡  Találat: %hit_chance%%", False, False, False),
            Row(f"☣  Krit: %crit_chance%%", False, False, False),
            Row(f"🛡  Hárítás: %dodge_chance%%", False, False, False),

        ], 20)
        #print(f"Játékos: {name}\t{player.health}❤\t{player.balance}Ft\tArmor:{player.armor_slot.name}")

        opponent = player.current_fight.opponent
        opponent_column = Column([
            Row(f"{opponent.name} %is_mob_hit%", False, False, True),
            Row(f"• Életerő: %mob_health%❤", False, False, False),
            Row(f"• Sebzés: ❁ {opponent.base_damage}", False, False, False),
            Row(" ", False),
            Row(f"🗡  Találat: {int(opponent.hit_chance * 100)}%", False, False, False),
            Row(f"☣  Krit: {int(opponent.crit_chance * 100)}%", False, False, False),
            Row(f"🛡  Hárítás: {int(opponent.dodge_chance * 100)}%", False, False, False),

        ], 20)
        table = player.inventory.get_inventory()
        table.bars[1] = "-"
        table.add_column(player_column)
        table.add_column(opponent_column)
        column_index = table.get_default_row()[0]
        selected_item = table.get_default_row()[1].line
        player.hand_slot = player.inventory.get_item_by_name(selected_item)
        clear()
        print(table.get_table())
        while not player.current_fight.finished:
            if player.current_fight.next_round:
                while True:
                    column = table.columns[column_index]
                    if keyboard_cooldown <= time.time_ns():
                        match keyboard.read_key(suppress = True):
                            case "up":
                                keyboard_cooldown = time.time_ns() + 250000000
                                selected_item = table.next_up(column_index).line
                                player.hand_slot = player.inventory.get_item_by_name(selected_item)
                                clear()
                                print(table.get_table())
                            case "down":
                                keyboard_cooldown = time.time_ns() + 250000000
                                selected_item = table.next_down(column_index).line
                                player.hand_slot = player.inventory.get_item_by_name(selected_item)
                                clear()
                                print(table.get_table())
                            case "enter":
                                keyboard_cooldown = time.time_ns() + 250000000
                                player.current_fight.run_next_round()
                                #time.sleep(1)
                                clear()
                                print(table.get_table())

                                break
                            case "esc":
                                if is_final_boss:
                                    continue
                                player.is_fighting = False
                                keyboard_cooldown = time.time_ns() + 550000000
                                clear()
                                if not debug:
                                    Dialog(f"{name} elfutott...").print()
                                player.current_fight.finished = True
                                break
            else:
                clear()
                print(table.get_table())
                player.current_fight.run_next_round()
                clear()
                print(table.get_table())
        player.current_fight = None
        player.is_fighting = False
        if map_manager.get_mobs() <= 0 and not is_final_boss:
            # End scene
            clear()
            Dialog(f"{starter_npc_name}: Hálásak vagyunk neked, {name}! Visszahoztad a béke és a biztonság érzését a faluba!").print()
            Dialog(f"Azonban, miközben a falusiak ünneplik a győzelmet, egy hatalmas árnyék borul a falura. Egy furcsa ember jön az úton, körülötte érezni a feszültséget.").print()

            Dialog(f"Fekete Mágus: Üdvözöllek, {name}. Gratulálok, hogy idáig eljutottál. De sajnos ez a végállomásod lesz.").print()
            Dialog(f"{name}: Te vagy az, aki elátkozta ezt a vidéket és szörnyekkel hozta meg az uralmát?").print()
            Dialog(f"Fekete Mágus: Haha, igen, én vagyok az, aki az átkot szórtam erre a tájra. Az emberek képtelenek voltak megérteni a hatalmat, amit birtokolok, és most fizetnek azokért a hibákért. De te semmi esélyed nincs ellenem, kis hős. A sötétség és a varázslat hatalma a kezemben van.").print()

            Dialog(f"{name}: Nem engedhetem, hogy pusztításba taszítsd ezt a vidéket. Meg foglak állítani!").print()
            Dialog(f"Fekete Mágus: Oh, mennyire naiv vagy. Meg akarsz küzdeni velem? Engem, aki uralom alá hajtottam minden élőlényt ezen a vidéken? Engem, aki a sötétség és a varázslat összes titkát ismeri? {name}, te csak egy kis tüzes gyertya vagy a sötét viharban.").print()

            Dialog(f"Fekete Mágus: Most már nincs tovább menekvés számodra. Gyere, próbálj meg megvédeni valamit, ami már rég elveszett!").print()
            time.sleep(5)
            player.current_fight = Fight(player, Witch(None,
                                                       random.randrange(1000,1575),
                                                       random.randrange(30,55),
                                                       random.randrange(30, 50) / 100,
                                                       random.randrange(15, 35) / 100,
                                                       random.randrange(25, 75) / 100,
                                                       ))
            player.is_fighting = True
            is_final_boss = True
        elif is_final_boss:
            # Game vége
            Dialog(f"Végül {name} legyőzte a Fekete Mágust, és most megpihen a csatát követően.").print()
            Dialog(f"{starter_npc_name}: {name}, te tényleg megmentetted a falut! Hálásak vagyunk neked!").print()
            Dialog(f"{name}: Ez az én kötelességem volt. De ne feledjétek, mindig légyetek óvatosak. A sötétség mindig újra és újra felbukkanhat, és nem mindig lesznek hősök, akik felállnak ellene.").print()
            Dialog(f"Ezután a játékos hősként ünneplik, és a falu visszanyeri békéjét, majd {name} tovább indult az útján a PÁGISZ felé...").print()

            time.sleep(5)
            clear()
            exit(f"GG Kivitted a játékot :3, eltöltött idő: {time.time()-start_time}" )
        clear()
        print(player.current_map.get_map())
    else:
        should_refresh = False
        old = player.position.copy()
        old_map = player.current_map
        if keyboard_cooldown <= time.time_ns():
            match keyboard.read_key(suppress = True):
                case "w":
                        player.move_y(False)
                        should_refresh = True
                        keyboard_cooldown = time.time_ns() + 250000000
                case "s":
                        player.move_y(True)
                        should_refresh = True
                        keyboard_cooldown = time.time_ns() + 250000000
                case "a":
                        player.move_x(False)
                        should_refresh = True
                        keyboard_cooldown = time.time_ns() + 250000000
                case "d":
                        player.move_x(True)
                        should_refresh = True
                        keyboard_cooldown = time.time_ns() + 250000000
                case "esc":
                    exit("Játék vége")
        if should_refresh:
            move_cursor_to_top_left()
            player.update_map(old,old_map)
            print(player.current_map.get_map())


