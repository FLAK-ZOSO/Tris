# Tris

Joshua is a Tic Tac Toe engine that learns to play from the user.

## How to use

1. Run the script `Tris.py`.

```bash
python Tris.py
```

2. Follow the instructions on the screen.
3. Play against Joshua, and teach him how to play.

# How it works

The engine is dynamic and takes its decisions based on the matches it has played in the past.

Those matches are stored in the file [`Matches.json`](../Matches.json).

# Future changes

- [ ] Add a control to the function `game()` to delete from [`Matches.json`](https://github.com/FLAK-ZOSO/Tris/blob/2e68d1dab5c43d7d24307f4817746f9313fb8f29/Matches.json) all those matches which are duplicates.
- [ ] Do not make the choice random once the common prefix is found with no winning outcomes, but rather base the decision on the most common suffix or on the rate of wins.
