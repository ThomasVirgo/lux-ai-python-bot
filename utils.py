from lux.game_map import Position
import math

def create_citytile_list(player):
    citytiles = []
    for k, city in player.cities.items():
                        for city_tile in city.citytiles:
                            citytiles.append(city_tile)
    return citytiles

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
                return circular_path[0]
            else:
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


def find_build_location(player, map):
    first_city_tile = create_citytile_list(player)[0]
    available_cells = []
    for i in range(first_city_tile.pos.x-1, first_city_tile.pos.x+2):
        for j in range(first_city_tile.pos.y-1, first_city_tile.pos.y+2):
            if Position(i,j).equals(first_city_tile.pos): continue
            cell = map.get_cell(i,j)
            if not cell.has_resource():
                available_cells.append(cell)
    sqaure = []
    for current_cell in available_cells:
        adjacent_cells = []
        for other_cell in available_cells:
            if current_cell.pos.equals(other_cell.pos): continue
            if abs(current_cell.pos.x - other_cell.pos.x) <= 1 and abs(current_cell.pos.y - other_cell.pos.y) <= 1:
                adjacent_cells.append(other_cell)
        if len(adjacent_cells) == 2:
            square =  adjacent_cells
    for cell in square:
        if not cell.citytile:
            return cell
    return None

def get_new_coordinate_given_action(action):
    pass