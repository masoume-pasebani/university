from collections import deque
import heapq

import board

import params
import colors

class Agent:
    def __init__(self, board):
        self.position = board.get_agent_pos()
        self.current_state = board.get_current_state()
        self.goal_pos = board.get_goal_pos()

    def get_position(self):
        return self.position

    def set_position(self, position, board):
        self.position = position
        board.set_agent_pos(position)
        board.update_board(self.current_state)

    def percept(self, board):
        # perception :
        # sets the current state
        # Use get_current_state function to get the maze matrix. - make your state
        self.current_state = board.get_current_state()
        self.goal_pos = board.get_goal_pos()

    def move(self, direction):
        # make your next move based on your perception
        # check if the move destination is not blocked
        # if not blocked , move to destination - set new position
        # something like :
        current_pos = self.get_position()
        x, y = current_pos[0], current_pos[1]
        board.colorize(x, y, colors.red)

        # then move to destination - set new position
        # something like :
        self.set_position(self.get_position() + direction)

        pass

    def get_actions(self, pos):
        current_x, current_y = pos
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        actions = map(lambda x: (current_x + x[0], current_y + x[1]), directions)
        valid_actions = filter(
            lambda pos: pos[0] >= 0 and pos[1] >= 0
                        and pos[0] < params.cols and pos[1] < params.rows
                and not self.current_state[pos[0]][pos[1]].is_blocked(),
            actions
        )

        # returns a list of valid actions
        return valid_actions

    def bfs(self, environment):
        self.percept(environment)

        initial = (self.position, None)
        o_list = deque([initial])
        c_list = set()
        solution = None

        while len(o_list) > 0:
            curr_node = o_list.popleft()
            c_list.add(curr_node[0])

            x, y = curr_node[0]
            if self.current_state[x][y].is_goal():
                solution = curr_node
                break

            for action in self.get_actions((x, y)):
                if action not in c_list:
                    o_list.append((action, curr_node))

        if solution is not None:
            self.show_solution_bfs(solution)

    def dfs(self, environment):
        self.percept(environment)
        
        initial = (self.position, None)
        o_list = [initial]
        c_list = set()
        solution = None

        while len(o_list) > 0:
            curr_node = o_list.pop()
            c_list.add(curr_node[0])

            x, y = curr_node[0]
            if self.current_state[x][y].is_goal():
                solution = curr_node
                break

            for action in self.get_actions((x, y)):
                if action not in c_list:
                    o_list.append((action, curr_node))

        if solution is not None:
            self.show_solution_dfs(solution)

    def a_star(self, environment):
        self.percept(environment)
 
        initial = (0, 0, self.position, None) 
        o_list = [initial]
        c_list = {}
        solution = None

        while len(o_list) > 0:
            curr_node = heapq.heappop(o_list)

            x, y = curr_node[2]
            if self.current_state[x][y].is_goal():
                solution = curr_node
                break

            for action in self.get_actions((x, y)):
                current_g = curr_node[1]
                new_g = current_g + 1
                h = self.heuristic(curr_node)

                if action not in c_list or new_g + h < c_list[action][0]:
                    new_node = (new_g + h, new_g, action, curr_node)
                    heapq.heappush(o_list, new_node)
                    c_list[action] = new_node

        if solution is not None:
            self.show_solution(solution, a_star = True)

    def show_solution(self, starting_solution_node, a_star = False):
        current_solution_node = starting_solution_node

        while current_solution_node is not None:
            current_solution_node = current_solution_node[2:]

            node_x, node_y = current_solution_node[0]

            current_tile_of_node = self.current_state[node_x][node_y]
            current_tile_of_node.set_color(colors.green)

            current_solution_node = current_solution_node[1]

    def show_solution_dfs(self, start_solution_node):
        current_node = start_solution_node

        while current_node is not None:
            current_node = current_node

            node_x, node_y = current_node[0]

            current_tile_of_node = self.current_state[node_x][node_y]
            current_tile_of_node.set_color(colors.red)

            current_node = current_node[1]

    def show_solution_bfs(self, start_solution_node):
        current_node = start_solution_node

        while current_node is not None:
            current_node = current_node

            node_x, node_y = current_node[0]

            current_tile_of_node = self.current_state[node_x][node_y]
            current_tile_of_node.set_color(colors.blue)

            current_node = current_node[1]
            
    
    @staticmethod
    def taxicab_distance(p1: tuple, p2: tuple):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def heuristic(self, node: tuple):
        return Agent.taxicab_distance(node[2], self.goal_pos)
