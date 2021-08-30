from lux.game_map import Position
import math

def create_circular_path(citytile_position, target_position):
        #edge case that city tile and target have the same x co-ordinate
        if citytile_position.y == target_position.y:
            pos_1 = Position(citytile_position.x, citytile_position.y)
            pos_2 = Position(citytile_position.x, citytile_position.y+1)
            pos_3 = Position(target_position.x, citytile_position.y+1)
            pos_4 = Position(target_position.x, target_position.y)
            return [pos_1, pos_2, pos_3, pos_4]

        #edge case that city tile and target have same y co-ordinate
        if citytile_position.x == target_position.x:
            pos_1 = Position(citytile_position.x, citytile_position.y)
            pos_2 = Position(citytile_position.x+1, citytile_position.y)
            pos_3 = Position(citytile_position.x+1, target_position.y)
            pos_4 = Position(target_position.x, target_position.y)
            return [pos_1, pos_2, pos_3, pos_4]

        pos_1 = Position(citytile_position.x, citytile_position.y)
        pos_2 = Position(target_position.x, citytile_position.y)
        pos_3 = Position(target_position.x, target_position.y)
        pos_4 = Position(citytile_position.x, target_position.y)
        return [pos_1, pos_2, pos_3, pos_4]

def determine_current_move_target(unit_position, circular_path, citytile_position, target_position):
    '''function to work out which position the unit should be heading towards'''
    # on exact position
    positions_unit_is_between = []
    for idx, pos in enumerate(circular_path):
        if unit_position.equals(pos):
            if idx == 3:
                print(circular_path[0].x, circular_path[0].y)
                return circular_path[0]
            else:
                print(circular_path[idx+1].x, circular_path[idx+1].y)
                return circular_path[idx+1]
        if unit_position.x == pos.x or unit_position.y == pos.y:
            positions_unit_is_between.append({
                "index": idx,
                "position": pos
            })
    try:
        if positions_unit_is_between[1]['index'] == 3:
            return positions_unit_is_between[0]['position']
        else:
            return positions_unit_is_between[1]['position']
    except Exception as e:
        print(e)
        return citytile_position

def get_closest_citytile(player, unit):
    closest_dist = math.inf
    closest_city_tile = None
    for k, city in player.cities.items():
                        for city_tile in city.citytiles:
                            dist = city_tile.pos.distance_to(unit.pos)
                            if dist < closest_dist:
                                closest_dist = dist
                                closest_city_tile = city_tile
                        return closest_city_tile

def is_collision_going_to_happen(new_unit_positions, target_position, units):
    for pos in new_unit_positions:
        if pos.equals(target_position):
            return True
    for unit in units:
        if target_position.equals(unit.pos):
            return True
    return False


def is_square_possible():
    pass