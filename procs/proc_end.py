from boardgame.proc_game_end import ProcGameEnd as BaseProc
from boardgame.event_type import EventType as ev
from dto import OutputEvent
from table import Table

class ProcEnd(BaseProc):
    '''ゲーム終了処理。残ったタイルから点数を計算して返す。'''
    def do(self, table:Table) -> OutputEvent:
        # 最終局面のサイコロ
        dice_for_output = [die.value for die in table.dice]
        dice_sum = sum(dice_for_output)
        # 点数：表になっているタイルを逆順に計算する
        score, digit = 0, 0
        for tile in reversed(table.tiles):
            if tile.isOpen:
                score += tile.value * (10 ** digit)
                digit += 1
        # 計算結果
        return OutputEvent(event_type=ev.GAME_RESULT,
                           dice=dice_for_output,
                           dice_sum=dice_sum,
                           tiles=table.get_tiles_str(),
                           score=score)

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