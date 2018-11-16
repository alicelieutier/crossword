"""
Helper to create a grid of crosswords from a list of words
"""
import sys
import random

class Grid:
  DOWN, ACCROSS = True, False
  EMPTY = ' '
  MAX_NB_OF_TRIES = 8

  def __init__(self, words=None, size=10):
    if not words:
      words = ['hello', 'world']
    self.words = self.arrange_words(words)
    self.letters = {}
    self.used_words = set()
    self.tries = 0
    self.size = size
    self.grid = self.empty_grid(self.size)

    # seed the grid with an E (because E is a common letter..)
    self.letters['E'] = {
      (random.randint(1,self.size - 2), random.randint(1,self.size - 2))
    }
    self.fill_grid()


  def fill_grid(self):
    self.tries += 1
    for word in self.words:
      if (word not in self.used_words):
        word_was_added = self.__try_word(word)
        if (word_was_added):
          self.used_words.add(word)
    if self.tries < self.MAX_NB_OF_TRIES:
      self.fill_grid()
    else:
      unused_words = self.words - self.used_words
      if len(unused_words) > 0:
          print(
            'Unused words: ' + ', '.join(unused_words)
          )


  def __try_word(self, word):
    for (i, letter) in enumerate(word):
      if letter in self.letters:
        for (x,y) in self.letters[letter]:
          # try to fit the word vertically
          if self.__try_word_down(word, x, y - i):
            self.__write_word(word, x, y - i, self.DOWN)
            return True
          # try to fit the word horizontally
          if self.__try_word_accross(word, x - i, y):
            self.__write_word(word, x - i, y, self.ACCROSS)
            return True
    return False

  """
  Try to fit word down, starting at position x, y
  This function does not write the word, it only checks whether it would fit
  Returns True if the word would fit, False otherwise
  """
  def __try_word_down(self, word, x, y):
    if y < 0:
      # y is out of the grid
      return False
    if y >= 1 and self.grid[x][y - 1] != self.EMPTY:
      # there is a letter just above the starting position
      return False
    for letter in word:
      if y >= self.size:
        # we got out of the grid
        return False
      if self.grid[x][y] not in {letter, self.EMPTY}:
        # we are trying to write over a different letter
        return False
      if self.grid[x][y] == self.EMPTY:
        if x - 1 >= 0:
          # look left
          if self.grid[x - 1][y] != self.EMPTY:
            # there is a letter on the left that is not part
            # of a crossing horizontal word
            return False
        if x + 1 < self.size:
          # look right
          if self.grid[x + 1][y] != self.EMPTY:
            # there is a letter on the right that is not part
            # of a crossing horizontal word
            return False
      # go to the next position
      y += 1
    if y < self.size and self.grid[x][y] != self.EMPTY:
      # there is a letter right under the word
      return False
    return True

  """
  Try to fit word accross, starting at position x, y
  This function does not write the word, it only checks whether it would fit
  Returns True if the word would fit, False otherwise

  Basically same as __try_word_down, except horizontal, so moving x
  """
  def __try_word_accross(self, word, x, y):
    if x < 0:
      return False
    if x >= 1 and self.grid[x - 1][y] != self.EMPTY:
      return False
    for letter in word:
      if x >= self.size:
        return False
      if self.grid[x][y] not in {letter, self.EMPTY}:
        return False
      if self.grid[x][y] == self.EMPTY:
        if y - 1 >= 0:
          if self.grid[x][y - 1] != self.EMPTY:
            return False
        if y + 1 < self.size:
          if self.grid[x][y + 1] != self.EMPTY:
            return False
      x += 1
    if x < self.size and self.grid[x][y] != self.EMPTY:
      return False
    return True

  """
  Writes the word on the grid at the postion x, y, in the given direction.
  Does not check anything, so use only after one of
  __try_word_down or __try_word_accross
  """
  def __write_word(self, word, x, y, direction):
    for letter in word:
      self.grid[x][y] = letter
      self.letters.setdefault(letter, set()).add((x,y))
      if direction: # this is made possible because self.DOWN = True
        y += 1
      else:
        x += 1

  """
  Display the grid nicely.
  Call using print(myGrid)
  """
  def __str__(self):
    display = []
    for line in self.grid:
      display.append(' '.join(line))
    return '\n'.join(display)

  """
  Creates an empty square grid of given size
  """
  def empty_grid(self, size):
    grid = []
    for i in range(size):
      grid.append([])
      for j in range(size):
        grid[i].append(self.EMPTY)
    return grid

  """
  Removes duplicates + makes all words uppercase
  """
  def arrange_words(self, words):
    words = {self.__format_word(w) for w in words}
    return words

  """
  Checks that word uses alphabetic characters + makes it uppercase
  """
  def __format_word(self, word):
    if not word.isalpha():
      raise Exception('''
      Words should use only alphabetic characters.
      Word given: {}'''.format(word))
    return word.upper()


if __name__ == '__main__':

  words = ['crossword', 'generator']

  if len(sys.argv) > 1:
      word_file = open(sys.argv[1])
      words = [line.strip() for line in word_file.readlines()]

  g = Grid(words)
  print(g)
