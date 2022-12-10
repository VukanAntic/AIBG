import math
from builtins import round
import heapq as hq
import math


INF = float("inf")


class Parser:

    def __init__(self, player_id):
        self.player_id = player_id
        self.players = []
        self.current_pattern = 1
        self.attack = 150
        self.hp = 1000
        self.xp = 0
        self.target_times = []
        self.boss_tiles = []
        self.attack_fields = []

        for i in range(-4, 5):
            for j in range(-4 - min(i,0), 5 - max(i,0)):
                self.target_times.append((i, j))

        for i in range(-1, 2):
            for j in range(-1 - min(i, 0), 2 - max(i, 0)):
                self.boss_tiles.append((i, j))
        #self.target_tiles = [(x,y) for x in range() for y in range()]

    # def makeField(stafield_size):
    #     field = []
    #     for i in range(-field_size, field_size+1):
    #         for j in range(-field_size - min(i, 0), field_size + 1 - max(i, 0)):
    #             field.append((i,j))
    #     return field


    def findClosesAttack(self, pos):

        min_dist = INF
        min_tile = None
        for tile in self.boss_tiles:
            dist = (abs(pos[0] - tile[0]) + abs(pos[1] - tile[1]))
            if dist < min_dist:
                min_dist = dist
                min_tile = tile
        return min_tile


    def getBestMove(self, state):
        #print(state)
        game_map = state["map"]
        block_matrix = game_map["tiles"]

        #players = {p["playerIdx"]: (p["q"], p["r"]) for p in state["scoreBoard"]["players"]}
        all_players = {}

        for player in state["scoreBoard"]["players"]:
            all_players[player["playerIdx"]] = (player["q"], player["r"])


        our_player = all_players[self.player_id]
        all_players.pop(self.player_id)
        self.players = list(all_players.values())
        #list_all_players = list(all_players.values())

        pl_ar_size = 4
        self.attack_fields = list()

        for p in self.players:
            for i in range( -pl_ar_size,   pl_ar_size + 1):
                for j in range( -pl_ar_size - min(i, 0), pl_ar_size + 1 - max(i, 0)):
                    #print(self.players)
                    self.attack_fields.append((p[0] + i, p[1] + j))


        #print("Ovo je neki ispis za self.players")
        #print(self.players)


        current_location = our_player
        #current_location = (our_player["q"], our_player["r"])
        #self.players.remove(current_location)
       # print(state["scoreBoard"]["players"])

        block_dict = self.block_to_dict(block_matrix)
        graph = self.create_graph(block_dict)
        parent, result = self.dijkstra(graph, current_location)

        min_val = INF
        min_tile = None
        for tile in self.target_times:
            val = result[tile]
            if min_val > val:
                min_tile = tile
                min_val = val

        if parent[min_tile] == None:
            closest_attacker = self.findClosesAttack(current_location)
            return "attack," +  str(closest_attacker[0]) + "," + str(closest_attacker[1])

        while parent[min_tile] != current_location:
            min_tile = parent[min_tile]

        if block_dict[min_tile]["tileType"] == "FULL":
            return "attack" + "," + str(min_tile[0]) + "," + str(min_tile[1])
        else:
            return "move" + "," + str(min_tile[0]) + "," + str(min_tile[1])



    def block_to_dict(self, block_matrix):
        block_dict = {}
        for block_arr in block_matrix:
            for block in block_arr:
                block_dict[(block["q"],block["r"])] = \
                    {"entity": block["entity"],"tileType": block["tileType"]}
        return block_dict

    def get_block_cost(self,block):
        cost = 0
        type_of_block = block["entity"]["type"]
        if type_of_block == "EMPTY":
            cost = 1
        elif type_of_block == "ASTEROID":
            #  need cost times of turns to destroy asteroid
            ast_hp = block["entity"]["health"]
            cost = math.ceil(ast_hp / self.attack)
        elif type_of_block == "BLACKHOLE" or type_of_block == "WORMHOLE":
            # need 3 turns to get out of the blackhole
            cost = INF
        #print(cost)
        return cost

    def create_graph(self, block_dict):

        # fix
        graph_matrix = {}

        for i in range(-14, 15):
            for j in range(-14 - min(i,0), 15 - max(i,0)):
                graph_matrix[(i, j)] = []
                for k in range(-1,2):
                    for l in range(-1,2):
                        if abs(i+k)<=14 and abs(j+l)<=14 and abs(i+k+j+l)<=14 and not(k==l):
                            #if i + k == -7 and j + l == -2:
                               # print("Ovo je unutar if-a")
                               # print(self.players)
                            if (i + k, j + l) in self.players:
                                #print((i + k, j + l))
                                cost = INF
                            elif (i + k, j + l) in self.attack_fields:
                                cost = 5
                            else:
                                cost = self.get_block_cost(block_dict[(i + k, j + l)])
                            graph_matrix[(i, j)].append(((i+k,j+l),cost))
                            #print(cost)

        return graph_matrix

    def dijkstra(self, graph, player_position):

        # player_position is (x, y)
        shortest_paths = {}
        parent = {}
        for key in graph.keys():
            shortest_paths[key] = INF
            parent[key] = None

        shortest_paths[player_position] = 0
        parent[player_position] = None

        pq = []
        hq.heappush(pq, (0, player_position))

        while pq:
            dist, current_element = hq.heappop(pq)

            for neigh, neigh_value in graph[current_element]:
                if shortest_paths[current_element] + neigh_value < shortest_paths[neigh]:
                    shortest_paths[neigh] = shortest_paths[current_element] + neigh_value
                    hq.heappush(pq, (shortest_paths[neigh], neigh))
                    parent[neigh] = current_element

        return parent, shortest_paths



        #dist = 0
        #pq = []
        #hq.heappush(pq, (dist, source))

        #while pq:
        #    d, u = hq.heappop(pq)
        #    for v, w in adj[u]:
        #        if dist[u] + w < dist[v]:
        #            dist[v] = dist[u] + w
        #            hq.heappush(pq, (dist[v], v))


