from luxai2021.env.lux_env import LuxEnvironment, SaveReplayAndModelCallback
import numpy as np

class luxvectorEnv(gym.Wrapper):
    def __init__(self, env):
        """
        env input is the luxai gym env operator
        """
        super().__init__(env)
        self.env = env
    def reset(self):
        
        self.env.reset()
        return self.get_array_worker_cities()
        
    def step(self, action):
        
        next_state, reward, done, info = self.env.step(action)
        next_state = self.get_array_worker_cities()
        
        return next_state, reward, done, info

    def get_array_worker_cities(self):
        
        """
        Retrieve the map in a tensor format :
        map => (h, w, 12) tensor
        
        0 channel is the cities information
        1-2 channels is the units information
        3-5 is the ressources information
        
        """
        
        map = self.env.game.map

        w = map.width
        h = map.height

        array_cities = np.zeros((h, w, 1))
        array_units = np.zeros((h, w, 2)) # 2 channels for the units types

        array_ressource = np.zeros((h, w, 3)) ## 3 channels for all resosurces

        for y in range(map.height):
                row = map.get_row(y)
                for idx, cell in enumerate(row):
                    if cell.has_units():
                        unit = list(cell.units.values())[0]
                        if len(cell.units) == 1:
                            unit_str = '?'
                            if unit.type == Constants.UNIT_TYPES.CART:
                                array_units[y, idx, 0] += 1
                            elif unit.type == Constants.UNIT_TYPES.WORKER:
                                array_units[y, idx, 1] += 1

                            if unit.team == Constants.TEAM.A:
                                pass
                            elif unit.team == Constants.TEAM.B:
                                array_units[y, idx, :] = -array_units[y, idx, :] 
                            else:
                                pass

                        else:
                            unit_str = str(len(cell.units))

                            if unit.team == Constants.TEAM.A:
                                array_units[y, idx, :] = 2
                            elif unit.team == Constants.TEAM.B:
                                array_units[y, idx, :] = -2
                            else:
                                unit_str += "?"

                            map_str += unit_str
                    elif cell.has_resource():
                        if cell.resource.type == Constants.RESOURCE_TYPES.WOOD:
                            array_ressource[y, idx, 0] = 1
                        if cell.resource.type == Constants.RESOURCE_TYPES.COAL:
                            array_ressource[y, idx, 1] = 1
                        if cell.resource.type == Constants.RESOURCE_TYPES.URANIUM:
                            array_ressource[y, idx, 2] = 1
                    elif cell.is_city_tile():
                        map_str += "C"
                        if cell.city_tile.team == Constants.TEAM.A:
                            array_cities[y, idx, :] = 1
                        elif cell.city_tile.team == Constants.TEAM.B:
                            array_cities[y, idx, :] = -1
                        else:
                            pass
                    else:
                        pass
                pass
        return np.concatenate((array_cities, array_units, array_ressource), axis=-1)
