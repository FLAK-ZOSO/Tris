#usr/bin/env python3

__version__ = 1.0
__author__ = "FLAK-ZOSO"

class Box(object):

    def __init__(self) -> None:
        self.dict = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}

    def check(self) -> bool:
        c = self.dict
        if (c[1] == c[2] == c[3] or c[4] == c[5] == c[6] or c[7] == c[8] == c[9]): # Orizzontali
            return True
        if (c[1] == c[4] == c[7] or c[2] == c[5] == c[8] or c[3] == c[6] == c[9]):  # Verticali
            return True
        if (c[1] == c[5] == c[9] or c[3] == c[5] == c[7]): # Diagonali
            return True
        return False
