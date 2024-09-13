class Item:
    def __init__(self, name: str, amount: int = 1):
        self.name = name
        self.amount = amount

    def to_dict(self):
        return {"name": self.name, "amount": self.amount}
