class Border:
    def __init__(self, location, is_breakable=False):
        self.location = location
        self.is_breakable: bool = is_breakable
        self.break_status: int = 3

    def to_dict(self):
        return {"location": self.location.position, "break": self.is_breakable, "status": self.break_status}

    def border_break(self):
        if self.is_breakable:
            self.break_status -= 1
            if self.break_status <= 0:
                self.remove()

    def remove(self):
        self.location.map.set(self.location.position, 0)
