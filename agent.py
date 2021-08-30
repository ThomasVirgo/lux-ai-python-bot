import math, sys
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate
from utils import create_circular_path, determine_current_move_target, get_closest_citytile, is_collision_going_to_happen

DIRECTIONS = Constants.DIRECTIONS
game_state = None


def agent(observation, configuration):
    global game_state

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])
    
    actions = []

    ### AI Code goes down here! ### 
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height
    city_tile_goal = 4

    resource_tiles: list[Cell] = []
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if cell.has_resource():
                resource_tiles.append(cell)

    ### utility functions ###
    def total_city_tiles():
        total = 0
        for k, city in player.cities.items():
            total += len(city.citytiles)
        return total
    ### end of utility functions

    # iterate over all our units and do something with them
    new_unit_positions = []
    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            # if the unit can build a city tile then do so as long as not above city tile goal
            if unit.can_build(game_state.map) and total_city_tiles() < city_tile_goal:
                actions.append(unit.build_city())
                break

            closest_dist = math.inf
            closest_resource_tile = None
            # if unit.get_cargo_space_left() > 0:
            # if the unit is a worker and we have space in cargo, lets find the nearest resource tile and try to mine it
            for resource_tile in resource_tiles:
                # only collect wood to begin with
                if resource_tile.resource.type == Constants.RESOURCE_TYPES.COAL and not player.researched_coal(): continue
                if resource_tile.resource.type == Constants.RESOURCE_TYPES.URANIUM and not player.researched_uranium(): continue
                dist = resource_tile.pos.distance_to(unit.pos)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_resource_tile = resource_tile
            if closest_resource_tile is not None and len(player.cities.items()):
                closest_city_tile = get_closest_citytile(player, unit)
                path = create_circular_path(closest_city_tile.pos, closest_resource_tile.pos)
                target_pos = determine_current_move_target(unit.pos, path, closest_city_tile.pos, closest_resource_tile.pos)

                if target_pos and not is_collision_going_to_happen(new_unit_positions, target_pos, player.units):
                    new_unit_positions.append(target_pos)
                    actions.append(unit.move(unit.pos.direction_to(target_pos)))
                # actions.append(unit.move(unit.pos.direction_to(closest_resource_tile.pos)))
            # else:
                # if unit is a worker and there is no cargo space left, and we have cities, lets return to them
                # if len(player.cities) > 0:
                #     closest_dist = math.inf
                #     closest_city_tile = None
                #     for k, city in player.cities.items():
                #         for city_tile in city.citytiles:
                #             dist = city_tile.pos.distance_to(unit.pos)
                #             if dist < closest_dist:
                #                 closest_dist = dist
                #                 closest_city_tile = city_tile
                #     if closest_city_tile is not None:
                #         move_dir = unit.pos.direction_to(closest_city_tile.pos)
                #         actions.append(unit.move(move_dir))

    # iterate over all our citytiles and do something with them

    for k, city in player.cities.items():
        for city_tile in city.citytiles:
            if city_tile.can_act() and len(player.units) < total_city_tiles():
                actions.append(city_tile.build_worker())
    return actions
