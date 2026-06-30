from boardgame.proc import Proc
from boardgame.eventtype import EventType as ev
from table import Table

class ProcShut(Proc):
    '''選んだタイルを閉じる処理。'''
    def do(self, table:Table)->dict:
        '''選んだタイルを閉じ、更新したタイル一覧を返す。'''
        # タイルを閉じる
        for i in table.inputData['choice']:
            if i > 0:
                table.tiles[i - 1].shut()
        table.event['TILES'] = [str(tile) for tile in table.tiles]
        # ユーザ選択を完了し、入力データを初期値に戻す
        table.inputData['choice'] = None
        table.event['EVENT_TYPE'] = ev.USER_APPROVED
        return table.event

# テスト
if __name__ == '__main__':
    # 卓を作る
    table = Table()
    print([str(tile) for tile in table.tiles])

    # タイルを閉じ、値を出力する
    table.inputData['choice'] = (2, 7)
    event = ProcShut().do(table)
    print(event['TILES'])