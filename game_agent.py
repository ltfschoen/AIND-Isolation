"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import logging
import typing; from typing import *
from heuristics import null_score, open_move_score, improved_score

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
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

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    heuristics_options = {
        "null_score": null_score,
        "open_move_score": open_move_score,
        "improved_score": improved_score
    }

    return heuristics_options["improved_score"](game, player)

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate successors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            pass

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Initialise variable for no legal moves
        no_legal_moves = (-1, -1)
        best_move = no_legal_moves
        best_utility = float('-inf') if maximizing_player else float('inf')
        current_player = game.active_player if maximizing_player else game.inactive_player
        remaining_legal_moves = game.get_legal_moves(game.active_player)

        logging.debug("Current player is Maximizing: %r", maximizing_player)
        logging.debug("Current depth: %r", depth)
        logging.debug("Best utility: %r", best_utility)
        logging.debug("Remaining legal moves: %r", remaining_legal_moves)

        # Recursion function termination conditions when legal moves exhausted or no plies left
        if not remaining_legal_moves:
            logging.debug("Recursion terminated due to no remaining legal moves")
            return game.utility(current_player), no_legal_moves
        elif depth == 0:
            logging.debug("Recursion terminated due to no more plies to search")
            return self.score(game, current_player), remaining_legal_moves[0]

        # Recursively alternate between Maximise and Minimise calculations for decrementing depths
        for move in remaining_legal_moves:
            logging.debug("Recursion with move: %r", move)
            logging.debug("Best utility: %r", best_utility)
            logging.debug("Best move: %r", best_move)

            # Obtain successor of current state by creating copy of board and applying a move.
            forecast_game = game.forecast_move(move)
            forecast_utility, _ = self.minimax(forecast_game, depth - 1, not maximizing_player)
            logging.debug("Forecast utility: %r", forecast_utility)

            if maximizing_player:
                logging.debug("Checking move with Maximising player, forecast_utility > best_utility? : %r", (forecast_utility > best_utility))
                if forecast_utility > best_utility:
                    best_utility, best_move = forecast_utility, move
            else:
                logging.debug("Checking move with Minimising player, forecast_utility < best_utility? : %r", (forecast_utility > best_utility))
                if forecast_utility < best_utility:
                    best_utility, best_move = forecast_utility, move

        return best_utility, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        raise NotImplementedError

def run():
    try:
        # Copy of minimax Unit Test for debugging only
        import isolation
        h, w = 7, 7
        test_depth = 1
        starting_location = (5, 3)
        adversary_location = (0, 0)
        iterative_search = False
        search_method = "minimax"
        heuristic = lambda g, p: 0.
        agentUT = CustomPlayer(
            test_depth, heuristic, iterative_search, search_method)
        agentUT.time_left = lambda: 99
        board = isolation.Board(agentUT, 'null_agent', w, h)
        board.apply_move(starting_location)
        board.apply_move(adversary_location)

        for move in board.get_legal_moves():
            next_state = board.forecast_move(move)
            v, _ = agentUT.minimax(next_state, test_depth)
            assert type(v) is float, "Minimax function should return a floating point value approximating the score for the branch being searched."
        return
    except SystemExit:
        logging.exception('SystemExit occurred')
    except:
        logging.exception('Unknown exception occurred.')

if __name__ == '__main__':
    run()