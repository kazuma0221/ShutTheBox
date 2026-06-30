from boardgame.proc import Proc
from boardgame.eventtype import EventType as ev
from table import Table

class ProcRoll(Proc):
    '''プレイ処理。次のダイスを振り、可能な選択肢を列挙する。'''
    def do(self, table:Table)->dict:
        '''残りタイルの値の合計に応じて1個か2個のダイスを振り、選択肢を作って返す。'''
        # ダイスを2個振る
        for die in table.dice:
            die.roll()
        dice = [die for die in table.dice]

        # 残りタイルの値の合計が6以下の場合、ダイスの1個目だけを採用する
        tile_total = sum([tile.value for tile in table.tiles])
        if tile_total < 7:
            dice.pop(-1)
        table.event['DICE'] = [die.value for die in dice]

        # 合計値
        dice_sum = sum([die.value for die in table.dice])
        table.event['DICE_SUM'] = dice_sum

        # 選択肢を列挙し、使えるものだけを採用
        choices: list[tuple] = [(i, dice_sum - i) for i in range(1, (dice_sum // 2 + 1))]
        available = []
        # 自然数2つ
        # 同値とタイル上限超えははねる
        for choice in choices:
            if choice[0] == choice[1]:
                continue
            if choice[1] > Table.UPPER_LIMIT:
                continue
            if table.tiles[choice[0] - 1].isOpen and table.tiles[choice[1] - 1].isOpen:
                available.append(choice)
        # 自然数1つ（出目そのもの）
        if dice_sum <= Table.UPPER_LIMIT and table.tiles[dice_sum - 1].isOpen:
            available.append((dice_sum, 0))
        table.event['CHOICES'] = available

        # 選択肢があれば手番、なければ終了
        if len(available) > 0:
            table.event['EVENT_TYPE'] = ev.USER_TURN
        else:
            table.event['GAME_END'] = True
            table.event['EVENT_TYPE'] = ev.AUTO_MOVE
        return table.event

# テスト
if __name__ == '__main__':
    import numpy as np

    # 卓を作る
    table = Table()
    rng = np.random.default_rng()
    for tile in table.tiles:
        #tile.isOpen = rng.choice([True, False])
        pass
    print([str(tile) for tile in table.tiles])

    # 手番を実行し、値を出力する
    event = ProcRoll().do(table)
    for elem in event.items():
        print(elem)