#!/usr/bin/env python3
import random
import numpy as np

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

# to run the program: python main.py settings.yml

class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """
        alpha_top = -9999
        beta_top = 9999

        # create children node
        initial_tree_node.compute_and_get_children()

        depth_limit = 4  #depth limit in minimax search

        best_score = -9999
        best_value, best_value_node = self.minimax(initial_tree_node, alpha_top, beta_top, depth_limit)
        #print(best_value)

        node_with_best_value = best_value_node

        for i in range(depth_limit-1):
            node_with_best_value = node_with_best_value.parent
        best_move = node_with_best_value.move

        #random_move = random.randrange(5)
        #print("Heuristic value: ", self.heuristic(best_value_node))
        #string = ACTION_TO_STR[best_move]
        print("Best move:", ACTION_TO_STR[best_move])
        return ACTION_TO_STR[best_move]

    def minimax(self, node: Node, alpha, beta, depth_limit):
        #print("Current depth: ", node.depth)
        if node.depth == depth_limit: 
            #print("arrive at leaf node")
            return self.heuristic_rob(node), node

        alpha = -999
        beta = 999

        if not (node.state.get_player == 0): #MIN's turn
            best_value = 999
            try:
                best_value_node = node.children[0]  # should assign a leaf node here
            except:
                best_value_node = node
            children = node.compute_and_get_children()
            for i in node.children:
                (value,node) = self.minimax(i, alpha, beta, depth_limit)  #value_node is a list {Value, Node class}
                #print("value returned from MINIMAX(MIN's Turn): ",value)
                if value < best_value:
                    best_value_node = node   # best_value_node is a node
                    best_value = value

                beta = min(best_value, beta)
                if beta <= alpha:
                    break
            #return min_value

        else:  # MAX's turn
            best_value = -999
            try:
                best_value_node = node.children[0]  # should assign a leaf node here
            except:
                best_value_node = node

            children = node.compute_and_get_children()
            for i in node.children:
                (value,node) = self.minimax(i, alpha, beta, depth_limit)
                
                if value > best_value:
                    best_value_node = node
                    best_value = value

                alpha = max(best_value, alpha)
                if beta <= alpha:
                     break
        '''
        node = best_value_node
        for i in range(depth_limit-1):
            node = node.parent
        '''
        return best_value, best_value_node;  # this is the {value,node} returned by MINIMAX

    def heuristic(self, node: Node):  
        # THis heuristic calculates the distance between the hook pos and the avergae postion of the fishes

        hook_pos = node.state.get_hook_positions() # return: dict of 2-tuples with (x, y) values of each player's hook
        fish_pos = node.state.get_fish_positions()
        #print(fish_pos)
        #print("Remaining number of fishes: ", len(fish_pos.keys()))
        #print("fish position at:" , fish_pos()) # maybe here can compute the avergae of fish
        #print(np.average(fish_pos().values()))
        x_sum = 0
        y_sum = 0
        for i in fish_pos.keys():
            x_sum = x_sum + fish_pos[i][0]
            y_sum = y_sum + fish_pos[i][1]
        average_xy = (x_sum/len(fish_pos.keys()), y_sum/len(fish_pos)) #to get the average position of all the fishes
        #print("average fish pos: ", average_xy)
        #print("My hook position: ", hook_pos[0])
        dist = np.sqrt((hook_pos[0][0] - average_xy[0])**2 + (hook_pos[0][1] - average_xy[1])**2)
        value = -dist # we want to stay close to the fishes  ~10, 20 , 30
        #print("heuristic Value:", value)
        #hook_pos()[0]
        return (value)
    
    def heuristic_rob(self, node:Node):
        # the purpose is to rob the closest fish from the opponent
        hook_pos = node.state.get_hook_positions() 
        fish_pos = node.state.get_fish_positions()
        #print("fish position: ",fish_pos)
        #print("hook position: ",hook_pos)
        MINs_distance = {} # init dict
        MAXs_distance = {} # init dict

        for d in fish_pos.keys():
            MINs_distance[d] = self.L1_distance(fish_pos[d], hook_pos[1])
            #print("Fish",d, "distance: ",MINs_distance[d])
            MAXs_distance[d] = self.L1_distance(fish_pos[d], hook_pos[0])
        #print("MIN's distance: ",MINs_distance)  
        #print("MAX's distance: ",MAXs_distance)
        #print(fish_pos.keys())
        target_fish = None
        dist_ahead_max = 0  # only when we are closer to the fish than our opponent, we set it as our target
        for i in MAXs_distance.keys():
            dist_ahead = MAXs_distance[i] - MINs_distance[i]
            if dist_ahead  < 0 and dist_ahead < dist_ahead_max : # find the closest possible fish as target
                target_fish = i
                dist_ahead_max = dist_ahead

        if target_fish == None:
            return -999
        
        target_fish_pos = fish_pos[target_fish] # a tuple (X,Y) 

        distance = self.L1_distance(target_fish_pos, hook_pos[0])
        value = -distance
        #print("Target fish is: ", target_fish)
        return value 


    def L1_distance(self, fish_pos, hook_pos):
        '''
        fish_pos: tuple of (X,Y)
        hook_pos: tuple
        '''
        y = abs(fish_pos[1] - hook_pos[1])
        delta_x = abs(fish_pos[0] - hook_pos[0])
        x = min(delta_x, 20 - delta_x)
        #print("L1 distance between: ",fish_pos, hook_pos, "is ",x+y)
        return x + y
