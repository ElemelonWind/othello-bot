# Name: Cindy Yang
# Date: 12/15/2021

import random
import copy

class RandomBot:
   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None

   def best_strategy(self, board, color):
      # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      
      ''' Your code goes here ''' 
      if self.stones_left(board) == 0: return (-1, -1), 0
      moves = self.find_moves(board, color)
      if len(moves) == 0: return (-1, -1), 0
      best_move = random.choice(tuple(moves)) # change this
      return best_move, 0

   def stones_left(self, board):
    # returns number of stones that can still be placed (empty spots)
    count = 0  
    for i in range(self.x_max):
       for j in range(self.y_max):
           if board[i][j] == ".":
               count += 1
    return count


   def find_moves(self, board, color):
    # finds all possible moves
    moves = set()
    for i in range(self.x_max):
        for j in range(self.y_max):
            legal = False 
            for dir in self.directions:
                curX = i+dir[0]
                curY = j+dir[1]
                if curX >= 0 and curY >= 0 and curX < self.x_max and curY < self.y_max and board[curX][curY] == self.opposite_color[color] and board[i][j] == ".":
                  while curX >= 0 and curY >= 0 and curX < self.x_max and curY < self.y_max:
                     # print(i, j, curX, curY)
                     if board[curX][curY] == ".":
                        break 
                     if board[curX][curY] == self.opposite_color[color]:
                        curX += dir[0]
                        curY += dir[1]
                     elif board[curX][curY] == color:
                        moves.add((i, j))
                        legal = True 
                        break 
                if legal: 
                   continue
    return moves


   def find_flipped(self, board, x, y, color):
    # finds which chips would be flipped given a move and color
      flipped = set()
      for dir in self.directions:
         curX = x+dir[0]
         curY = y+dir[1]
         toFlip = set()
         while curX >= 0 and curY >= 0 and curX < self.x_max and curY < self.y_max:
            if board[curX][curY] == self.opposite_color[color]:
               toFlip.add((curX, curY))
               curX += dir[0]
               curY += dir[1]
            elif board[curX][curY] == color:
               flipped += toFlip 
               break 
            else:
               break

      return flipped

class Minimax_AI_bot:

   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None

   def best_strategy(self, board, color):
    # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      return self.minimax(board, color, 4)
      # return self.alphabeta(board, color, 5, float("-inf"), float("inf"))

   def minimax(self, board, color, search_depth):
    # returns best "value"
      sol = self.max_value(board, color, search_depth, -1, -1, -1, -1)
      return sol

   def max_value(self, board, color, search_depth, maxX, maxY, minX, minY):
      if search_depth == 0: return (maxX, maxY), self.evaluate(board, color)
      moves = self.find_moves(board, color)
      if len(moves) == 0: return (-1, -1), self.evaluate(board, color) 
      v = ((maxX, maxY), float("-inf"))
      for curX, curY in moves:
         cur = self.min_value(self.make_move(copy.deepcopy(board), color, curX, curY, self.find_flipped(board, curX, curY, color)), color, search_depth-1, curX, curY, minX, minY)
         if cur[1] > v[1]:
               v = (curX, curY), cur[1]
      return v

   def min_value(self, board, color, search_depth, maxX, maxY, minX, minY):
      if search_depth == 0: return (minX, minY), self.evaluate(board, color)
      moves = self.find_moves(board, self.opposite_color[color])
      if len(moves) == 0: return (-1, -1), self.evaluate(board, color) 
      v = ((minX, minY), float("inf"))
      for curX, curY in moves:
         cur = self.max_value(self.make_move(copy.deepcopy(board), self.opposite_color[color], curX, curY, self.find_flipped(board, curX, curY, self.opposite_color[color])), color, search_depth-1, maxX, maxY, curX, curY)
         if cur[1] < v[1]:
               v = (curX, curY), cur[1]
      return v

   def stones_left(self, board):
    # returns number of stones that can still be placed
      count = 0  
      for i in range(self.x_max):
         for j in range(self.y_max):
            if board[i][j] == ".":
                  count += 1
      return count

   def make_move(self, board, color, x, y, flipped):
    # returns board that has been updated
      board[x][y] = color
      for r, c in flipped:
         board[r][c] = color
      return board

   def evaluate(self, board, color):
    # returns the utility value
      return self.score(board, color) - self.score(board, self.opposite_color[color])

   def score(self, board, color):
    # returns the score of the board 
      sum = 0 
      for r in range(self.x_max):
         for c in range(self.y_max):
            if board[r][c] == color: sum += 1
      return sum

   def find_moves(self, board, color):
    # finds all possible moves
      moves = set()
      for i in range(self.x_max):
         for j in range(self.y_max):
               legal = False 
               for dir in self.directions:
                  curX = i+dir[0]
                  curY = j+dir[1]
                  if curX >= 0 and curY >= 0 and curX < self.x_max and curY < self.y_max and board[curX][curY] == self.opposite_color[color] and board[i][j] == ".":
                     while curX >= 0 and curY >= 0 and curX < self.x_max and curY < self.y_max:
                        # print(i, j, curX, curY)
                        if board[curX][curY] == ".":
                           break 
                        if board[curX][curY] == self.opposite_color[color]:
                           curX += dir[0]
                           curY += dir[1]
                        elif board[curX][curY] == color:
                           moves.add((i, j))
                           legal = True 
                           break 
                  if legal: 
                     continue
      return moves

   def find_flipped(self, board, x, y, color):
    # finds which chips would be flipped given a move and color
      flipped = set()
      for dir in self.directions:
         curX = x+dir[0]
         curY = y+dir[1]
         toFlip = set()
         while curX >= 0 and curY >= 0 and curX < self.x_max and curY < self.y_max:
            if board[curX][curY] == self.opposite_color[color]:
               toFlip.add((curX, curY))
               curX += dir[0]
               curY += dir[1]
            elif board[curX][curY] == color:
               flipped = flipped.union(toFlip)
               break 
            else:
               break

      return flipped

class Alpha_beta_AI_bot:

   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None

   def best_strategy(self, board, color):
    # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      # return self.minimax(board, color, 4)
      return self.alphabeta(board, color, 6, float("-inf"), float("inf"))
      
   def alphabeta(self, board, color, search_depth, alpha, beta):
    # returns best "value" while also pruning
      sol = self.max_ab(board, color, search_depth, alpha, beta, -1, -1, -1, -1)
      return sol
   
   def max_ab(self, board, color, search_depth, alpha, beta, maxX, maxY, minX, minY):
      if search_depth == 0: return (maxX, maxY), self.evaluate(board, color)
      moves = self.find_moves(board, color)
      if len(moves) == 0: return (-1, -1), self.evaluate(board, color) 
      v = ((maxX, maxY), float("-inf"))
      for curX, curY in moves:
         cur = self.min_ab(self.make_move(copy.deepcopy(board), color, curX, curY, self.find_flipped(board, curX, curY, color)), color, search_depth-1, alpha, beta, curX, curY, minX, minY)
         if cur[1] > v[1]:
               v = (curX, curY), cur[1]
         if v[1] > beta: return v
         alpha = max(alpha, v[1])
      return v

   def min_ab(self, board, color, search_depth, alpha, beta, maxX, maxY, minX, minY):
      if search_depth == 0: return (minX, minY), self.evaluate(board, color)
      moves = self.find_moves(board, self.opposite_color[color])
      if len(moves) == 0: return (-1, -1), self.evaluate(board, color) 
      v = ((minX, minY), float("inf"))
      for curX, curY in moves:
         cur = self.max_ab(self.make_move(copy.deepcopy(board), self.opposite_color[color], curX, curY, self.find_flipped(board, curX, curY, self.opposite_color[color])), color, search_depth-1, alpha, beta, maxX, maxY, curX, curY)
         if cur[1] < v[1]:
               v = (curX, curY), cur[1]
         if v[1] < alpha: return v 
         beta = min(beta, v[1])
      return v

   def stones_left(self, board):
    # returns number of stones that can still be placed
      count = 0  
      for i in range(self.x_max):
         for j in range(self.y_max):
            if board[i][j] == ".":
                  count += 1
      return count

   def make_move(self, board, color, x, y, flipped):
    # returns board that has been updated
      board[x][y] = color
      for r, c in flipped:
         board[r][c] = color
      return board

   def evaluate(self, board, color):
    # returns the utility value
      return self.score(board, color) - self.score(board, self.opposite_color[color])

   def score(self, board, color):
    # returns the score of the board 
      sum = 0 
      for r in range(self.x_max):
         for c in range(self.y_max):
            if board[r][c] == color: sum += 1
      return sum

   def find_moves(self, board, color):
    # finds all possible moves
      moves = set()
      for i in range(self.x_max):
         for j in range(self.y_max):
               legal = False 
               for dir in self.directions:
                  curX = i+dir[0]
                  curY = j+dir[1]
                  if curX >= 0 and curY >= 0 and curX < self.x_max and curY < self.y_max and board[curX][curY] == self.opposite_color[color] and board[i][j] == ".":
                     while curX >= 0 and curY >= 0 and curX < self.x_max and curY < self.y_max:
                        # print(i, j, curX, curY)
                        if board[curX][curY] == ".":
                           break 
                        if board[curX][curY] == self.opposite_color[color]:
                           curX += dir[0]
                           curY += dir[1]
                        elif board[curX][curY] == color:
                           moves.add((i, j))
                           legal = True 
                           break 
                  if legal: 
                     continue
      return moves

   def find_flipped(self, board, x, y, color):
    # finds which chips would be flipped given a move and color
      flipped = set()
      for dir in self.directions:
         curX = x+dir[0]
         curY = y+dir[1]
         toFlip = set()
         while curX >= 0 and curY >= 0 and curX < self.x_max and curY < self.y_max:
            if board[curX][curY] == self.opposite_color[color]:
               toFlip.add((curX, curY))
               curX += dir[0]
               curY += dir[1]
            elif board[curX][curY] == color:
               flipped = flipped.union(toFlip)
               break 
            else:
               break

      return flipped

class Best_AI_bot:

   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None

   def best_strategy(self, board, color):
    # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      # return self.minimax(board, color, 3)
      return self.alphabeta(board, color, 4, float("-inf"), float("inf"))

   def alphabeta(self, board, color, search_depth, alpha, beta):
    # returns best "value" while also pruning
      sol = self.max_ab(board, color, search_depth, alpha, beta, -1, -1, -1, -1)
      return sol
   
   def max_ab(self, board, color, search_depth, alpha, beta, maxX, maxY, minX, minY):
      if search_depth == 0: return (maxX, maxY), self.evaluate(board, color)
      moves = self.find_moves(board, color)
      if len(moves) == 0: return (-1, -1), self.evaluate(board, color) 
      v = ((maxX, maxY), float("-inf"))
      for curX, curY in moves:
         cur = self.min_ab(self.make_move(copy.deepcopy(board), color, curX, curY, self.find_flipped(board, curX, curY, color)), color, search_depth-1, alpha, beta, curX, curY, minX, minY)
         if cur[1] > v[1]:
               v = (curX, curY), cur[1]
         if v[1] > beta: return v
         alpha = max(alpha, v[1])
      return v

   def min_ab(self, board, color, search_depth, alpha, beta, maxX, maxY, minX, minY):
      if search_depth == 0: return (minX, minY), self.evaluate(board, color)
      moves = self.find_moves(board, self.opposite_color[color])
      if len(moves) == 0: return (-1, -1), self.evaluate(board, color) 
      v = ((minX, minY), float("inf"))
      for curX, curY in moves:
         cur = self.max_ab(self.make_move(copy.deepcopy(board), self.opposite_color[color], curX, curY, self.find_flipped(board, curX, curY, self.opposite_color[color])), color, search_depth-1, alpha, beta, maxX, maxY, curX, curY)
         if cur[1] < v[1]:
               v = (curX, curY), cur[1]
         if v[1] < alpha: return v 
         beta = min(beta, v[1])
      return v

   def minimax(self, board, color, search_depth):
    # returns best "value"
      sol = self.max_value(board, color, search_depth, -1, -1, -1, -1)
      return sol

   def max_value(self, board, color, search_depth, maxX, maxY, minX, minY):
      if search_depth == 0: return (maxX, maxY), self.evaluate(board, color)
      moves = self.find_moves(board, color)
      if len(moves) == 0: return (-1, -1), self.evaluate(board, color) 
      v = ((maxX, maxY), float("-inf"))
      for curX, curY in moves:
         cur = self.min_value(self.make_move(copy.deepcopy(board), color, curX, curY, self.find_flipped(board, curX, curY, color)), color, search_depth-1, curX, curY, minX, minY)
         if cur[1] > v[1]:
               v = (curX, curY), cur[1]
      return v

   def min_value(self, board, color, search_depth, maxX, maxY, minX, minY):
      if search_depth == 0: return (minX, minY), self.evaluate(board, color)
      moves = self.find_moves(board, self.opposite_color[color])
      if len(moves) == 0: return (-1, -1), self.evaluate(board, color) 
      v = ((minX, minY), float("inf"))
      for curX, curY in moves:
         cur = self.max_value(self.make_move(copy.deepcopy(board), self.opposite_color[color], curX, curY, self.find_flipped(board, curX, curY, self.opposite_color[color])), color, search_depth-1, maxX, maxY, curX, curY)
         if cur[1] < v[1]:
               v = (curX, curY), cur[1]
      return v

   def stones_left(self, board):
    # returns number of stones that can still be placed
      count = 0  
      for i in range(self.x_max):
         for j in range(self.y_max):
            if board[i][j] == ".":
                  count += 1
      return count

   def make_move(self, board, color, x, y, flipped):
    # returns board that has been updated
      board[x][y] = color
      for r, c in flipped:
         board[r][c] = color
      return board

   def evaluate(self, board, color):
    # returns the utility value
    score = self.score(board, color) - self.score(board, self.opposite_color[color])
    if self.stones_left(board) > 14:
        score /= 100 
        score += len(self.find_moves(board, color)) - len(self.find_moves(board, self.opposite_color[color]))
        for x, y in [(0, 0), (0, self.y_max-1), (self.x_max-1, 0), (self.x_max-1, self.y_max-1)]:
            if board[x][y] == color:
                score += 10 
            elif board[x][y] == self.opposite_color[color]:
                score -= 10
    return score

   def score(self, board, color):
    # returns the score of the board 
      sum = 0 
      for r in range(self.x_max):
         for c in range(self.y_max):
            if board[r][c] == color: sum += 1
      return sum

   def find_moves(self, board, color):
    # finds all possible moves
    moves_found = set()
    for i in range(self.x_max):
        for j in range(self.y_max):
            flipped_stones = self.find_flipped(board, i, j, color)
            if len(flipped_stones) > 0:
                moves_found.add((i, j))
    return moves_found

   def find_flipped(self, board, x, y, color):
    # finds which chips would be flipped given a move and color
    if board[x][y] != ".":
        return []
    flipped_stones = set()
    for incr in self.directions:
        temp_flip = set()
        x_pos = x + incr[0]
        y_pos = y + incr[1]
        while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
            if board[x_pos][y_pos] == ".":
                break
            if board[x_pos][y_pos] == color:
                flipped_stones = flipped_stones.union(temp_flip)
                break
            temp_flip.add((x_pos, y_pos))
            x_pos += incr[0]
            y_pos += incr[1]
    return flipped_stones