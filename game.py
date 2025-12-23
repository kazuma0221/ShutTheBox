from boardgame.proc import Proc
from boardgame.game import Game as BaseGame

from table import Table
from procstart import ProcStart
from procshut import ProcShut
from procroll import ProcRoll
from procend import ProcEnd

class Game(BaseGame):
    '''シャット・ザ・ボックスのゲーム手順。'''
    def __init__(self):
        '''ゲーム卓を作成し、プロシージャ定義を行う。'''
        self.table = Table()
        self.defineProc()

    def defineProc(self):
        '''プロシージャ定義。'''
        self.procdic: dict[str, Proc] = {
            'startgame' : ProcStart(),
            'roll' : ProcRoll(),
            'shut' : ProcShut(),
            'endgame' : ProcEnd()
        }

    def setProc(self):
        '''ゲームの流れ。終了条件を満たすまでプレイを行う。ユーザ入力があればタイルを閉じ、そうでなければダイスを振る。'''
        if self.isGameEnd():
            self.proc = self.procdic['endgame']
        elif self.table.inputData['choice'] is not None:
            self.proc = self.procdic['shut']
        else:
            self.proc = self.procdic['roll']

    def isGameEnd(self)->bool:
        '''ゲームの終了判定。すべてのタイルが閉じるか選択肢がなくなったらTrue、それ以外はFalseを返す。'''
        # タイルがすべて閉じる
        if len([tile for tile in self.table.tiles if tile.isOpen]) < 1:
            return True
        # 選択肢なしフラグ
        if self.table.event['GAME_END']:
            return True
        return False

# CUIでプレイ
if __name__ == '__main__':
    from boardgame.eventtype import EventType as ev

    # ゲーム開始
    game = Game()
    event = game.start()
    print('---------- GAME START ----------')

    # 入力データの初期化
    game.table.inputData = {'choice': (0, 0)}
    inputData = game.table.inputData

    # ゲーム終了までプレイ
    while event['EVENT_TYPE'] != ev.GAME_RESULT:
        # 入力待ちでなければ、次のゲーム処理を実行する
        event = game.next()
        if event['EVENT_TYPE'] != ev.USER_TURN:
            continue

        # タイルとダイスの表示
        print(event['TILES'])
        print(f'DICE: {event["DICE"]} -> {event["DICE_SUM"]}')

        # 選択肢を表示し、選んでもらう
        marks = [letter for letter, _ in zip('ABCDEF', event['CHOICES'])]
        for i, choice in enumerate(event['CHOICES']):
            choice_str = f'{choice[0]}, {choice[1]}' if choice[1] > 0 else f'{choice[0]}'
            print(f'{marks[i]}: {choice_str}')

        # 入力チェック
        while not event['GAME_END']:
            user_selection = input('Choose the tile(s)> ').upper()
            if user_selection not in marks:
                print('The mark isn\'t correct.')
            else:
                inputData['choice'] = event['CHOICES'][marks.index(user_selection)]
                break

    # 終了
    print(event['TILES'])
    print(f'DICE: {event["DICE"]} -> {event["DICE_SUM"]}')
    print(f'SCORE: {event["SCORE"]}')
    print('---------- GAME END ----------')