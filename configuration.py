from multiprocessing import set_start_method
from os import path
from typing import Type
from typing_extensions import Self
import pprint
pp = pprint.PrettyPrinter(indent=2)

class PlotterConfiguration():
    def __init__(self):
        self._input_path: str = 'data/out.png'

        self.tile_size: float = 0.25
        self.z_high: float = 19
        self.z_low: float = 13
        self.x = [50, 220]
        self.y = [30, 220]
        self.horizontal_move_force: int = 500
        self.vertical_move_force: int = 200
        self.validate()

    def validate(self, quiet=False) -> tuple[bool, Exception]:
        try:
            for key, value in self.__dict__.items():
                # Invoke the setter on each property
                if key.startswith('_'):
                    setattr(self, key.lstrip('_'), value)
        except Exception as e:
            if not quiet:
                print('Encountered an exception during validation:')
                print(type(e))
            # raise e # for debug
            return False, e

    def __str__(self) -> str:
        return pp.pformat(self.__dict__)
                
    @property
    def input_path(self):
        print('getter')
        return self._input_path

    @input_path.setter
    def input_path(self, fp: str):
        if type(fp) != str: raise TypeError
        
        if not path.exists(fp):
            print(f'file not found: {fp}\nconfiguration unchanged')
            raise FileNotFoundError

        print(f'Input file set to {fp}')
        self._input_path = fp

if __name__ == '__main__':
    a = PlotterConfiguration()
    print(a)