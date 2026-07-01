from dataclasses import dataclass, field
from boardgame.dto import InputData as BaseInput, OutputEvent as BaseOutput

@dataclass(frozen=True)
class InputData(BaseInput):
    '''PR層からAP層へ、ゲーム入力を引き渡すためのデータ転送オブジェクト(DTO)。'''
    choice: tuple = None

@dataclass(frozen=True)
class OutputEvent(BaseOutput):
    '''AP層からPR層へ、ゲーム状態の変更を通知するためのデータ転送オブジェクト(DTO)。'''
    game_end: bool = False
    choices: list = field(default_factory=list)
    tiles: list[str] = field(default_factory=list)
    dice: list[int] = field(default_factory=list)
    dice_sum: int = 0
    score: int = 0