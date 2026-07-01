from bgpieces.die import Die
from boardgame.table import Table as BaseTable
from dto import InputData
from tile import Tile

class Table(BaseTable):
    '''シャット・ザ・ボックスのゲーム卓。ゲームに必要なデータを保持する。'''
    UPPER_LIMIT: int = 9

    def __init__(self):
        self.tiles: list[Tile] = [Tile(value=i) for i in range(1, Table.UPPER_LIMIT + 1)]
        super().__init__(rules=None, players=[], pieces=self.tiles, input_data=InputData())
        self.dice = [Die(), Die()]

    def get_tiles_str(self) -> list[str]:
        return [str(tile) for tile in self.tiles]

# テスト
if __name__ == '__main__':
    table = Table()
    for elem in table.__dict__.items():
        print(elem)