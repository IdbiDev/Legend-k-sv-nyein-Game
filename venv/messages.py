from enum import Enum
from message import Message


class MessageType(Enum):
    WELCOME = Message("welcome")
    MOB_DODGE = Message("mob_dodge")
    PLAYER_EAT = Message("player_eat")
    VILLAGER_OUT_OF_STOCK = Message("villager_out_of_stock")
    PLAYER_MISS = Message("player_miss")
    PLAYER_DODGE = Message("player_dodge")
    PLAYER_CRIT = Message("player_crit")
    MOB_DEAD = Message("mob_dead")
    MOB_MISS = Message("mob_miss")
    MOB_CRIT = Message("mob_crit")
    PLAYER_DEAD = Message("player_dead")
    PLAYER_HIT = Message("player_hit")
    MOB_HIT = Message("mob_hit")

    STARTER_NPC_NAMES = Message("starter_npcs")
    SPAWN_NAMES = Message("spawn_names")
    VILLAGE_NAMES = Message("village_names")
    DUNGEON_NAMES = Message("dungeon_names")

    BLACKSMITH_NAMES = Message("blacksmith_names")
    WIZARD_NAMES = Message("wizard_names")
    HUNTER_NAMES = Message("hunters_names")
    FARMER_NAMES = Message("farmer_names")
    ARMORER_NAMES = Message("armorer_names")

    SHOP_HEADERS = Message("shop_headers")
    SHOP_NOT_ENOUGH_MONEY = Message("shop_not_enough_money")
    SHOP_BOUGHT = Message("shop_bought")
