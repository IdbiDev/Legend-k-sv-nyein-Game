class Portal:
    """
    current_location, next_location, id=0
    """
    def __init__(self, current_location, next_location, id=0):
        self.current_location = current_location
        self.next_location = next_location
        self.current_location.map.set(self.current_location.position, self)
        self.next_location.map.set(self.next_location.position, self)
        self.id = id


    """
    Ha ebbe megy bele, akkor a next_locationre kell tpzni
    """
    def is_current(self, position: list[int]) -> bool:
        return position[0] == self.current_location.position[0] and position[1] == self.current_location.position[1]


    """
    Ha ebbe megy bele, akkor a current_locationre kell tpzni
    """
    def is_next(self, position: list[int]) -> bool:
        return position[0] == self.next_location.position[0] and position[1] == self.next_location.position[1]