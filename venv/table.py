import os


def fill_line(line: str, length: int) -> str:
    return_text = line + ((length - len(line)) * " ")
    return return_text


def fill_line_center(line: str, length: str) -> str:
    return line.center(length, " ")


def get_border(line: str, border_left: str = None, border_right: str = None) -> str:
    if border_left and border_right:
        return f"{border_left} {line} {border_right}"
    elif border_left:
        return f"{border_left} {line}"
    elif border_right:
        return f" {line} {border_right}"
    else:
        return line


def get_bar(char: str, length: int, left: str, right: str):
    if left and right:
        return f"+{(length - 2) * char}+"
    elif left:
        return f"+{(length - 1) * char}"
    elif right:
        return f"{(length - 1) * char}+"
    else:
        return ""


class Row:
    def __init__(self, line: str, selectable: bool, is_selected: bool = False, center: bool = False) -> None:
        self.line = line
        self.selectable = selectable
        self.center = center
        self.is_selected = is_selected
        if self.is_selected:
            self.selectable = True

    def select(self):
        if self.selectable:
            self.is_selected = True

    def unselect(self):
        self.is_selected = False

    def get_pure_text(self, player) -> str:
        if self.is_selected:
            if player is None:
                return f"▶ {self.line}"
            return player.replace_placeholders(f"▶ {self.line}")
        if player is None:
            return self.line
        return player.replace_placeholders(self.line)

    def get_filled_line(self, player, length) -> str:
        pure_text = self.get_pure_text(player)
        if self.center:
            return fill_line_center(pure_text, length)
        return fill_line(pure_text, length)

    def get_bordered_line(self, player, length, border_left: str, border_right: str) -> str:
        return get_border(self.get_filled_line(player, length), border_left, border_right)


class Column:
    def __init__(self, rows: list[Row], width=-1):
        self.rows = rows
        self.width = width


    def get_selected_row(self) -> Row:
        for r in self.rows:
            if r.is_selected:
                return r

    def refresh_length(self, player):
        for r in self.rows:
            if self.width < len(r.get_pure_text(player)):
                self.width = len(r.get_pure_text(player))

    def get_column(self, player, border_left: str, border_right: str, bars: dict[int, str], height=-1) -> list[str]:
        formatted_column = []
        self.refresh_length(player)

        temp_rows = self.rows.copy()
        if height > len(temp_rows):
            for i in range(height - len(temp_rows)):
                temp_rows.append(Row("", False))

        for i, r in enumerate(temp_rows):
            line = r.get_bordered_line(player, self.width, border_left, border_right)
            if i in bars:
                formatted_column.append(get_bar(bars[i], len(line), border_left, border_right))

            formatted_column.append(line)

            if i == len(temp_rows) - 1:
                formatted_column.append(get_bar("-", len(line), border_left, border_right))

        return formatted_column


class Table:
    def __init__(self, player, columns: list[Column], bars: dict[int, str] = {}):
        self.columns = columns
        self.player = player
        self.bars = bars
        self.bars[0] = "-"
        self.height = -1
        for c in columns:
            if self.height < len(c.rows):
                self.height = len(c.rows)


    def add_column(self, column: Column):
        self.columns.append(column)
        for c in self.columns:
            if self.height < len(c.rows):
                self.height = len(c.rows)


    def get_default_row(self) -> tuple[int, Row] | None:
        for i, c in enumerate(self.columns):
            for r in c.rows:
                if r.is_selected:
                    return (i, r)


    def get_table(self) -> list[str]:
        return_columns: dict[int, str] = {}
        for i, c in enumerate(self.columns):
            border_left = "|"
            border_right = "|"
            if not i == 0:
                border_left = None

            for i2, line in enumerate(c.get_column(self.player, border_left, border_right, self.bars, self.height)):
                if not i2 in return_columns:
                    return_columns[i2] = line
                    continue
                return_columns[i2] += line
        return '\n'.join(return_columns.values())


    def next_down(self, column_index) -> Row:
        for i, r in enumerate(self.columns[column_index].rows):
            if r.is_selected:
                for i_ in range(i + 1, len(self.columns[column_index].rows)):
                    row = self.columns[column_index].rows[i_]
                    if row.selectable:
                        row.select()
                        r.unselect()
                        return row
                return r


    def next_up(self, column_index) -> Row:
        for i, r in enumerate(self.columns[column_index].rows):
            if r.is_selected:
                for i_ in reversed(range(0, i)):
                    row = self.columns[column_index].rows[i_]
                    if row.selectable:
                        row.select()
                        r.unselect()
                        return row
                return r
            


# rows1 = [
#     Row("Eszköztár", False, False, True),
#     Row("Kard", True, True, False),
#     Row("AK-47", True, False, False),
#     Row("World Destroyer", True, False, False),
# ]
# rows2 = [
#     Row("Ellenfél", False, False, True),
#     Row("Zombie", True, False, False),
#     Row("Életerő: 200HP", True, False, False),
# ]
# rows3 = [
#     Row("Statisztikáid", False, False, True),
#     Row("Életerő: 200HP", True, False, False),
#     Row("Fogyatékosság: 100", True, False, False),
# ]
# if __name__ == "__main__":
#     columns = [Column(rows1), Column(rows2), Column(rows3)]
#     table = Table(columns, {0: "-", 1: "-"})
#
#     column_index = 0
#     while True:
#         os.system("cls")
#         print(table.get_table())
#         action = input("Parancs >")
#         column = table.columns[column_index]
#         match action:
#             case "le":
#                 for i, row in enumerate(column.rows):
#                     if row.is_selected:
#                         row.unselect()
#
#                         for _i, _row in enumerate(column.rows):
#                             if _i > i:
#                                 if _row.selectable:
#                                     _row.select()
#                                     break
#                         else:
#                             for _i, _row in enumerate(column.rows):
#                                 if _i <= i:
#                                     if _row.selectable:
#                                         _row.select()
#                                         break
#                         break
#             case "fel":
#                 for i, row in enumerate(column.rows):
#                     if row.is_selected:
#                         row.unselect()
#
#                         for _i, _row in reversed(list(enumerate(column.rows))):
#                             if _i < i:
#                                 if _row.selectable:
#                                     _row.select()
#                                     break
#                         else:
#                             for _i, _row in reversed(list(enumerate(column.rows))):
#                                 if _i >= i:
#                                     if _row.selectable:
#                                         _row.select()
#                                         break
#                         break
#             case "bal":
#                 next_column_index = max(column_index - 1, 0)
#
#                 next_column_is_selectable = False
#                 for r in table.columns[next_column_index].rows:
#                     if r.selectable and next_column_index != column_index:
#                         next_column_is_selectable = True
#
#                 if next_column_is_selectable:
#                     column_index = next_column_index
#                     for r in column.rows:
#                         r.unselect()
#
#                     column = table.columns[column_index]
#                     for r in column.rows:
#                         if r.selectable:
#                             r.select()
#                             break
#             case "jobb":
#                 next_column_index = min(column_index + 1, len(table.columns) - 1)
#                 next_column_is_selectable = False
#                 for r in table.columns[next_column_index].rows:
#                     if r.selectable:
#                         next_column_is_selectable = True
#
#                 if next_column_is_selectable and next_column_index != column_index:
#                     column_index = next_column_index
#                     for r in column.rows:
#                         r.unselect()
#
#                     column = table.columns[column_index]
#                     for r in column.rows:
#                         if r.selectable:
#                             r.select()
#                             break
