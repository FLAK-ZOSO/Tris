#!/usr/bin/env python3
from random import choice
import json
import sys

__version__ = '3.1.0'
__author__ = "FLAK-ZOSO"


class Box(object):

    def __init__(self) -> None:
        self.grid = {
            1: '1', 2: '2', 3: '3', 
            4: '4', 5: '5', 6: '6', 
            7: '7', 8: '8', 9: '9'
        }

    def check(self) -> bool:
        g = self.grid
        return (
            (g[1] == g[2] == g[3] or g[4] == g[5] == g[6] or g[7] == g[8] == g[9]) # Horizontals
            or (g[1] == g[4] == g[7] or g[2] == g[5] == g[8] or g[3] == g[6] == g[9]) # Verticals
            or (g[1] == g[5] == g[9] or g[3] == g[5] == g[7]) # Diagonals
        )

    def print(self) -> None:
        _ = [*self.grid.values()]
        table = [
            (_[0], _[1], _[2]), 
            (_[3], _[4], _[5]), 
            (_[6], _[7], _[8])
        ]
        for line in table:
            print(*line)


class Moves(object):

    def __init__(self) -> None:
        self.resume = [
            None, None, None, None, None,
            None, None, None, None, False
        ]
        self.cursor = 0
        self.current_game = []

    def add(self, value: chr) -> None:
        self.resume[self.cursor] = value
        self.current_game.append(value)
        self.cursor += 1

    def _equalTo(self, moves: list) -> bool:
        for current, saved in zip(self.current_game, moves):
            if (current != saved):
                return False
        return True
    
    def equalsList(self) -> list:
        self.equals = []
        with open(rf"Matches.json", 'r') as file:
            for game in json.load(file).values():
                if (self._equalTo(game)):
                    self.equals.append(game)
        return self.equals
    
    def winningEqualsList(self) -> list:
        self.winning_equals = []
        with open(rf"Matches.json", 'r') as file:
            for game in json.load(file).values():
                if (self._equalTo(game) and game[-1]):
                    self.winning_equals.append(game)
        return self.winning_equals
    
    def _identicalsList(self) -> list:
        self.identicals = []
        with open(rf"Matches.json", 'r') as file:
            for game in json.load(file).values():
                if (self.resume == game):
                    self.identicals.append(game)
        return self.identicals

    def finishIf(self) -> bool:
        if (self._isFinished()):
            print("There's no winner.")
            self.resume[-1] = True # A draft is considered a computer's win
            return self.save()

    def hasEquals(self) -> bool:
        return self.equalsList()

    def hasWinningEquals(self) -> bool:
        return self.winningEqualsList()
    
    def hasIdenticals(self) -> bool:
        return self._identicalsList()

    def _isFinished(self) -> bool:
        return (self.cursor >= 8 and len(self.current_game) == 9)

    def save(self) -> bool:
        with open(rf"Matches.json", 'r') as file:
            dictionary: dict = json.load(file)
        id_ = max(map(int, dictionary.keys())) + 1
        with open(rf"Matches.json", 'w') as file:
            dictionary[str(id_)] = self.resume
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
    b = Box()
    m = Moves()
    avaiableBoxes = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    while (True):
        # Printing the table
        b.print()

        # User's move
        move = input("Insert the number of the case you want: ")
        if (b.grid[int(move)] == move): # The box is free
            b.grid[int(move)] = 'X'
            m.add(move)
            avaiableBoxes.remove(int(move))
            if (b.check()):
                print("The human player won.")
                m.save()
                return True
        else: # The box is already occupied
            print("Your case is already occupied. Game Over.")
            return False
        
        # Draft check
        if (m.finishIf()):
            return True

        # Computer's move
        if (m.hasEquals()):
            if (m.hasWinningEquals()):
                case = int(m.winningEqualsList()[-1][m.cursor])
            else: # The previously played games are not winning
                if (len(m.equalsList()) == 9): # All the possibilities are cooked
                    case = choice(avaiableBoxes)
                else:
                    possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
                    for game in m.equalsList():
                        try:
                            possibilities.remove(int(game[m.cursor]))
                        except KeyError:
                            pass
                    # print(f"Computer's possibilities: {possibilities}")
                    # print(f"Avaiable boxes: {avaiableBoxes}")
                    # print(f"Intersection: {possibilities.intersection(avaiableBoxes)}")
                    if possibilities.intersection(avaiableBoxes):
                        case = choice(list(possibilities.intersection(avaiableBoxes)))
                    else:
                        case = choice(avaiableBoxes)
        else:
            case = choice(avaiableBoxes)
        try:
            b.grid[case] = 'O'
            m.add(str(case))
        except UnboundLocalError: # The variable case is still empty
            b.grid[case := choice(avaiableBoxes)] = 'O'
            m.add(str(case))
        avaiableBoxes.remove(case)

        if (b.check()):
            print("The computer won.")
            m.resume[-1] = True # The computer won? Yes, True.
            m.save()
            return True


if __name__ == '__main__':
    print(f"Professor Falken, welcome to Tris v{__version__} by {__author__}.")
    game()
else:
    print(f"You imported the module Tris v{__version__} by {__author__}.")
    print("You can now use the function Tris.game() when you want.")