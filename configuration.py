from multiprocessing import set_start_method
from os import path
from typing import Type
from typing_extensions import Self

class PlotterConfiguration():
    properties = ['input_path']

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
            for attr in self.properties:
                # Invoke the setter on each property
                setattr(self, attr, getattr(self, f'_{attr}'))
        except Exception as e:
            if not quiet:
                print('Encountered an exception during validation:')
                print(type(e))
            return False, e

    def __str__(self) -> str:
        return \
f"""{{
    input_path: {self.input_path}
}}
"""
        # return 'bruh'

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