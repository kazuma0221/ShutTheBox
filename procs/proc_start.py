from boardgame.proc_game_start import ProcGameStart as BaseProc
from boardgame.event_type import EventType as ev
from dto import OutputEvent
from table import Table

class ProcStart(BaseProc):
    '''ゲーム開始処理。タイルのリストを出力用に渡す。'''
    def createEvent(self, table:Table) -> OutputEvent:
        return OutputEvent(event_type=ev.START_GAME, tiles=table.get_tiles_str())

# テスト
if __name__ == '__main__':
    table = Table()
    event = ProcStart().do(table)
    for elem in event.items():
        print(elem)