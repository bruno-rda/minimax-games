# Negamax implementation inspired by: Pascal Pons's Connect4 implementation
# https://github.com/PascalPons/connect4

import math
from time import time
from game.game import Game

class Solver:
    def __init__(self, verbose=False, max_depth=math.inf):
        self.cache = dict()
        self.hit = 0
        self.node_count = 0
        self.verbose = verbose
        self.max_depth = max_depth
                
    def negamax(
        self, 
        game: Game, 
        alpha: int, 
        beta: int, 
        depth: int = 0
    ) -> int:
        
        self.node_count += 1
        
        if game.is_over():
            return game.compute_final_score()
        
        # If max depth is reached, return upper or lower bound
        if depth >= self.max_depth:
            return (alpha if game.turn % 2 else beta)
        
        # Check for immediate win
        immediate_win_score = game.evaluate_immediate_win()
        if immediate_win_score is not None:
            return immediate_win_score
        
        # Check for forced loss
        forced_lose_score = game.evaluate_forced_loss()
        if forced_lose_score is not None:
            return forced_lose_score
        
        # Compute upper bound since immediate win isn't possible
        # and lower bound since forced loss isn't possible
        upper_bound = game.get_upper_bound()
        lower_bound = game.get_lower_bound()
        
        # Retrieve cached bounds if possible
        key = game.get_key()
        if key is not None and key in self.cache:
            if self.cache[key] > game.max_score * 8:
                self.hit += 1
                lower_bound = self.cache[key] - game.max_score * 10
            else:
                self.hit += 1
                upper_bound = self.cache[key]
        
        # Adjust beta based on upper bound
        if beta > upper_bound:
            beta = upper_bound
            
        # Adjust alpha based on lower bound
        if alpha < lower_bound:
            alpha = lower_bound

        # Prune exploration if [alpha, beta] window is empty
        if alpha >= beta:
            return beta #+ 0.001
        
        for move in game.legal_moves():
            game.play_move(move)
            score = -self.negamax(game, -beta, -alpha, depth + 1)
            game.undo_move()

            # Prune exploration if score is greater than beta   
            if score >= beta:
                if key is not None:
                    self.cache[key] = score + game.max_score * 10
                return score

            # Reduce window for next exploration
            if score > alpha:
                alpha = score

        # Cache the upper bound
        if key is not None:
            self.cache[key] = alpha

        return alpha
    
    def get_best_move(self, game: Game):
        start_time = time()
        initial_node_count = self.node_count
        initial_hit_count = self.hit
        
        best_score = -math.inf
        best_move = None

        for move in game.legal_moves():
            self.node_count += 1

            if self.verbose:
                print(f'Move: {move}', end=' | ')

            game.play_move(move)
            score = -self.negamax(game, -game.max_score, game.max_score)
            game.undo_move()

            if self.verbose:
                print(f'Scored: {score}')

            if score > best_score:
                best_score = score
                best_move = move

        search_time = time() - start_time
        nodes_searched = self.node_count - initial_node_count 
        cache_hits = self.hit - initial_hit_count

        print(f'{nodes_searched} scenarios searched in {search_time:.6f} seconds')
        print(f'Cache hit rate: {cache_hits / nodes_searched * 100:.2f}%')

        return best_move