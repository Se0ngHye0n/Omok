import time


MAX_DEPTH = 4


def iterative_deepening(game, state, max_time= 10.0):
    start_time = time.time()
    best_move = None
    depth = 1
    player = game.player_turn(state)

    while time.time() - start_time < max_time:
        score, move = alpha_beta_search(game, state, depth, player, start_time, max_time)
        if move is not None:
            best_move = move
        depth += 1

    return best_move

def alpha_beta_search(game, state, depth, player, start_time, max_time):
    best_score = float('-inf')
    best_action = None
    alpha = float('-inf')
    beta = float('inf')

    for action in game.valid_loc(state):
        if time.time() - start_time > max_time:
            break

        next_state = game.state_update(state, action, player)
        score, _ = min_value(game, next_state, alpha, beta, depth - 1, player, start_time, max_time)

        if score > best_score:
            best_score = score
            best_action = action

        alpha = max(alpha, best_score)

    return best_score, best_action

def max_value(game, state, alpha, beta, depth, player, start_time, max_time):
    if time.time() - start_time > max_time:
        return game.evaluate(state, player), None

    if depth == 0 or game.is_terminal(state):
        return game.evaluate(state, player), None

    value = float('-inf')
    best_move = None

    for action in game.valid_loc(state):
        if time.time() - start_time > max_time:
            break

        next_state = game.state_update(state, action, player)
        score, _ = min_value(game, next_state, alpha, beta, depth - 1, player, start_time, max_time)

        if score > value:
            value = score
            best_move = action
        if value >= beta:
            return value, best_move
        alpha = max(alpha, value)

    return value, best_move

def min_value(game, state, alpha, beta, depth, player, start_time, max_time):
    if time.time() - start_time > max_time:
        return game.evaluate(state, player), None

    if depth == 0 or game.is_terminal(state):
        return game.evaluate(state, player), None

    opponent = game.opponent_turn(player)
    value = float('inf')
    best_move = None

    for action in game.valid_loc(state):
        if time.time() - start_time > max_time:
            break

        next_state = game.state_update(state, action, opponent)
        score, _ = max_value(game, next_state, alpha, beta, depth - 1, player, start_time, max_time)

        if score < value:
            value = score
            best_move = action
        if value <= alpha:
            return value, best_move
        beta = min(beta, value)

    return value, best_move
