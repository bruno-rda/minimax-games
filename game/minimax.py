import math
from time import time
from game.game import Game

def cache(func):
    def wrapper(*args, **kwargs):
        key = args[0].get_key()

        if key in wrapper.cache:
            wrapper.hit += 1
            return wrapper.cache[key]

        wrapper.miss += 1
        res = func(*args, **kwargs)
        wrapper.cache[key] = res

        wrapper.count = len(wrapper.cache.keys())
        return res

    wrapper.count = 0
    wrapper.cache = dict()
    wrapper.hit, wrapper.miss = 0, 0
    return wrapper


@cache
def minimax(
    game: Game, 
    depth=0, 
    max_depth=math.inf
) -> int:

    if game.is_over() or depth > max_depth:
        return game.compute_final_score()

    if not (game.turn % 2):
        best_score = -math.inf

        for move in game.legal_moves():
            game.play_move(move)
            score = minimax(game, depth + 1, max_depth)
            game.undo_move()

            best_score = max(best_score, score)
    else:
        best_score = math.inf

        for move in game.legal_moves():
            game.play_move(move)
            score = minimax(game, depth + 1, max_depth)
            game.undo_move()

            best_score = min(best_score, score)

    return best_score


def state_counter(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        return func(*args, **kwargs)

    wrapper.count = 0
    return wrapper


@state_counter
def minimax_ab(
    game: Game, 
    alpha=-math.inf, 
    beta=math.inf,
    depth=0,
    max_depth=math.inf
) -> int:

    if game.is_over() or depth > max_depth:
        return game.compute_final_score()

    if not (game.turn % 2):
        best_score = -math.inf

        for move in game.legal_moves():
            game.play_move(move)
            score = minimax_ab(game, alpha, beta, depth + 1, max_depth)
            game.undo_move()

            best_score = max(best_score, score)
            
            alpha = max(alpha, score)
            if beta <= alpha:
                break
    else:
        best_score = math.inf

        for move in game.legal_moves():
            game.play_move(move)
            score = minimax_ab(game, alpha, beta, depth + 1, max_depth)
            game.undo_move()

            best_score = min(best_score, score)
            
            beta = min(beta, score)
            if beta <= alpha:
                break

    return best_score


def get_best_move(
    game: Game, 
    ab=False,
    verbose=False,
    max_depth=math.inf
) -> int:
    minimax_ = minimax_ab if ab else minimax

    t0 = time()
    c0 = minimax_.count

    mult = 1 if not (game.turn % 2) else -1

    best_score = -math.inf
    best_move = -1

    for move in game.legal_moves():
        if verbose:
            print(f'Move: {move}', end=' | ')

        game.play_move(move)
        score = minimax_(game, depth=1, max_depth=max_depth)
        game.undo_move()

        if verbose:
            print(f'Scored: {mult * score}')

        if mult * score > best_score:
            best_score = mult * score
            best_move = move

    print(
        f'{minimax_.count - c0} scenarios'
        f' searched in {time() - t0:.6f} seconds'
    )

    return best_move


def get_cache_stats():
    return minimax.count, minimax.hit, minimax.miss


def clear_cache():
    minimax.cache.clear()
    minimax.count = 0
    minimax.hit = 0
    minimax.miss = 0
