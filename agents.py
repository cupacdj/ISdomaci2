import random
import time
import math


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_action(self, state, max_depth):
        pass


class RandomAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    def get_chosen_action(self, state=None, max_depth=None, *args, **kwargs):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = None, None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = new_state.get_score(state.get_on_move_chr())
            if (best_score is None and best_action is None) or score > best_score:
                best_action = action
                best_score = score
        return best_action



class MaxNAgent(Agent):
    
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()

        if not actions:
            return None
            
        curr = state.get_on_move_ord()
        best_action = None
        best_score_list = [-math.inf for _ in range(state.get_num_of_players())]
        agent = MaxNAgent()
        for action in actions:
            successor_state = state.generate_successor_state(action)
            score_list = agent.max_n(successor_state, max_depth - 1)
            
            if score_list[curr] > best_score_list[curr]:
                best_score_list = score_list
                best_action = action

        return best_action
    
    
    def max_n(self, state, depth=None):
        
        if state.is_goal_state() or depth == 0:
            return self.get_score_list(state)
        
        num_players = state.get_num_of_players()
        best_score_list = [-math.inf for _ in range(num_players)]
        curr = state.get_on_move_ord()
        
        actions = state.get_legal_actions()
        
        if not actions:
            return self.get_score_list(state)
        
        for action in actions:
            successor_state = state.generate_successor_state(action)
            child_score_list = self.max_n(successor_state, depth - 1)
            
            if child_score_list[curr] > best_score_list[curr]:
                best_score_list = child_score_list
        
        return best_score_list
    
    
    def get_score_list(self, state):
            
        scores = state.get_scores()
        score_list = []
        
        for i in range(state.get_num_of_players()):
            player_char = chr(ord('A') + i)
            if player_char in scores:
                score_list.append(scores[player_char])
            else:
                score_list.append(0)
        
        return score_list
    
    
    
    
class MinimaxAgent(Agent):

    player = None
    enemy = None 

    def get_chosen_action(self, state, max_depth):
        import math, time
        time.sleep(0.5)

        actions = state.get_legal_actions()
        if not actions:
            return None

        if MinimaxAgent.player is None and MinimaxAgent.enemy is None:
            MinimaxAgent.player = state.get_on_move_ord()
            successor_state = state.generate_successor_state(actions[0])
            MinimaxAgent.enemy = successor_state.get_on_move_ord()

        is_max_player = (state.get_on_move_ord() == MinimaxAgent.player)

        def get_score(state):
            scores = state.get_scores()
            player_chr = chr(ord('A') + MinimaxAgent.player)
            enemy_chr = chr(ord('A') + MinimaxAgent.enemy)
            return scores.get(player_chr, 0) - scores.get(enemy_chr, 0)

        def minimax(state, depth, is_max):
            if state.is_goal_state() or depth == 0:
                return get_score(state)

            actions = state.get_legal_actions()
            if not actions:
                return get_score(state)

            if is_max:
                best_score = -math.inf
                for action in actions:
                    successor_state = state.generate_successor_state(action)
                    score = minimax(successor_state, depth - 1, False)
                    best_score = max(best_score, score)
                return best_score
            else:
                best_score = math.inf
                for action in actions:
                    successor_state = state.generate_successor_state(action)
                    score = minimax(successor_state, depth - 1, True)
                    best_score = min(best_score, score)
                return best_score


        best_action = None
        if is_max_player:
            best_score = -math.inf
            for action in actions:
                successor_state = state.generate_successor_state(action)
                score = minimax(successor_state, max_depth - 1, False) 
                if score > best_score:
                    best_score = score
                    best_action = action
        else:
            best_score = math.inf
            for action in actions:
                successor_state = state.generate_successor_state(action)
                score = minimax(successor_state, max_depth - 1, True)
                if score < best_score:
                    best_score = score
                    best_action = action

        return best_action

    
class MinimaxABAgent(Agent):

    player = None
    enemy = None 

    def get_chosen_action(self, state, max_depth):
        import math, time
        time.sleep(0.5)

        actions = state.get_legal_actions()
        if not actions:
            return None

        if MinimaxABAgent.player is None and MinimaxABAgent.enemy is None:
            MinimaxABAgent.player = state.get_on_move_ord()
            successor_state = state.generate_successor_state(actions[0])
            MinimaxABAgent.enemy = successor_state.get_on_move_ord()

        is_max_player = (state.get_on_move_ord() == MinimaxABAgent.player)

        def get_score(state):
            scores = state.get_scores()
            player_chr = chr(ord('A') + MinimaxABAgent.player)
            enemy_chr = chr(ord('A') + MinimaxABAgent.enemy)
            return scores.get(player_chr, 0) - scores.get(enemy_chr, 0)

        def minimax(state, depth, alpha, beta, is_max):
            if state.is_goal_state() or depth == 0:
                return get_score(state)

            actions = state.get_legal_actions()
            if not actions:
                return get_score(state)

            if is_max:
                value = -math.inf
                for action in actions:
                    successor_state = state.generate_successor_state(action)
                    score = minimax(successor_state, depth - 1, alpha, beta, False)
                    value = max(value, score)
                    alpha = max(alpha, value)
                    if beta <= alpha: 
                        break
                return value
            else:
                value = math.inf
                for action in actions:
                    successor_state = state.generate_successor_state(action)
                    score = minimax(successor_state, depth - 1, alpha, beta, True)
                    value = min(value, score)
                    beta = min(beta, value)
                    if beta <= alpha: 
                        break
                return value

        best_action = None
        alpha, beta = -math.inf, math.inf
        if is_max_player:
            best_score = -math.inf
            for action in actions:
                successor_state = state.generate_successor_state(action)
                score = minimax(successor_state, max_depth - 1, alpha, beta, False)
                if score > best_score:
                    best_score = score
                    best_action = action
                alpha = max(alpha, best_score)
        else:
            best_score = math.inf           
            for action in actions:
                successor_state = state.generate_successor_state(action)
                score = minimax(successor_state, max_depth - 1, alpha, beta, True)
                if score < best_score:
                    best_score = score
                    best_action = action
                beta = min(beta, best_score)

        return best_action
