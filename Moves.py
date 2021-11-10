#usr/bin/env python3
import json

__version__ = 3.1
__author__ = "FLAK-ZOSO"


class Moves(object):

    def __init__(self) -> None:
        self.list = [
            None, None, None, None, None,
            None, None, None, None, False
        ]
        self.counter = 0
        self.list2 = []

    def add(self, value: chr) -> None:
        self.list[self.counter] = value
        self.list2.append(value)
        self.counter += 1

    def equalTo(self, moves: list) -> bool:
        for idx, val in enumerate(self.list2):
            if (val != moves[idx]):
                return False
        return True
    
    def equalsList(self, path="D:\\Python\Python\Variables") -> list:
        self.equals = []
        with open(rf"{path}\Matches.json", 'r') as file:
            for game in json.load(file).values():
                if (self.equalTo(game)):
                    self.equals.append(game)
        return self.equals
    
    def winningEqualsList(self, path="D:\\Python\Python\Variables") -> list:
        self.winning_equals = []
        with open(rf"{path}\Matches.json", 'r') as file:
            for game in json.load(file).values():
                if (self.equalTo(game) and game[-1]):
                    self.winning_equals.append(game)
        return self.winning_equals
    
    def identicalsList(self, path="D:\\Python\Python\Variables") -> list:
        self.identicals = []
        with open(rf"{path}\Matches.json", 'r') as file:
            for game in json.load(file).values():
                if (self.list == game):
                    self.identicals.append(game)
        return self.identicals

    def hasEquals(self, path="D:\\Python\Python\Variables") -> bool:
        if (self.equalsList(path=path)):
            return True
        return False

    def hasWinningEquals(self, path="D:\\Python\Python\Variables") -> bool:
        if (self.winningEqualsList(path=path)):
            return True
        return False
    
    def hasIdenticals(self, path="D:\\Python\Python\Variables") -> bool:
        if (self.identicalsList()):
            return True
        return False

    def save(self, path="D:\\Python\Python\Variables") -> bool:
        with open(rf"{path}\IDs.json", 'r') as file:
            id_ = int(file.read())+1
        with open(rf"{path}\IDs.json", 'w') as file:
            file.write(str(id_))
        with open(rf"{path}\Matches.json", 'r') as file:
            dictionary = json.load(file)
        with open(rf"{path}\Matches.json", 'w') as file:
            dictionary[id_] = self.list
            json.dump(dictionary, file, indent=4)
