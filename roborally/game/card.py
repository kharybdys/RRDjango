from roborally.models import CardDefinition

TYPE_U_TURN = 'U_TURN'
TYPE_ROTATE_LEFT = 'ROTATE_LEFT'
TYPE_ROTATE_RIGHT = 'ROTATE_RIGHT'
TYPE_BACKUP = 'BACKUP'
TYPE_MOVE1 = 'MOVE1'
TYPE_MOVE2 = 'MOVE2'
TYPE_MOVE3 = 'MOVE3'

FIELD_CARD_TYPE = 'CARD_TYPE'
FIELD_PRIORITY = 'PRIORITY'

cards = {CardDefinition.MC_10: {FIELD_PRIORITY: 10, FIELD_CARD_TYPE: TYPE_U_TURN},
         CardDefinition.MC_20: {FIELD_PRIORITY: 20, FIELD_CARD_TYPE: TYPE_U_TURN},
         CardDefinition.MC_30: {FIELD_PRIORITY: 30, FIELD_CARD_TYPE: TYPE_U_TURN},
         CardDefinition.MC_40: {FIELD_PRIORITY: 40, FIELD_CARD_TYPE: TYPE_U_TURN},
         CardDefinition.MC_50: {FIELD_PRIORITY: 50, FIELD_CARD_TYPE: TYPE_U_TURN},
         CardDefinition.MC_60: {FIELD_PRIORITY: 60, FIELD_CARD_TYPE: TYPE_U_TURN},
         CardDefinition.MC_70: {FIELD_PRIORITY: 70, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_80: {FIELD_PRIORITY: 80, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_90: {FIELD_PRIORITY: 90, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_100: {FIELD_PRIORITY: 100, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_110: {FIELD_PRIORITY: 110, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_120: {FIELD_PRIORITY: 120, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_130: {FIELD_PRIORITY: 130, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_140: {FIELD_PRIORITY: 140, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_150: {FIELD_PRIORITY: 150, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_160: {FIELD_PRIORITY: 160, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_170: {FIELD_PRIORITY: 170, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_180: {FIELD_PRIORITY: 180, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_190: {FIELD_PRIORITY: 190, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_200: {FIELD_PRIORITY: 200, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_210: {FIELD_PRIORITY: 210, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_220: {FIELD_PRIORITY: 220, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_230: {FIELD_PRIORITY: 230, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_240: {FIELD_PRIORITY: 240, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_250: {FIELD_PRIORITY: 250, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_260: {FIELD_PRIORITY: 260, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_270: {FIELD_PRIORITY: 270, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_280: {FIELD_PRIORITY: 280, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_290: {FIELD_PRIORITY: 290, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_300: {FIELD_PRIORITY: 300, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_310: {FIELD_PRIORITY: 310, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_320: {FIELD_PRIORITY: 320, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_330: {FIELD_PRIORITY: 330, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_340: {FIELD_PRIORITY: 340, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_350: {FIELD_PRIORITY: 350, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_360: {FIELD_PRIORITY: 360, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_370: {FIELD_PRIORITY: 370, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_380: {FIELD_PRIORITY: 380, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_390: {FIELD_PRIORITY: 390, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_400: {FIELD_PRIORITY: 400, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_410: {FIELD_PRIORITY: 410, FIELD_CARD_TYPE: TYPE_ROTATE_LEFT},
         CardDefinition.MC_420: {FIELD_PRIORITY: 420, FIELD_CARD_TYPE: TYPE_ROTATE_RIGHT},
         CardDefinition.MC_430: {FIELD_PRIORITY: 430, FIELD_CARD_TYPE: TYPE_BACKUP},
         CardDefinition.MC_440: {FIELD_PRIORITY: 440, FIELD_CARD_TYPE: TYPE_BACKUP},
         CardDefinition.MC_450: {FIELD_PRIORITY: 450, FIELD_CARD_TYPE: TYPE_BACKUP},
         CardDefinition.MC_460: {FIELD_PRIORITY: 460, FIELD_CARD_TYPE: TYPE_BACKUP},
         CardDefinition.MC_470: {FIELD_PRIORITY: 470, FIELD_CARD_TYPE: TYPE_BACKUP},
         CardDefinition.MC_480: {FIELD_PRIORITY: 480, FIELD_CARD_TYPE: TYPE_BACKUP},
         CardDefinition.MC_490: {FIELD_PRIORITY: 490, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_500: {FIELD_PRIORITY: 500, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_510: {FIELD_PRIORITY: 510, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_520: {FIELD_PRIORITY: 520, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_530: {FIELD_PRIORITY: 530, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_540: {FIELD_PRIORITY: 540, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_550: {FIELD_PRIORITY: 550, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_560: {FIELD_PRIORITY: 560, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_570: {FIELD_PRIORITY: 570, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_580: {FIELD_PRIORITY: 580, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_590: {FIELD_PRIORITY: 590, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_600: {FIELD_PRIORITY: 600, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_610: {FIELD_PRIORITY: 610, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_620: {FIELD_PRIORITY: 620, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_630: {FIELD_PRIORITY: 630, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_640: {FIELD_PRIORITY: 640, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_650: {FIELD_PRIORITY: 650, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_660: {FIELD_PRIORITY: 660, FIELD_CARD_TYPE: TYPE_MOVE1},
         CardDefinition.MC_670: {FIELD_PRIORITY: 670, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_680: {FIELD_PRIORITY: 680, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_690: {FIELD_PRIORITY: 690, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_700: {FIELD_PRIORITY: 700, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_710: {FIELD_PRIORITY: 710, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_720: {FIELD_PRIORITY: 720, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_730: {FIELD_PRIORITY: 730, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_740: {FIELD_PRIORITY: 740, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_750: {FIELD_PRIORITY: 750, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_760: {FIELD_PRIORITY: 760, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_770: {FIELD_PRIORITY: 770, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_780: {FIELD_PRIORITY: 780, FIELD_CARD_TYPE: TYPE_MOVE2},
         CardDefinition.MC_790: {FIELD_PRIORITY: 790, FIELD_CARD_TYPE: TYPE_MOVE3},
         CardDefinition.MC_800: {FIELD_PRIORITY: 800, FIELD_CARD_TYPE: TYPE_MOVE3},
         CardDefinition.MC_810: {FIELD_PRIORITY: 810, FIELD_CARD_TYPE: TYPE_MOVE3},
         CardDefinition.MC_820: {FIELD_PRIORITY: 820, FIELD_CARD_TYPE: TYPE_MOVE3},
         CardDefinition.MC_830: {FIELD_PRIORITY: 830, FIELD_CARD_TYPE: TYPE_MOVE3},
         CardDefinition.MC_840: {FIELD_PRIORITY: 840, FIELD_CARD_TYPE: TYPE_MOVE3}
         }


def card_type(card_definition):
    return cards[card_definition][FIELD_CARD_TYPE]


def priority(card_definition):
    return cards[card_definition][FIELD_PRIORITY]
