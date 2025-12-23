from bgpieces.piece import Piece

class Tile(Piece):
    '''数字タイルを表すクラス。値と表裏を持つ。表が開いた状態で、裏が閉じた状態。'''
    def __init__(self, value:int):
        super().__init__(color=None, value=value, name=f'tile_{value}')
        self.isOpen = True

    def __str__(self):
        if self.isOpen:
            return str(self.value)
        else:
            return '_'

    def open(self):
        self.isOpen = True

    def shut(self):
        self.isOpen = False