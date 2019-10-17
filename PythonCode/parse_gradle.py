import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')


class TokenType():

    def __init__(self):
        pass

    BEGIN_BIG_BRACKETS = 1
    END_BIG_BRACKETS = 2
    BEGIN_ARRAY = 4
    END_ARRAY = 8
    KEY = 16
    STRING = 32
    NUMBER = 64
    BOOLEAN = 128
    SEP_COMMA = 256
    SPACE = 512

