import sys

from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES


class Agent:
    def __init__(self, game_data):
        self.game = Game(game_data)
        opponent_index = 1 if self.game.id == 0 else 0
        self.player = self.game.players[self.game.id]
        self.opponent = self.game.players[opponent_index]

    def get_actions(self):
        actions = []
        resource_tiles = self.get_resource_tiles()
        player_city_tiles = self.get_player_city_tiles()

        for unit in self.player.units:
            if unit.cooldown == 0:
                if unit.get_cargo_space_left() > 0:
                    nearest_wood = sorted(resource_tiles["wood"], key=unit.pos.distance_to)[0]
                    actions.append(unit.move(unit.pos.direction_to(nearest_wood)))
                else:
                    if len(player_city_tiles) > 0:
                        nearest_city = sorted(player_city_tiles, key=unit.pos.distance_to)[0]
                        actions.append(unit.move(unit.pos.direction_to(nearest_city)))

        return actions

    def take_turn(self, turn_data=None):
        if turn_data:
            self.game.update(turn_data)
        actions = self.get_actions()
        self.game.submit_actions(actions)
        self.game.end_turn()

    def get_resource_tiles(self):
        resources = {
            "wood": [],
            "coal": [],
            "uranium": []
        }
        for row in self.game.map.map:
            for cell in row:
                if cell.has_resource():
                    resources[cell.resource.type].append(cell.pos)
        return resources

    def get_player_city_tiles(self):
        city_tiles = []
        for row in self.game.map.map:
            for cell in row:
                if cell.city_tile and cell.city_tile.team == self.player.team:
                    city_tiles.append(cell.pos)
        return city_tiles

# Kaggle function
def agent(observation, configuration):
    if not hasattr(agent, "instance"):
        agent.instance = Agent(observation["updates"])
    else:
        agent.instance.game.update(observation["updates"])
    instance = agent.instance
    (player_index, opponent_index) = (0, 1) if observation["player"] == 0 else (1, 0)
    instance.player = instance.game.players[player_index]
    instance.opponent = instance.game.players[opponent_index]
    actions = agent.instance.get_actions()
    print(f"step {observation['step']}: {actions=}", file=sys.stderr)
    return actions
