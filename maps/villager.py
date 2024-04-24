import random, keyboard, time, sys,platform, os
import items.inventory as inventory
from table import Table, Column, Row
from messages import MessageType
from dialog import Dialog

def move_cursor_to_top_left():
    sys.stdout.write("\033[H")  # Move cursor to top-left corner
    sys.stdout.flush()


def clear():
    if platform.system() == "Windows":
        os.system("cls")
        move_cursor_to_top_left()
    else:
        os.system("clear")

class Villager:
    def __init__(self, name: str, location):
        self.name = name
        self.location = location
        self.keyboard_cooldown = time.time_ns() + 550000000


class Blacksmith(Villager):
    def __init__(self, location):  # offers: dict[Item, int]
        name = MessageType.BLACKSMITH_NAMES.value.get_message()
        super().__init__(name, location)
        self.offers = inventory.blacksmith_items
        self.current_offers = {}

    def interact(self, player):
        self.keyboard_cooldown = time.time_ns() + 550000000
        self.refresh_offer(player)
        table = self.get_table(None)

        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
        balance_columns = [Column(balance_rows, 20)]
        balance_table = Table(player, balance_columns)

        selected_row = table.columns[0].get_selected_row()
        header = MessageType.SHOP_HEADERS.value.get_replaced_message(player=player.name, npc=self.name)
        print(header)
        print(balance_table.get_table())
        print(table.get_table())
        while True:
            if self.keyboard_cooldown <= time.time_ns():
                match keyboard.read_key(suppress=True):
                    case "up":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_up(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "down":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_down(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "enter":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])
                        # Todo: Dialogs
                        if player.balance - self.current_offers[selected_item] < 0:
                            Dialog(MessageType.SHOP_NOT_ENOUGH_MONEY.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()
                        else:
                            player.inventory.add_item(selected_item)
                            player.balance -= self.current_offers[selected_item]
                            Dialog(MessageType.SHOP_BOUGHT.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()

                            time.sleep(2)
                            clear()
                            break
                        move_cursor_to_top_left()

                        print(header)

                        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
                        balance_columns = [Column(balance_rows, 20)]
                        balance_table = Table(player, balance_columns)

                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "esc":
                        clear()
                        break

    def get_table(self, selected_item) -> Table:
        header = Row("Ajánlatok", False, False, True)
        offer_rows = [header]

        is_selected = True
        for k, v in self.current_offers.items():
            if selected_item:
                offer_rows.append(Row(f"{k.name} -- {v} Ft", True, selected_item == k))
                continue

            offer_rows.append(Row(f"{k.name} -- {v} Ft", True, is_selected))
            is_selected = False

        offer_column = Column(offer_rows, 35)
        if selected_item is None:
            selected_item = inventory.name_to_item(offer_column.get_selected_row().line.split(" --")[0])

        stats_rows = [
            Row("Tárgy információk", False, False, True),
            Row(f"•  Életerő: {int(selected_item.health)}❤", False, False, False) if not int(
                selected_item.health) == 0 else None,
            Row(f"•  Sebzés: ❁ {int(selected_item.base_damage)}", False, False, False) if not int(
                selected_item.base_damage) == 0 else None,
            Row(" ", False, False, False) if not int(selected_item.health) == 0 or not int(
                selected_item.base_damage) == 0 else None,
            Row(f"🗡  Találat: {int(selected_item.hit_chance * 100)}%", False, False,
                False) if not selected_item.hit_chance == 0 else None,
            Row(f"☣  Krit: {int(selected_item.crit_chance * 100)}%", False, False,
                False) if not selected_item.crit_chance == 0 else None,
            Row(f"🛡  Hárítás: {int(selected_item.dodge_chance * 100)}%", False, False,
                False) if not selected_item.dodge_chance == 0 else None,
        ]

        stats_column = Column([r for r in stats_rows if r is not None], 25)
        columns = [offer_column, stats_column]
        table = Table(None, columns=columns, bars={1: "-"})
        return table

    def refresh_offer(self, player):
        new_offers_selected = []
        new_offers = {}
        offers = [o for o in list(self.offers.keys()) if not player.armor_slot == o and o not in player.inventory.items]
        for i in range(len(offers)):
            c = random.choice(offers)

            new_offers_selected.append(c)
            offers.remove(c)

        for item in new_offers_selected:
            increase_price = random.choice([True, False])
            if increase_price:
                price = self.offers[item] + self.offers[item] * (random.randint(1, 15) / 100)
            else:
                price = self.offers[item] - self.offers[item] * (random.randint(1, 15) / 100)

            new_offers[item] = int(price)
        self.current_offers = dict(sorted(new_offers.items(), key=lambda item: item[1]))


class Armorer(Villager):
    def __init__(self, location):
        name = MessageType.ARMORER_NAMES.value.get_message()
        super().__init__(name, location)
        self.offers =  inventory.armorer_items
        self.current_offers = {}

    def interact(self, player):
        self.keyboard_cooldown = time.time_ns() + 550000000
        self.refresh_offer(player)
        table = self.get_table(None)

        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
        balance_columns = [Column(balance_rows, 20)]
        balance_table = Table(player, balance_columns)

        selected_row = table.columns[0].get_selected_row()
        header = MessageType.SHOP_HEADERS.value.get_replaced_message(player=player.name, npc=self.name)
        print(header)
        print(balance_table.get_table())
        print(table.get_table())
        while True:
            if self.keyboard_cooldown <= time.time_ns():
                match keyboard.read_key(suppress=True):
                    case "up":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_up(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "down":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_down(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "enter":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])
                        # Todo: Dialogs
                        if player.balance - self.current_offers[selected_item] < 0:
                            Dialog(MessageType.SHOP_NOT_ENOUGH_MONEY.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()
                        else:
                            player.balance -= self.current_offers[selected_item]
                            Dialog(MessageType.SHOP_BOUGHT.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()
                            player.armor_slot = selected_item
                            time.sleep(2)
                            clear()
                            break
                        move_cursor_to_top_left()

                        print(header)

                        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
                        balance_columns = [Column(balance_rows, 20)]
                        balance_table = Table(player, balance_columns)

                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "esc":
                        clear()
                        break

    def get_table(self, selected_item) -> Table:
        header = Row("Ajánlatok", False, False, True)
        offer_rows = [header]

        is_selected = True
        for k, v in self.current_offers.items():
            if selected_item:
                offer_rows.append(Row(f"{k.name} -- {v} Ft", True, selected_item == k))
                continue

            offer_rows.append(Row(f"{k.name} -- {v} Ft", True, is_selected))
            is_selected = False

        offer_column = Column(offer_rows, 35)
        if selected_item is None:
            selected_item = inventory.name_to_item(offer_column.get_selected_row().line.split(" --")[0])

        stats_rows = [
            Row("Tárgy információk", False, False, True),
            Row(f"•  Életerő: {int(selected_item.health)}❤", False, False, False) if not int(
                selected_item.health) == 0 else None,
            Row(f"•  Sebzés: ❁ {int(selected_item.base_damage)}", False, False, False) if not int(
                selected_item.base_damage) == 0 else None,
            Row(" ", False, False, False) if not int(selected_item.health) == 0 or not int(
                selected_item.base_damage) == 0 else None,
            Row(f"🗡  Találat: {int(selected_item.hit_chance * 100)}%", False, False,
                False) if not selected_item.hit_chance == 0 else None,
            Row(f"☣  Krit: {int(selected_item.crit_chance * 100)}%", False, False,
                False) if not selected_item.crit_chance == 0 else None,
            Row(f"🛡  Hárítás: {int(selected_item.dodge_chance * 100)}%", False, False,
                False) if not selected_item.dodge_chance == 0 else None,
        ]

        stats_column = Column([r for r in stats_rows if r is not None], 25)
        columns = [offer_column, stats_column]
        table = Table(None, columns=columns, bars={1: "-"})
        return table

    def refresh_offer(self, player):
        new_offers_selected = []
        new_offers = {}
        offers = [o for o in list(self.offers.keys()) if not player.armor_slot == o and o not in player.inventory.items and o not in player.inventory.talismans]
        for i in range(len(offers)):
            c = random.choice(offers)

            new_offers_selected.append(c)
            offers.remove(c)

        for item in new_offers_selected:
            increase_price = random.choice([True, False])
            if increase_price:
                price = self.offers[item] + self.offers[item] * (random.randint(1, 15) / 100)
            else:
                price = self.offers[item] - self.offers[item] * (random.randint(1, 15) / 100)

            new_offers[item] = int(price)
        self.current_offers = dict(sorted(new_offers.items(), key=lambda item: item[1]))


class Farmer(Villager):
    def __init__(self, location):
        name = MessageType.FARMER_NAMES.value.get_message()
        super().__init__(name, location)
        self.offers = inventory.farmer_items
        self.current_offers = {}

    def interact(self, player):
        self.keyboard_cooldown = time.time_ns() + 550000000
        self.refresh_offer(player)
        table = self.get_table(None)

        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
        balance_columns = [Column(balance_rows, 20)]
        balance_table = Table(player, balance_columns)

        selected_row = table.columns[0].get_selected_row()
        header = MessageType.SHOP_HEADERS.value.get_replaced_message(player=player.name, npc=self.name)
        print(header)
        print(balance_table.get_table())
        print(table.get_table())
        while True:
            if self.keyboard_cooldown <= time.time_ns():
                match keyboard.read_key(suppress=True):
                    case "up":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_up(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "down":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_down(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "enter":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])
                        # Todo: Dialogs
                        if player.balance - self.current_offers[selected_item] < 0:
                            Dialog(MessageType.SHOP_NOT_ENOUGH_MONEY.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()
                        else:
                            player.inventory.add_item(selected_item)
                            player.balance -= self.current_offers[selected_item]
                            Dialog(MessageType.SHOP_BOUGHT.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()
                            time.sleep(2)
                            clear()
                            break
                        move_cursor_to_top_left()

                        print(header)

                        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
                        balance_columns = [Column(balance_rows, 20)]
                        balance_table = Table(player, balance_columns)

                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "esc":
                        clear()
                        break

    def get_table(self, selected_item) -> Table:
        header = Row("Ajánlatok", False, False, True)
        offer_rows = [header]

        is_selected = True
        for k, v in self.current_offers.items():
            if selected_item:
                offer_rows.append(Row(f"{k.name} -- {v} Ft", True, selected_item == k))
                continue

            offer_rows.append(Row(f"{k.name} -- {v} Ft", True, is_selected))
            is_selected = False

        offer_column = Column(offer_rows, 35)
        if selected_item is None:
            selected_item = inventory.name_to_item(offer_column.get_selected_row().line.split(" --")[0])

        stats_rows = [
            Row("Tárgy információk", False, False, True),
            Row(f"•  Életerő: {int(selected_item.health)}❤", False, False, False) if not int(
                selected_item.health) == 0 else None,
            Row(f"•  Sebzés: ❁ {int(selected_item.base_damage)}", False, False, False) if not int(
                selected_item.base_damage) == 0 else None,
            Row(" ", False, False, False) if not int(selected_item.health) == 0 or not int(
                selected_item.base_damage) == 0 else None,
            Row(f"🗡  Találat: {int(selected_item.hit_chance * 100)}%", False, False,
                False) if not selected_item.hit_chance == 0 else None,
            Row(f"☣  Krit: {int(selected_item.crit_chance * 100)}%", False, False,
                False) if not selected_item.crit_chance == 0 else None,
            Row(f"🛡  Hárítás: {int(selected_item.dodge_chance * 100)}%", False, False,
                False) if not selected_item.dodge_chance == 0 else None,
        ]

        stats_column = Column([r for r in stats_rows if r is not None], 25)
        columns = [offer_column, stats_column]
        table = Table(None, columns=columns, bars={1: "-"})
        return table

    def refresh_offer(self, player):
        new_offers_selected = []
        new_offers = {}
        offers = [o for o in list(self.offers.keys()) if not player.armor_slot == o and o not in player.inventory.items and o not in player.inventory.talismans]
        for i in range(len(offers)):
            c = random.choice(offers)

            new_offers_selected.append(c)
            offers.remove(c)

        for item in new_offers_selected:
            increase_price = random.choice([True, False])
            if increase_price:
                price = self.offers[item] + self.offers[item] * (random.randint(1, 15) / 100)
            else:
                price = self.offers[item] - self.offers[item] * (random.randint(1, 15) / 100)

            new_offers[item] = int(price)
        self.current_offers = dict(sorted(new_offers.items(), key=lambda item: item[1]))

class Hunter(Villager):
    def __init__(self, location):
        name = MessageType.HUNTER_NAMES.value.get_message()
        super().__init__(name, location)
        self.offers =  inventory.hunter_items
        self.current_offers = {}

    def interact(self, player):
        self.keyboard_cooldown = time.time_ns() + 550000000
        self.refresh_offer(player)
        table = self.get_table(None)

        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
        balance_columns = [Column(balance_rows, 20)]
        balance_table = Table(player, balance_columns)

        selected_row = table.columns[0].get_selected_row()
        header = MessageType.SHOP_HEADERS.value.get_replaced_message(player=player.name, npc=self.name)
        print(header)
        print(balance_table.get_table())
        print(table.get_table())
        while True:
            if self.keyboard_cooldown <= time.time_ns():
                match keyboard.read_key(suppress=True):
                    case "up":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_up(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "down":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_down(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "enter":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])
                        # Todo: Dialogs
                        if player.balance - self.current_offers[selected_item] < 0:
                            Dialog(MessageType.SHOP_NOT_ENOUGH_MONEY.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()

                        else:
                            player.inventory.add_item(selected_item)
                            player.balance -= self.current_offers[selected_item]
                            Dialog(MessageType.SHOP_BOUGHT.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()

                            time.sleep(2)
                            clear()
                            break
                        move_cursor_to_top_left()

                        print(header)

                        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
                        balance_columns = [Column(balance_rows, 20)]
                        balance_table = Table(player, balance_columns)

                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "esc":
                        clear()
                        break

    def get_table(self, selected_item) -> Table:
        header = Row("Ajánlatok", False, False, True)
        offer_rows = [header]

        is_selected = True
        for k, v in self.current_offers.items():
            if selected_item:
                offer_rows.append(Row(f"{k.name} -- {v} Ft", True, selected_item == k))
                continue

            offer_rows.append(Row(f"{k.name} -- {v} Ft", True, is_selected))
            is_selected = False

        offer_column = Column(offer_rows, 35)
        if selected_item is None:
            selected_item = inventory.name_to_item(offer_column.get_selected_row().line.split(" --")[0])

        stats_rows = [
            Row("Tárgy információk", False, False, True),
            Row(f"•  Életerő: {int(selected_item.health)}❤", False, False, False) if not int(
                selected_item.health) == 0 else None,
            Row(f"•  Sebzés: ❁ {int(selected_item.base_damage)}", False, False, False) if not int(
                selected_item.base_damage) == 0 else None,
            Row(" ", False, False, False) if not int(selected_item.health) == 0 or not int(
                selected_item.base_damage) == 0 else None,
            Row(f"🗡  Találat: {int(selected_item.hit_chance * 100)}%", False, False,
                False) if not selected_item.hit_chance == 0 else None,
            Row(f"☣  Krit: {int(selected_item.crit_chance * 100)}%", False, False,
                False) if not selected_item.crit_chance == 0 else None,
            Row(f"🛡  Hárítás: {int(selected_item.dodge_chance * 100)}%", False, False,
                False) if not selected_item.dodge_chance == 0 else None,
        ]

        stats_column = Column([r for r in stats_rows if r is not None], 25)
        columns = [offer_column, stats_column]
        table = Table(None, columns=columns, bars={1: "-"})
        return table

    def refresh_offer(self, player):
        new_offers_selected = []
        new_offers = {}
        offers = [o for o in list(self.offers.keys()) if not player.armor_slot == o and o not in player.inventory.items and o not in player.inventory.talismans]
        for i in range(len(offers)):
            c = random.choice(offers)

            new_offers_selected.append(c)
            offers.remove(c)

        for item in new_offers_selected:
            increase_price = random.choice([True, False])
            if increase_price:
                price = self.offers[item] + self.offers[item] * (random.randint(1, 15) / 100)
            else:
                price = self.offers[item] - self.offers[item] * (random.randint(1, 15) / 100)

            new_offers[item] = int(price)
        self.current_offers = dict(sorted(new_offers.items(), key=lambda item: item[1]))

class Wizard(Villager):
    def __init__(self, location):
        name = MessageType.WIZARD_NAMES.value.get_message()
        super().__init__(name, location)
        self.offers = inventory.wizard_items
        self.current_offers = {}

    def interact(self, player):
        self.keyboard_cooldown = time.time_ns() + 550000000
        self.refresh_offer(player)
        table = self.get_table(None)

        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
        balance_columns = [Column(balance_rows, 20)]
        balance_table = Table(player, balance_columns)

        selected_row = table.columns[0].get_selected_row()
        header = MessageType.SHOP_HEADERS.value.get_replaced_message(player=player.name, npc=self.name)
        print(header)
        print(balance_table.get_table())
        print(table.get_table())
        while True:
            if self.keyboard_cooldown <= time.time_ns():
                match keyboard.read_key(suppress=True):
                    case "up":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_up(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "down":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_row = table.next_down(0)
                        move_cursor_to_top_left()
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])

                        print(header)
                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "enter":
                        self.keyboard_cooldown = time.time_ns() + 250000000
                        selected_item = inventory.name_to_item(selected_row.line.split(" --")[0])
                        # Todo: Dialogs
                        if player.balance - self.current_offers[selected_item] < 0:
                            Dialog(MessageType.SHOP_NOT_ENOUGH_MONEY.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()
                        else:
                            player.inventory.talismans.append(selected_item)
                            player.balance -= self.current_offers[selected_item]
                            Dialog(MessageType.SHOP_BOUGHT.value.get_replaced_message(player=player.name, npc=self.name, item=selected_item.name)).print()
                            time.sleep(2)
                            clear()
                            break

                        move_cursor_to_top_left()

                        print(header)

                        balance_rows = [Row(f"Egyenleged: {player.balance} Ft", False, False, False)]
                        balance_columns = [Column(balance_rows, 20)]
                        balance_table = Table(player, balance_columns)

                        print(balance_table.get_table())
                        print(self.get_table(selected_item).get_table())

                    case "esc":
                        clear()
                        break

    def get_table(self, selected_item) -> Table:
        header = Row("Ajánlatok", False, False, True)
        offer_rows = [header]

        is_selected = True
        for k, v in self.current_offers.items():
            if selected_item:
                offer_rows.append(Row(f"{k.name} -- {v} Ft", True, selected_item == k))
                continue

            offer_rows.append(Row(f"{k.name} -- {v} Ft", True, is_selected))
            is_selected = False

        offer_column = Column(offer_rows, 35)
        if selected_item is None:
            selected_item = inventory.name_to_item(offer_column.get_selected_row().line.split(" --")[0])

        stats_rows = [
            Row("Tárgy információk", False, False, True),
            Row(f"•  Életerő: {int(selected_item.health)}❤", False, False, False) if not int(
                selected_item.health) == 0 else None,
            Row(f"•  Sebzés: ❁ {int(selected_item.base_damage)}", False, False, False) if not int(
                selected_item.base_damage) == 0 else None,
            Row(" ", False, False, False) if not int(selected_item.health) == 0 or not int(
                selected_item.base_damage) == 0 else None,
            Row(f"🗡  Találat: {int(selected_item.hit_chance * 100)}%", False, False,
                False) if not selected_item.hit_chance == 0 else None,
            Row(f"☣  Krit: {int(selected_item.crit_chance * 100)}%", False, False,
                False) if not selected_item.crit_chance == 0 else None,
            Row(f"🛡  Hárítás: {int(selected_item.dodge_chance * 100)}%", False, False,
                False) if not selected_item.dodge_chance == 0 else None,
        ]

        stats_column = Column([r for r in stats_rows if r is not None], 25)
        columns = [offer_column, stats_column]
        table = Table(None, columns=columns, bars={1: "-"})
        return table

    def refresh_offer(self, player):
        new_offers_selected = []
        new_offers = {}
        offers = [o for o in list(self.offers.keys()) if not player.armor_slot == o and o not in player.inventory.items and o not in player.inventory.talismans]
        for i in range(len(offers)):
            c = random.choice(offers)

            new_offers_selected.append(c)
            offers.remove(c)

        for item in new_offers_selected:
            increase_price = random.choice([True, False])
            if increase_price:
                price = self.offers[item] + self.offers[item] * (random.randint(1, 15) / 100)
            else:
                price = self.offers[item] - self.offers[item] * (random.randint(1, 15) / 100)

            new_offers[item] = int(price)
        self.current_offers = dict(sorted(new_offers.items(), key=lambda item: item[1]))