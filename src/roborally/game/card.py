from enum import Enum


class CardType(Enum):
    U_TURN = 'U_TURN'
    ROTATE_LEFT = 'ROTATE_LEFT'
    ROTATE_RIGHT = 'ROTATE_RIGHT'
    BACKUP = 'BACKUP'
    MOVE1 = 'MOVE1'
    MOVE2 = 'MOVE2'
    MOVE3 = 'MOVE3'

    @classmethod
    def from_priority(cls, priority: int):
        if priority % 10 != 0:
            raise ValueError(f"Unsupported priority: {priority}")
        elif 10 <= priority <= 60:
            return CardType.U_TURN
        elif 70 <= priority <= 420:
            if priority % 20 == 0:
                return CardType.ROTATE_RIGHT
            else:
                return CardType.ROTATE_LEFT
        elif 430 <= priority <= 480:
            return CardType.BACKUP
        elif 490 <= priority <= 660:
            return CardType.MOVE1
        elif 670 <= priority <= 780:
            return CardType.MOVE2
        elif 790 <= priority <= 840:
            return CardType.MOVE3
        else:
            raise ValueError(f"Unsupported priority: {priority}")

    def get_turns(self):
        match self:
            case self.U_TURN:
                return 2
            case self.ROTATE_LEFT:
                return -1
            case self.ROTATE_RIGHT:
                return 1
            case _:
                return 0

    def get_steps(self):
        match self:
            case self.MOVE1:
                return 1
            case self.MOVE2:
                return 2
            case self.MOVE3:
                return 3
            case self.BACKUP:
                return -1
            case _:
                return 0


class CardDefinition(Enum):
    MC_10 = 'MC_10'
    MC_20 = 'MC_20'
    MC_30 = 'MC_30'
    MC_40 = 'MC_40'
    MC_50 = 'MC_50'
    MC_60 = 'MC_60'
    MC_70 = 'MC_70'
    MC_80 = 'MC_80'
    MC_90 = 'MC_90'
    MC_100 = 'MC_100'
    MC_110 = 'MC_110'
    MC_120 = 'MC_120'
    MC_130 = 'MC_130'
    MC_140 = 'MC_140'
    MC_150 = 'MC_150'
    MC_160 = 'MC_160'
    MC_170 = 'MC_170'
    MC_180 = 'MC_180'
    MC_190 = 'MC_190'
    MC_200 = 'MC_200'
    MC_210 = 'MC_210'
    MC_220 = 'MC_220'
    MC_230 = 'MC_230'
    MC_240 = 'MC_240'
    MC_250 = 'MC_250'
    MC_260 = 'MC_260'
    MC_270 = 'MC_270'
    MC_280 = 'MC_280'
    MC_290 = 'MC_290'
    MC_300 = 'MC_300'
    MC_310 = 'MC_310'
    MC_320 = 'MC_320'
    MC_330 = 'MC_330'
    MC_340 = 'MC_340'
    MC_350 = 'MC_350'
    MC_360 = 'MC_360'
    MC_370 = 'MC_370'
    MC_380 = 'MC_380'
    MC_390 = 'MC_390'
    MC_400 = 'MC_400'
    MC_410 = 'MC_410'
    MC_420 = 'MC_420'
    MC_430 = 'MC_430'
    MC_440 = 'MC_440'
    MC_450 = 'MC_450'
    MC_460 = 'MC_460'
    MC_470 = 'MC_470'
    MC_480 = 'MC_480'
    MC_490 = 'MC_490'
    MC_500 = 'MC_500'
    MC_510 = 'MC_510'
    MC_520 = 'MC_520'
    MC_530 = 'MC_530'
    MC_540 = 'MC_540'
    MC_550 = 'MC_550'
    MC_560 = 'MC_560'
    MC_570 = 'MC_570'
    MC_580 = 'MC_580'
    MC_590 = 'MC_590'
    MC_600 = 'MC_600'
    MC_610 = 'MC_610'
    MC_620 = 'MC_620'
    MC_630 = 'MC_630'
    MC_640 = 'MC_640'
    MC_650 = 'MC_650'
    MC_660 = 'MC_660'
    MC_670 = 'MC_670'
    MC_680 = 'MC_680'
    MC_690 = 'MC_690'
    MC_700 = 'MC_700'
    MC_710 = 'MC_710'
    MC_720 = 'MC_720'
    MC_730 = 'MC_730'
    MC_740 = 'MC_740'
    MC_750 = 'MC_750'
    MC_760 = 'MC_760'
    MC_770 = 'MC_770'
    MC_780 = 'MC_780'
    MC_790 = 'MC_790'
    MC_800 = 'MC_800'
    MC_810 = 'MC_810'
    MC_820 = 'MC_820'
    MC_830 = 'MC_830'
    MC_840 = 'MC_840'

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]

    def get_priority(self) -> int:
        return int(self.value[3:])

    def get_type(self) -> CardType:
        return CardType.from_priority(self.get_priority())
