"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # raise NotImplementedError
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    opponent = game.get_opponent(player)
    player_mv = game.get_legal_moves(player)
    opponent_mv = game.get_legal_moves(opponent)
    player_mv_left = len(player_mv)
    opponent_mv_left = len(opponent_mv)

    if player_mv_left != opponent_mv_left:
        return float(player_mv_left - opponent_mv_left)
    else:
        # look for a positional advantage if player and its opponent have the same number of moves left
        # Access positional advantage by using Manhattan distance to the center of the board
        center_y, center_x = int(game.height / 2), int(game.width / 2)
        player_y, player_x = game.get_player_location(player)
        opponent_y, opponent_x = game.get_player_location(opponent)
        player_distance = abs(player_y - center_y) + abs(player_x - center_x)
        opponent_distance = abs(opponent_y - center_y) + abs(opponent_x - center_x)
        return float(opponent_distance - player_distance) / 10

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!

    # This heuristic is easy to interpret and fast to compute, it is clear to the notion of
    # positional advantage but it only allows knight moves. So, this method is not great.
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    player_mv= game.get_legal_moves(player)
    opponent_mv = game.get_legal_moves(game.get_opponent(player))
    # check if we have moves more than our opponent
    player_moves_remaining = len(player_mv)
    opponent_moves_remaining = len(opponent_mv)
    return float(player_moves_remaining - opponent_moves_remaining)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # raise NotImplementedError
    # This heuristic will cause our computer player to chase after the opponent, the winning
    # move now has the highest evaluation function result. It keeps opponent closer, but it is
    # not guaranteed to be the best evaluation without seeing different variants of other
    # evaluation functions.
    
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    opponent = game.get_opponent(player)
    player_mv = len(game.get_legal_moves(player))
    opponent_mv = len(game.get_legal_moves(opponent))
    # check if we have moves more than our opponent

    return float(player_mv - (2.0 * opponent_mv))

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=40):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        if not game.get_legal_moves():
            return (-1, -1)

        best_move = game.get_legal_moves()[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # raise NotImplementedError
        # TODO: finish this function!

        # Initialize the best score
        best_val = float('-inf')

        # if it is a terminal state or no depth, return (-1, -1)
        if not game.get_legal_moves() or depth == 0:
            return (-1, -1)

        best_mv = game.get_legal_moves()[0]

        # Min value helper function
        def min_value(game, depth):
            # Set time checker
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Check if it is terminal state
            if not game.get_legal_moves() or depth == 0:
                return self.score(game,self)

            v = float ("inf")
            for m in game.get_legal_moves():
                # update best score based on minimum score
                v = min(v, max_value(game.forecast_move(m), depth-1))
            return v

        # Max value helper function
        def max_value(game, depth):
            # Set time checker
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Check if it is terminal state
            if not game.get_legal_moves() or depth == 0:
                return self.score(game,self)

            v = float("-inf")
            for m in game.get_legal_moves():
                # update best score based on maximum score
                v = max(v, min_value(game.forecast_move(m), depth-1))
            return v

        # Minimax logic follows the same as it in min_value function
        # Update both best score and best move
        for mv in game.get_legal_moves():
            v = min_value(game.forecast_move(mv), depth-1)
            if v > best_val:
                best_val = v
                best_mv = mv
        return best_mv


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        self.time_left = time_left

        # TODO: finish this function!
        if not game.get_legal_moves():
            return (-1, -1)

        best_mv = game.get_legal_moves()[0]

        try:
            current_depth = 1
            while True:
                best_mv = self.alphabeta(game, current_depth)
                current_depth += 1
        except SearchTimeout:
            pass

        return best_mv

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        # initialize the best score
        best_val = float('-inf')
        # best_mv = (-1, -1)

        # if it is a terminal state or no depth, return (-1, -1)
        if not game.get_legal_moves() or depth == 0:
            # return best_mv
            return (-1, -1)

        best_mv = game.get_legal_moves()[0]

        # Min value helper function
        def min_value(game, alpha, beta, depth):
            # Set time checker
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Check if it is terminal state
            if not game.get_legal_moves() or depth == 0:
                return self.score(game,self)

            v = float ("inf")
            for m in game.get_legal_moves():
                # update best score based on minimum score
                v = min(v, max_value(game.forecast_move(m), alpha, beta, depth-1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        # Max value helper function
        def max_value(game, alpha, beta, depth):
            # Set time checker
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Check if it is terminal state
            if not game.get_legal_moves() or depth == 0:
                return self.score(game,self)

            v = float("-inf")
            for m in game.get_legal_moves():
                # update best score based on maximum score
                v = max(v, min_value(game.forecast_move(m), alpha, beta, depth-1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        # alphabeta logic follows the same as it in min_value function
        # Update both best score and best move
        for mv in game.get_legal_moves():
            v = min_value(game.forecast_move(mv), alpha, beta, depth-1)
            # update the alpha parameter in each iteration during root-level search
            # alpha = max (v, alpha)
            if v > best_val:
                best_val = v
                best_mv = mv
            alpha = max (alpha, best_val)
        return best_mv
