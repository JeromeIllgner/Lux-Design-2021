import math, sys

from typing import List

from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate

DIRECTIONS = Constants.DIRECTIONS
game_state = None


def setup_game(observation):
    ## Don't Edit
    global game_state
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])


def days_until_night(observation):
    day = 30 - observation["step"] % 40
    return max(day, 0)


def get_resource_tiles(map):
    resource_tiles = []
    for y in range(map.height):
        for x in range(map.width):
            cell = map.get_cell(x,y)
            if cell.has_resource():
                resource_tiles.append(cell)
    return resource_tiles


def get_closest_available_resource_tile(unit, resource_tiles, has_researched_coal, has_researched_uranium):
    min_distance = math.inf
    closest_resource_tile = None
    for tile in resource_tiles:
        if tile.resource.type == Constants.RESOURCE_TYPES.COAL and not has_researched_coal:
            continue
        if tile.resource.type == Constants.RESOURCE_TYPES.URANIUM and not has_researched_uranium:
            continue

        distance = tile.pos.distance_to(unit.pos)
        if distance < min_distance:
            min_distance = distance
            closest_resource_tile = tile

    return closest_resource_tile


def get_nearest_city(unit, cities):
    nearest_city_tile = None
    min_distance = math.inf
    for key, city in cities.items():
        for city_tile in city.citytiles:
            distance = city_tile.pos.distance_to(unit.pos)
            if distance < min_distance:
                min_distance = distance
                nearest_city_tile = city_tile
    return nearest_city_tile


def agent(observation, configuration):
    global game_state
    setup_game(observation)

    actions = []
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]

    resource_tiles: List[Cell] = get_resource_tiles(game_state.map)

    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            if unit.get_cargo_space_left() > 0:
                closest_resource_tile = get_closest_available_resource_tile(unit, resource_tiles, player.researched_coal(), player.researched_uranium())

                if closest_resource_tile is not None:
                    actions.append(unit.move(unit.pos.direction_to(closest_resource_tile.pos)))
            else:
                nearest_city_tile = get_nearest_city(unit, player.cities)
                if nearest_city_tile is not None:
                    move_dir = unit.pos.direction_to(nearest_city_tile.pos)
                    actions.append(unit.move(move_dir))

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))
    
    return actions
