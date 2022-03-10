# TODO validate func setting all the members to themselves,
# thus calling setters which have validation code
from os import path

class PlotterConfiguration():
    _input_path: str = None
    tile_size: float = 0.25
    # TODO rise_height
    z_high: float = 19

    z_low: float = 13
    x = [50, 220]
    y = [30, 220]
    horizontal_move_force: int = 500
    vertical_move_force: int = 200

    @property
    def input_path(self):
        return self._input_path

    @input_path.setter
    def input_path(self, fp: str):
        if type(fp) != str: raise TypeError
        
        if not path.exists(fp):
            print(f'file not found: {fp}\nconfiguration unchanged')
            raise FileNotFoundError

        print(f'Input file set to {fp}')
        self._input_path = fp