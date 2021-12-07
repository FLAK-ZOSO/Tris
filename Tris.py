#!/usr/bin/env python3
from random import choice
import json

__version__ = 'v2.3.1'
__author__ = "FLAK-ZOSO"


class Box(object):
    __slots__ = ('dict')

    def __init__(self) -> None:
        self.dict = {
            1: '1', 2: '2', 3: '3', 
            4: '4', 5: '5', 6: '6', 
            7: '7', 8: '8', 9: '9'
        }

    def check(self) -> bool:
        c = self.dict
        if (c[1] == c[2] == c[3] or c[4] == c[5] == c[6] or c[7] == c[8] == c[9]): # Orizontals
            return True
        if (c[1] == c[4] == c[7] or c[2] == c[5] == c[8] or c[3] == c[6] == c[9]): # Verticals
            return True
        if (c[1] == c[5] == c[9] or c[3] == c[5] == c[7]): # Diagonals
            return True
        return False

    def print(self) -> None:
        a = [*self.dict.values()]
        table = [
            (a[0], a[1], a[2]), 
            (a[3], a[4], a[5]), 
            (a[6], a[7], a[8])
        ]
        for line in table:
            print(*line)


class Moves(object):
    __slots__ = ('counter', 'list', 'list2', 'equals', 'winning_equals')

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

    def __equalTo(self, moves: list) -> bool:
        for idx, val in enumerate(self.list2):
            if (val != moves[idx]):
                return False
        return True
    
    def equalsList(self) -> list:
        self.equals = []
        with open(rf"Matches.json", 'r') as file:
            for game in json.load(file).values():
                if (self.__equalTo(game)):
                    self.equals.append(game)
        return self.equals
    
    def winningEqualsList(self) -> list:
        self.winning_equals = []
        with open(rf"Matches.json", 'r') as file:
            for game in json.load(file).values():
                if (self.__equalTo(game) and game[-1]):
                    self.winning_equals.append(game)
        return self.winning_equals
    
    def __identicalsList(self) -> list:
        self.identicals = []
        with open(rf"Matches.json", 'r') as file:
            for game in json.load(file).values():
                if (self.list == game):
                    self.identicals.append(game)
        return self.identicals

    def finishIf(self) -> bool:
        if (self.__isFinished()):
            print("There's no winner.")
            self.list[-1] = True # A draft is considered a computer's win
            return self.save()

    def hasEquals(self) -> bool:
        return bool(self.equalsList())

    def hasWinningEquals(self) -> bool:
        return bool(self.winningEqualsList())
    
    def hasIdenticals(self) -> bool:
        return bool(self.__identicalsList())

    def __isFinished(self) -> bool:
        return (self.counter >= 8 and len(self.list2) == 9)

    def save(self) -> bool:
        with open(rf"IDs.json", 'r') as file:
            id_ = int(file.read())+1
        with open(rf"IDs.json", 'w') as file:
            file.write(str(id_))
        with open(rf"Matches.json", 'r') as file:
            dictionary = json.load(file)
        with open(rf"Matches.json", 'w') as file:
            dictionary[str(id_)] = self.list
            file.write(encodeMatches(dictionary))
        return True


def encodeMatches(dictionary: dict) -> str:
    result = "{"
    for key, value in dictionary.items():
        result += f"""\n    {json.dumps(key)}: {json.dumps(value)},"""
    result = result[:-1]
    result += "\n}"
    return result


def game() -> bool:

    # Start
    b = Box()
    m = Moves()
    avaiableBoxes = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Game
    while (True):
        # Printing the table
        b.print()

        # User's move
        move = input("Insert the number of the case you want: ")
        if (b.dict[int(move)] == move): # The box is free
            b.dict[int(move)] = 'X'
            m.add(move)
            avaiableBoxes.remove(int(move))
            if (b.check()):
                print("The human player won.")
                m.save()
                return True
        else: # The box is already occupied
            print("Your case is already occupied. Game Over.")
            del b, m
            return False
        
        # Draft check
        if (m.finishIf()):
            return True

        # Computer's move
        if (m.hasEquals()):
            if (m.hasWinningEquals()):
                case = int(m.winningEqualsList() [-1] [m.counter])
            else:
                possibilities = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
                for game in m.equalsList():
                    try:
                        possibilities.remove(int(game[m.counter]))
                    except KeyError:
                        pass
                if (not possibilities - set(avaiableBoxes)):
                    case = choice(avaiableBoxes)
        try:
            b.dict[case] = 'O'
            m.add(str(case))
        except UnboundLocalError: # The variable case is still empty
            b.dict[case := choice(avaiableBoxes)] = 'O'
            m.add(str(case))
        avaiableBoxes.remove(case)
        del case
        if (b.check()):
            print("The computer won.")
            m.list[-1] = True # The computer won? Yes, True.
            m.save()
            return True
