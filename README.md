# crossword
Greedy python 3 crossword generator script that tries to place words from a list inside a grid.

This project was developed for fun. It is neither optimised nor super efficient.

## usage

1. Create a word file containing one word on each line, like this:

```
river
otter
crossword
```

2. Run the programme using

```
python crossword.py <your_word_file>
```
This is a greedy algorithm, with some randomness to it, so each run gives a different solution. Jsut run it until you get an interesting one.

It will display the words arranged in a grid, and possibly a list of unused words if it was not able to place them all.

The placement is random each time, so try again until happy with the result.

### Example output:
```

C R O S S W O R D  
            T      
            T      
      R I V E R    
            R      


```
