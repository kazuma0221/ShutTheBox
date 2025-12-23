from boardgame.procendgame import ProcEndGame as ProcEndGameBase
from boardgame.eventtype import EventType as ev
from table import Table

class ProcEnd(ProcEndGameBase):
    '''ゲーム終了処理。残ったタイルから点数を計算して返す。'''
    def do(self, table:Table)->dict:
        # 表になっているタイルを逆順に計算する
        score, digit = 0, 0
        for tile in reversed(table.tiles):
            if tile.isOpen:
                score += tile.value * (10 ** digit)
                digit += 1
        # 計算結果
        table.event['SCORE'] = score
        table.event['EVENT_TYPE'] = ev.GAME_RESULT
        return table.event

if __name__ == '__main__':
    import numpy as np

    # 卓を作り、タイルを適当に伏せる
    table = Table()
    rng = np.random.default_rng()
    for tile in table.tiles:
        tile.isOpen = rng.choice([True, False])
    print([str(tile) for tile in table.tiles])

    # プロシージャの計算結果を出力
    event = ProcEnd().do(table)
    print(event['SCORE'])