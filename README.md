# othello-bot
othello strategy board game for two players, played on an 8×8 uncheckered board. 

## algorithms
`RandomBot` moves randomly by computing a list of valid moves and choosing one. <br>
`Minimax AI` uses the basic minimax algorithm with limited depth, looking 4 moves ahead. <br>
`Alphabeta AI` uses the alphabeta algorithm, which introduces pruning to the minimax game tree. it is able to look 5 moves ahead due to this optimization. <br>
`Best AI` uses alphabeta again, and also implements a better evaluation method. <br>

## heuristic 
i used the heuristic introduced by yunpeng li and dobo radichkov from cornell university. the evaluation function returns an integer specifying the attractiveness of a potential move. the greater the number, the more attractive a given move is. the number returned is evaluated through three components: disc count, legal moves count, and corner squares. 

#### disc count
the goal of the game is to have more discs than the opponent, however, maximizing one’s disc count is a very poor strategy. therefore, little weight is given to a player’s number of discs, namely a weight of 1/100.

#### legal moves count
each legal move is counted as 1. this makes the number of discs (weighted 1/100) irrelevant unless the number of legal moves is equal, in which case we prefer the move that results in a greater disc count.

#### corner squares
the squares in the corners of the board are strategic positions that result in great advantage when occupied: a disc in a corner square can never be flipped. for this reason, a value of 10 is assigned to each corner square, and thus one corner square is worth 10 legal moves or 1000 discs.
