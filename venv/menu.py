from table import Table, Row, Column
import time, os, keyboard, sys, platform


def move_cursor_to_top_left():
    sys.stdout.write("\033[H")  # Move cursor to top-left corner
    sys.stdout.flush()


def clear():
    if platform.system() == "Windows":
        os.system("cls")
        move_cursor_to_top_left()
    else:
        os.system("clear")


class ConfirmMenu:
    def __init__(self, message):
        self.rows = [
            Row(message, False, False, True),
            Row("Tovább", True, True, False),
            Row("Mégse", True, False, False),
        ]
        self.keyboard_cooldown = time.time_ns() + 350000000

    def show_menu(self) -> bool:
        table = Table(None, [Column(self.rows)], {0: "-", 1: "-"})
        clear()
        print(table.get_table())
        column_index = table.get_default_row()[0]
        selected_row = table.get_default_row()[1].line
        while True:
            column = table.columns[column_index]
            if self.keyboard_cooldown <= time.time_ns():
                match keyboard.read_key(suppress=True):

                    case "up":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_up(column_index).line
                        move_cursor_to_top_left()
                        print(table.get_table())

                    case "down":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_down(column_index).line
                        move_cursor_to_top_left()
                        print(table.get_table())

                    case "enter":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        match selected_row:
                            case "Tovább":
                                # Kezdjé
                                clear()
                                return True
                            case "Mégse":
                                clear()
                                return False


class MainMenu:
    def __init__(self):
        self.rows = [
            Row("Legendák Ösvényein", False, False, True),
            Row("Új Játék", True, True, False),
            Row("Folytatás", True, False, False),
            Row("Kilépés", True, False, False),
            Row("Készítette: Bozsóki Adrián, Kovács Balázs", False, False, True),
        ]
        self.keyboard_cooldown = time.time_ns() + 250000000

    def show_menu(self):
        table = Table(None, [Column(self.rows)], {0: "-", 1: "-", 4: "-"})
        clear()
        print(table.get_table())
        column_index = table.get_default_row()[0]

        selected_row = table.get_default_row()[1].line
        running_bitch = True
        while running_bitch:
            column = table.columns[column_index]
            if self.keyboard_cooldown <= time.time_ns():
                match keyboard.read_key(suppress=True):

                    case "up":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_up(column_index).line
                        move_cursor_to_top_left()
                        print(table.get_table())

                    case "down":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_down(column_index).line
                        move_cursor_to_top_left()
                        print(table.get_table())

                    case "enter":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        match selected_row:
                            case "Új Játék":
                                # Kezdjé
                                running_bitch = False
                                return "newgame"
                            case "Folytatás":
                                # Kezdjé
                                if os.path.isfile(os.path.abspath("saves.json")):
                                    running_bitch = False
                                    return "continue"
                                else:
                                    running_bitch = False
                                    return "newgame"
                            case "Kilépés":
                                exit(-1)


class ItemSelectorMenu:
    def __init__(self, inventory):
        self.table = inventory.get_inventory()
        self.keyboard_cooldown = time.time_ns() + 250000000
        self.inventory = inventory

    def show_menu(self):  # -> Item
        #column_index = self.table.get_default_row()[0]
        selected_item = self.table.columns[0].get_selected_row()
        clear()
        print(self.table.get_table())
        while True:

            # column = self.table.columns[column_index]
            if self.keyboard_cooldown <= time.time_ns():
                match keyboard.read_key(suppress=False):
                    case "up":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_item = self.table.next_up(0).line.split(" --")[0]
                        # self.player.hand_slot = self.player.inventory.get_item_by_name(selected_item)
                        clear()
                        print(self.table.get_table())
                    case "down":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_item = self.table.next_down(0).line.split(" --")[0]
                        # self.player.hand_slot = self.player.inventory.get_item_by_name(selected_item)
                        clear()
                        print(self.table.get_table())
                    case "enter":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        # time.sleep(1)
                        clear()
                        return self.inventory.get_item_by_name(selected_item)
                        #print(self.table.get_table())


                    # case "esc":
                    #     # player.is_fighting = False
                    #     keyboard_cooldown = time.time_ns() + 550000000
                    #     clear()
                    #     if not debug:
                    #         Dialog(f"{name} elfutott...").print()
                    #     player.current_fight.finished = True
                    #     break
