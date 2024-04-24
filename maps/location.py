from maps.border import Border


class Location:
    def __init__(self, map, position: list[int]):
        self.map = map
        self.position = position

    def set(self, new_value):
        self.map.set(self.position, new_value)

    def clear(self):
        self.map.set(self.position, 0)

    def get_nearest_free(self) -> list[int]:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in directions:
            if self.map.grid[self.position[0] + d[0]][self.position[1] + d[1]] == 0:
                return [self.position[0] + d[0], self.position[1] + d[1]]

        for d in directions:
            x = self.map.grid[self.position[0] + d[0]][self.position[1] + d[1]]
            if isinstance(x, Border):
                if x.is_breakable:
                    x.remove()
                    return [self.position[0] + d[0], self.position[1] + d[1]]
