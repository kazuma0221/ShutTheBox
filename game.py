from boardgame.proc import Proc
from boardgame.game import Game as BaseGame

from table import Table
from dto import InputData, OutputEvent
from procs.proc_start import ProcStart
from procs.proc_shut import ProcShut
from procs.proc_roll import ProcRoll
from procs.proc_end import ProcEnd

class Game(BaseGame):
    '''シャット・ザ・ボックスのゲーム手順。'''
    def __init__(self):
        '''ゲーム卓を作成し、プロシージャ定義を行う。'''
        self.table = Table()
        self.event: OutputEvent = None
        self.defineProc()

    def defineProc(self):
        '''プロシージャ定義。'''
        self.procdic: dict[str, Proc] = {
            'game_start' : ProcStart(),
            'roll' : ProcRoll(),
            'shut' : ProcShut(),
            'game_end' : ProcEnd()
        }

    def setProc(self):
        '''ゲームの流れ。終了条件を満たすまでプレイを行う。ユーザ入力があればタイルを閉じ、そうでなければダイスを振る。'''
        if self.isGameEnd():
            self.proc = self.procdic['game_end']
        elif self.table.input_data and self.table.input_data.choice:
            self.proc = self.procdic['shut']
        else:
            self.proc = self.procdic['roll']

    def isGameEnd(self) -> bool:
        '''ゲームの終了判定。すべてのタイルが閉じるか選択肢がなくなったらTrue、それ以外はFalseを返す。'''
        # タイルがすべて閉じる
        if len([tile for tile in self.table.tiles if tile.isOpen]) < 1:
            return True
        # 選択肢なしフラグ
        if self.event.game_end:
            return True
        return False

# CUIでプレイ
if __name__ == '__main__':
    from boardgame.event_type import EventType as ev

    # ゲーム開始
    game = Game()
    event: OutputEvent = game.start()
    print('---------- GAME START ----------')

    # 入力データの初期化
    game.table.input_data = InputData()

    # タイルとダイスを表示する関数
    def show():
        print(event.tiles)
        if len(event.dice) > 0:
            print(f'DICE: {event.dice} -> {event.dice_sum}')

    # ゲーム終了までプレイ
    while event.event_type != ev.GAME_RESULT:
        # 入力待ちでなければ、次のゲーム処理を実行する
        event = game.next()
        if event.event_type != ev.USER_TURN:
            game.table.input_data = None
            continue
        show()

        # 選択肢を表示し、選んでもらう
        marks = [letter for letter, _ in zip('ABCDEF', event.choices)]
        for i, choice in enumerate(event.choices):
            choice_str = f'{choice[0]}, {choice[1]}' if choice[1] > 0 else f'{choice[0]}'
            print(f'{marks[i]}: {choice_str}')

        # 入力チェック
        while not event.game_end:
            user_selection = input('Choose the tile(s)> ').upper()
            if user_selection not in marks:
                print('The mark isn\'t correct.')
            else:
                game.table.input_data = InputData(choice=event.choices[marks.index(user_selection)])
                break

    # 終了
    show()
    print(f'SCORE: {event.score}')
    print('---------- GAME END ----------')