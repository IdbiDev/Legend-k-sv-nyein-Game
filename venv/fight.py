import random
from messages import MessageType
from dialog import Dialog
class Fight:
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
        self.finished = False
        self.next_round = random.random() >= 0.5 # True: Player; False: Opponent


    def run_next_round(self) -> str:
        if self.next_round:
            # Player választ
            
            attack_res = self.player.attack(self.opponent) # return {"mob_dodge": is_dodge, "player_hit": is_hit, "is_crit": is_crit, "is_dead": False}
            if attack_res["mob_dodge"]:
                MessageType.MOB_DODGE.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
                #print("MOB dodgolta. :c")
            elif not attack_res["player_hit"]:
                MessageType.PLAYER_MISS.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
            else:
                MessageType.PLAYER_HIT.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
            if attack_res["is_crit"]:
                MessageType.PLAYER_CRIT.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
            if attack_res["is_dead"]:
                MessageType.MOB_DEAD.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
                self.finished = True
                self.opponent.kys_ilydodo()
                self.player.balance += self.opponent.bounty
                self.player.current_map.set(self.player.position, 0)
                self.player.position = self.opponent.location.position
                self.player.current_map.set(self.player.position, 1)
        else:
            attack_res = self.opponent.attack(self.player) # return {"player_dodge": is_dodge, "mob_hit": is_hit, "is_crit": False, "is_dead": False}
            if attack_res["player_dodge"]:
                MessageType.PLAYER_DODGE.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
            elif not attack_res["mob_hit"]:
                MessageType.MOB_MISS.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
            else:
                MessageType.MOB_HIT.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
            if attack_res["is_crit"]:
                MessageType.MOB_CRIT.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
            if attack_res["is_dead"]:
                MessageType.PLAYER_DEAD.value.get_dialog_replaced_message(player=self.player.name, mob=self.opponent.name).print()
                self.finished = True

                Dialog(f"A falut ellepték a szörnyek, keresztül gázolva {self.player.name} holttestén.").print()
                if self.opponent.name == "Fekete Mágus":
                    Dialog(f"A világ már nem az igazi a Fekete Mágus uralma alatt.").print()
                exit("Vége a játéknak! Meghaltál!")
                # End scene
        self.next_round = random.random() >= 0.5