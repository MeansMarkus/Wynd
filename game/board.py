
class Board:
    def __init__(self, size=8, empty_symbol="."):
        self.size = size
        self.empty_symbol = empty_symbol
        self.grid = [[self.empty_symbol for _ in range(size)] for _ in range(size)]

    def render(self):
        lines = []
        header = "  " + " ".join(chr(ord("a") + i) for i in range(self.size))
        lines.append(header)

        for row_index, row in enumerate(self.grid):
            rank = self.size - row_index
            lines.append(f"{rank:2} " + " ".join(row))

        return "\n".join(lines)

    def place_piece(self, file_char, rank, symbol):
        col = ord(file_char.lower()) - ord("a")
        row = self.size - int(rank)
        if 0 <= row < self.size and 0 <= col < self.size:
            self.grid[row][col] = symbol
        else:
            raise ValueError(f"Position out of bounds: {file_char}{rank}")
    


