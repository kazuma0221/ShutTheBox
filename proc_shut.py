from boardgame.proc import Proc
from boardgame.event_type import EventType as ev
from table import Table
from dto import OutputEvent

class ProcShut(Proc):
    '''選んだタイルを閉じる処理。'''
    def do(self, table:Table) -> OutputEvent:
        '''選んだタイルを閉じ、更新したタイル一覧を返す。'''
        # タイルを閉じる
        for i in table.input_data.choice:
            if i > 0:
                table.tiles[i - 1].shut()
        # ユーザ選択を完了する
        return OutputEvent(event_type=ev.USER_APPROVED, tiles=table.get_tiles_str())

# テスト
if __name__ == '__main__':
    # 卓を作る
    table = Table()
    print([str(tile) for tile in table.tiles])

    # タイルを閉じ、値を出力する
    table.inputData['choice'] = (2, 7)
    event = ProcShut().do(table)
    print(event['TILES'])