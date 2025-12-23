from boardgame.procstartgame import ProcStartGame as ProcStartGameBase
from boardgame.eventtype import EventType as ev
from table import Table

class ProcStart(ProcStartGameBase):
    '''ゲーム開始処理。タイルのリストを出力用に渡す。'''
    def setEvent(self, table:Table):
        table.event['TILES'] = [str(tile) for tile in table.tiles]
        table.event['GAME_END'] = False
        table.event['EVENT_TYPE'] = ev.START_GAME

# テスト
if __name__ == '__main__':
    table = Table()
    event = ProcStart().do(table)
    for elem in event.items():
        print(elem)