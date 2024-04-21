#!/usr/bin/python3
#  agent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW

'''
Data Structures: The program utilizes a numpy array to represent the game boards. 
Each cell of the array can hold three values: 0 for empty, 1 for the agent's move, and 2 for the opponent's move. 
It also uses lists to represent win situations and potentially winning configurations.

Game Logic: The game logic revolves around the play() function, 
which determines the agent's move based on the current state of the board. 
Initially, it randomly selects a move. However, as the game progresses, 
it employs a minimax algorithm with alpha-beta pruning to choose the best move.

Algorithms Used:

The player_turn() function uses alpha-beta pruning to search for the best move. 
It evaluates possible moves based on their potential to lead to a win, block the opponent, 
or create future advantageous positions.
The alphabeta_algorithm() function recursively explores possible moves up to a certain depth, 
evaluating the score for each move. Alpha-beta pruning is used to improve the efficiency of the search 
by pruning branches that are guaranteed to be worse than the current best move.
'''

import socket
import sys
import numpy as np
import random
# a board cell can hold:
#   0 - Empty
#   1 - We played here
#   2 - Opponent played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".","X","O"]
curr = 0 # this is the current board to play in
infinity = sys.maxsize
# print a row
def print_board_row(bd, a, b, c, i, j, k):
    print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
             +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
             +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]])

win_situation = [
    [1, 2, 3],
	[4, 5, 6],
	[7, 8, 9],
	[1, 4, 7],
	[2, 5, 8],
	[3, 6, 9],
	[1, 5, 9],
	[3, 5, 7]
]

protentially_win = [
    [win_situation[0], win_situation[3], win_situation[6]],
	[win_situation[0], win_situation[4]],
	[win_situation[0], win_situation[5], win_situation[7]],
	[win_situation[1], win_situation[3]],
	[win_situation[1], win_situation[4], win_situation[6], win_situation[7]],
	[win_situation[1], win_situation[5]],
	[win_situation[2], win_situation[3], win_situation[7]],
	[win_situation[2], win_situation[4]],
	[win_situation[2], win_situation[5], win_situation[6]]
]

def curr_position(board, curr):
    """
    Retrieve the positions of the player's and opponent's pieces on a specified board.
    """
    bd = board[curr]
    player_positions = []
    opponent_positions = []

    # Iterate over each row and column of the board
    for i in range(1,10):
        if bd[i] == 1:
            player_positions.append(i)
        elif bd[i] == 2:
            opponent_positions.append(i)

    return (player_positions, opponent_positions)

def check_init_case(board, curr):
    player, oppo = curr_position(board,curr)
    tri = [1,3,7,9]
    player_ret = False
    oppo_ret = False
    if len(set(player)) == 1 and player[0] in tri:
        player_ret = True
    if len(set(oppo)) == 1 and oppo[0] in tri:
        oppo_ret = True
    return player_ret, oppo_ret

def curr_score(board, curr, position_to_place):
    """
    Calculate the score for the current board configuration from the perspective of the current player.

    Parameters:
        board (numpy.ndarray): The game board.
        curr (int): The index of the current sub-board.
        position_to_place (int): The position to place the next move.

    Returns:
        list: A list containing the score for the current configuration and a boolean indicating if a win is achieved.
    """
    win = False
    # to adjust the index which starts from 1
    # position_to_place - 1

    # larger score means larger possibility to win
    score_to_win = 0
    # score_on_board is to evaluate the layout of the game
    for possible_win in protentially_win[position_to_place - 1]:
        score_on_board = 0
        if board[curr][possible_win[0]] == 1:
            score_on_board += 1
        elif board[curr][possible_win[0]] == 2:
            score_on_board -= 1
        if board[curr][possible_win[1]] == 1:
            score_on_board += 1
        elif board[curr][possible_win[1]] == 2:
            score_on_board -= 1
        if board[curr][possible_win[2]] == 1:
            score_on_board += 1
        elif board[curr][possible_win[2]] == 2:
            score_on_board -= 1

        if score_on_board == 3 or score_on_board == -3:
            score_to_win = score_on_board * 100000
            win = True
            break

        # And {x _ x} is better than {x x _}
        elif score_on_board == 2:
            score_to_win += 2000
            if board[curr][possible_win[1]] == 0:
                score_to_win += 500

        elif score_on_board == -2:
            score_to_win -= 2000
            if board[curr][possible_win[1]] == 0:
                score_to_win -= 500
        elif score_on_board == 1 or score_on_board == -1:
            # player can block a win situation
            if board[curr][possible_win[0]] & board[curr][possible_win[1]] & board[curr][possible_win[2]]:
            #if board[curr][possible_win[0]] != 0 and board[curr][possible_win[1]] != 0 and board[curr][possible_win[2]] != 0:
                score_to_win -= score_on_board * 500

    return score_to_win, win

def player_turn(board, curr):
    """
    Determine the best move for the current player using alpha-beta pruning.

    Parameters:
        board (numpy.ndarray): The game board.
        curr (int): The index of the current sub-board.

    Returns:
        int: The position for the next move.
    """

    search_depth = 3
    max_val = -float('inf')
    for i in range(1, 10):
        if board[curr][i] == 0:
            board[curr][i] = 1
            score_cur,if_won = curr_score(board, curr, i)
            if count_step > 5:
                search_depth = 7

            val = alphabeta_algorithm(board, i, 2, 1, -float('inf'), float('inf'), score_cur, 1, search_depth, if_won)

            board[curr][i] = 0

            if val > max_val:
                max_val = val
                my_move = [i]
            if val == max_val:
                my_move.append(i)
    return random.choice(my_move)


def alphabeta_algorithm(board, curr, player_cur, player_next, alpha, beta, score_sum, depth, max_depth, if_won):
    """
    Implement the alpha-beta pruning algorithm to determine the best move.

    Parameters:
        board (numpy.ndarray): The game board.
        curr (int): The index of the current sub-board.
        player_cur (int): The current player.
        player_next (int): The next player.
        alpha (float): The alpha value for alpha-beta pruning.
        beta (float): The beta value for alpha-beta pruning.
        score_sum (int): The sum of scores.
        depth (int): The depth of the search tree.
        max_depth (int): The maximum depth to search.
        if_won (bool): Indicates if a win is achieved.

    Returns:
        float: The evaluated score.
    """
    if depth >= max_depth or if_won:
        return score_sum

    for i in range(1, 10):
        if board[curr][i] == 0:
            board[curr][i] = player_cur
            score_cur,if_won = curr_score(board, curr, i)
            val = alphabeta_algorithm(board, i, player_next, player_cur, alpha, beta, score_cur + score_sum, depth + 1,  max_depth, if_won)
            board[curr][i] = 0

            if player_cur == 1:
                if val > alpha:
                    alpha = val
            else:
                if val < beta:
                    beta = val
            if beta <= alpha:
                break

    if player_cur == 1:
        return alpha
    return beta

# Print the entire board
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

def play():

    global count_step
    count_step += 1

    n = player_turn(boards, curr)

    place(curr, n, 1)
    return n

count_step = 0
def play():
    global count_step
    count_step += 1
    n = player_turn(boards, curr)
    place(curr, n, 1)
    print_board(boards)
    return n

# place a move in the global boards
def place( board, num, player ):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    # init tells us that a new game is about to begin.
    # start(x) or start(o) tell us whether we will be playing first (x)
    # or second (o); we might be able to ignore start if we internally
    # use 'X' for *our* moves and 'O' for *opponent* moves.

    # second_move(K,L) means that the (randomly generated)
    # first move was into square L of sub-board K,
    # and we are expected to return the second move.
    if command == "second_move":
        # place the first move (randomly generated for opponent)
        place(int(args[0]), int(args[1]), 2)
        return play()  # choose and return the second move

    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        # place the first move (randomly generated for us)
        place(int(args[0]), int(args[1]), 1)
        # place the second move (chosen by opponent)
        place(curr, int(args[2]), 2)
        return play() # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        place(curr, int(args[0]), 2)
        return play() # choose and return our next move

    elif command == "win":
        print("Yay!! We win!! :)")
        return -1

    elif command == "loss":
        print("We lost :(")
        return -1

    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
