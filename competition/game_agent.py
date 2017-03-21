"""AIND Isolation Player vs Player Competition
Reference: https://docs.google.com/document/d/1r4z6DF0ChUvBy-ivw0PxLbVv7xqC_E07JdOlNK3_c0c
"""
import random
import itertools

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def get_move_difference_factor(game, player) -> float:
    count_own_moves = len(game.get_legal_moves(player))
    count_opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return (count_own_moves - count_opp_moves)

def get_center_available_factor(game, player) -> float:
    own_moves = game.get_legal_moves(player)
    center_x, center_y = game.width / 2, game.height / 2
    center_available = -1
    # Center of grid is only available when odd width and odd height
    if not center_x.is_integer() and not center_y.is_integer():
        center_coords = (int(center_x), int(center_y))
        center_available = own_moves.index(center_coords) if center_coords in own_moves else -1
    # Next move should always be to center square if available
    return 2.0 if (center_available != -1) else 1.0

def is_empty_board(count_total_positions, count_empty_coords):
    all_empty = True if (count_total_positions == count_empty_coords) else False
    if all_empty:
        return 1.0

def get_reflection_available_factor(game, player) -> float:
    count_total_positions = game.height * game.width
    count_empty_coords = len(game.get_blank_spaces())

    # Return if no reflection move possible before first move
    if is_empty_board(count_total_positions, count_empty_coords):
        return 1.0

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    count_own_moves = len(game.get_legal_moves(player))
    count_opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    all_coords = list(itertools.product(range((game.width)), range((game.height))))
    player_coords = (player_x, player_y) = game.get_player_location(player)
    opp_coords = (opp_x, opp_y) = game.get_player_location(game.get_opponent(player))
    player_index = all_coords.index(player_coords)
    opp_index = all_coords.index(opp_coords)
    mirrored_all_coords = all_coords[::-1]
    mirrored_player_coords = mirrored_all_coords[player_index]
    mirrored_opp_coords = mirrored_all_coords[opp_index]

    # Return high Reflection Available Factor if the mirror coords that
    # correspond to the oppositions current coords is an available legal move for current player
    for legal_player_move_coords in own_moves:
        if legal_player_move_coords == mirrored_opp_coords:
            return 2.0
    return 1.0

def get_partition_possible_factor(game, player):
    count_total_positions = game.height * game.width
    count_empty_coords = len(game.get_blank_spaces())

    empty_coords = game.get_blank_spaces()

    # Return if no partition possible before first move
    if is_empty_board(count_total_positions, count_empty_coords):
        return 1.0

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    for move in own_moves:
        cell_left = (move[0]-1, move[1])
        cell_right = (move[0]+1, move[1])
        cell_below = (move[0], move[1]-1)
        cell_above = (move[0], move[1]+1)

        cell_left_x2 = (move[0]-2, move[1])
        cell_right_x2 = (move[0]+2, move[1])
        cell_below_x2 = (move[0], move[1]-2)
        cell_above_x2 = (move[0], move[1]+2)

        is_cell_left = cell_left not in empty_coords
        is_cell_right = cell_right not in empty_coords
        is_cell_below = cell_below not in empty_coords
        is_cell_above = cell_above not in empty_coords

        is_cell_left_x2 = cell_left_x2 not in empty_coords
        is_cell_right_x2 = cell_right_x2 not in empty_coords
        is_cell_below_x2 = cell_below_x2 not in empty_coords
        is_cell_above_x2 = cell_above_x2 not in empty_coords

        # Firstly check if two cells in sequence on either side of possible move
        # If so give double bonus points
        if ( (is_cell_left and is_cell_left_x2) or
             (is_cell_right and is_cell_right_x2) or
             (is_cell_below and is_cell_below_x2) or
             (is_cell_above and is_cell_above_x2) ):
            return 4.0

        # Secondly check if just one cell surrounding possible move
        if (is_cell_left or
            is_cell_right or
            is_cell_below or
            is_cell_above):
            return 2.0

    return 1.0

def get_improved_score_factor(game, player):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

def heuristic_1_center(game, player) -> float:
    """
    Evaluation function outputs a
    score equal to the Center Available Factor
    that has higher weight when center square still available on any move
    """
    center_available_factor = get_center_available_factor(game, player)

    # Heuristic score output
    return float(center_available_factor)

def heuristic_2_reflection(game, player) -> float:
    """
    Heuristic 2's Reflection Available Factor
    has higher weight when reflection of opposition player
    position is available on other side of board.
    i.e. In game tree, for all available opposition in coordinates,
    count how many available reflection moves (on opposite side of board)
    are available as a legal moves for the current player. These should result in
    higher weight if available
    """

    reflection_available_factor = get_reflection_available_factor(game, player)

    return float(reflection_available_factor)

def heuristic_3_partition(game, player) -> float:
    """
    Heuristic 3's Partition Growth Factor
    has higher weight when available moves are
    vertically or horizontally (not diagonally) adjacent
    to a sequence of one or two blocked locations
    """

    partition_possible_factor = get_partition_possible_factor(game, player)

    return float(partition_possible_factor)

def heuristic_combined_1_2(game, player) -> float:
    """
    Combines Heuristics 1 and 2
    """

    center_available_factor = get_center_available_factor(game, player)
    reflection_available_factor = get_reflection_available_factor(game, player)

    return float(center_available_factor + reflection_available_factor)

def heuristic_combined_1_3(game, player) -> float:
    """
    Combines Heuristics 1 and 3
    """

    center_available_factor = get_center_available_factor(game, player)
    partition_possible_factor = get_partition_possible_factor(game, player)

    return float(center_available_factor + partition_possible_factor)

def heuristic_combined_2_3(game, player) -> float:
    """
    Combines Heuristics 2 and 3
    """

    reflection_available_factor = get_reflection_available_factor(game, player)
    partition_possible_factor = get_partition_possible_factor(game, player)

    return float(reflection_available_factor + partition_possible_factor)

def heuristic_combined_1_2_3(game, player) -> float:
    """
    Combines Heuristics 1, 2 and 3
    """

    center_available_factor = get_center_available_factor(game, player)
    reflection_available_factor = get_reflection_available_factor(game, player)
    partition_possible_factor = get_partition_possible_factor(game, player)

    return float(center_available_factor +
                 reflection_available_factor +
                 partition_possible_factor)

def heuristic_combined_1_2_3_with_improve_score(game, player) -> float:
    """
    Combines Heuristics 1, 2 and 3 and improved score
    """

    center_available_factor = get_center_available_factor(game, player)
    reflection_available_factor = get_reflection_available_factor(game, player)
    partition_possible_factor = get_partition_possible_factor(game, player)
    improved_score_factor = get_improved_score_factor(game, player)

    return float((center_available_factor +
                 reflection_available_factor +
                 partition_possible_factor) * improved_score_factor)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    heuristics_options = {
        "heuristic_1_center": heuristic_1_center,
        "heuristic_2_reflection": heuristic_2_reflection,
        "heuristic_3_partition": heuristic_3_partition,
        "heuristic_combined_1_2": heuristic_combined_1_2,
        "heuristic_combined_1_3": heuristic_combined_1_3,
        "heuristic_combined_2_3": heuristic_combined_2_3,
        "heuristic_combined_1_2_3": heuristic_combined_1_2_3,
        "heuristic_combined_1_2_3_with_improve_score": heuristic_combined_1_2_3_with_improve_score
    }

    return heuristics_options["heuristic_combined_1_2_3_with_improve_score"](game, player)

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return
        board coordinates of best legal move before the time limit expires.
        This function only uses iterative deepening search
        and uses minimax with alpha-beta pruning. Return before time_left < 0 otherwise
        agent will forfeit the game due to timeout.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        remaining_legal_moves = game.get_legal_moves(game.active_player)
        no_legal_moves = (-1, -1)
        best_move = no_legal_moves
        if not remaining_legal_moves:
            return no_legal_moves

        # Use random IDS depth between 9 and 12
        depth = random.randint(9, 12)

        try:
            # Perform IDS
            while True:
                depth += 1
                _, best_move = self.alphabeta(game, depth)

                if self.time_left() <= 0.001:
                    return best_move

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Minimax search with alpha-beta pruning implementation
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Initialise variable for no legal moves
        no_legal_moves = (-1, -1)
        best_move = no_legal_moves
        best_utility = float('-inf') if maximizing_player else float('inf')
        current_player = game.active_player if maximizing_player else game.inactive_player
        remaining_legal_moves = game.get_legal_moves(game.active_player)

        # Recursion function termination conditions when legal moves exhausted or no plies left
        if not remaining_legal_moves:
            return game.utility(current_player), no_legal_moves
        elif depth == 0:
            return self.score(game, current_player), remaining_legal_moves[0]

        # Recursively alternate between Maximise and Minimise calculations for decrementing depths
        for move in remaining_legal_moves:
            # Obtain successor of current state by creating copy of board and applying a move.
            next_state = game.forecast_move(move)
            forecast_utility, _ = self.alphabeta(next_state, depth - 1, alpha, beta, not maximizing_player)

            if maximizing_player:
                if forecast_utility > best_utility:
                    best_utility, best_move = forecast_utility, move

                    # Prune next successor node if possible
                    if best_utility >= beta:
                        break
                    alpha = max(alpha, best_utility)
            else:
                if forecast_utility < best_utility:
                    best_utility, best_move = forecast_utility, move

                    # Prune next successor node if possible
                    if best_utility <= alpha:
                        break
                    beta = min(beta, best_utility)

        return best_utility, best_move
