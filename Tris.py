#usr/bin/env python3
from random import choice, randint
import table
import Moves
import Boxes

__version__ = 3.5
__author__ = "FLAK-ZOSO"

def game() -> bool:

    # Start
    b = Boxes.Box()
    m = Moves.Moves()
    avaiableBoxes = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Game
    while (True):
        # Printing the table
        print(table.table(b.dict.values()))

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

        # Tie (?)
        if (m.list[-2] != None): # All the cases are occupied
            print("There's no winner.")
            m.list[-1] = True # A tie is considered a computer's win
            m.save()
            return True
        
        # Computer's move
        if (m.hasEquals()):
            if (m.hasWinningEquals()):
                case = int(m.winningEqualsList()[-1][m.counter]) # removed +1
            else:
                possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for game in m.equalsList():
                    try:
                        possibilities.remove(int(game[m.counter])) # removed +1
                    except ValueError:
                        pass
                if (not set(possibilities) - set(avaiableBoxes)):
                    case = choice(avaiableBoxes)
        else:
            case = choice(avaiableBoxes)
        try:
            b.dict[case] = 'O'
            m.add(str(case))
        except UnboundLocalError:
            b.dict[case := choice(avaiableBoxes)] = 'O'
            m.add(str(case))
        avaiableBoxes.remove(case)
        del case
        if (b.check()):
            print("The computer won.")
            m.list[-1] = True # The computer won? Yes, True.
            m.save()
            return True

        # Tie (?)
        if (m.list[-2] != None): # All the cases are occupied
            print("There's no winner.")
            m.list[-1] = True # A tie is considered a computer's win
            m.save()
            return True
