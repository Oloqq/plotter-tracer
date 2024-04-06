from multiprocessing import set_start_method
from os import path
from typing import Type
from typing_extensions import Self
import pprint
pp = pprint.PrettyPrinter(indent=2)


class PlotterConfiguration():
    def pen(self):
        self._input_path: str = 'data/out.png'
        # TODO make those properties, remake z_high into rise_height
        self._tile_size: float = 0.25
        self._z_high: float = 19
        self._z_low: float = 13
        self._x = [50, 220]
        self._y = [30, 220]
        self._horizontal_move_force: int = 500
        self._vertical_move_force: int = 200

    def mill(self):
        self._input_path: str = 'data/out.png'
        # TODO make those properties, remake z_high into rise_height
        self._tile_size: float = 0.25
        self._z_high: float = 30
        self._z_low: float = 27
        self._x = [20, 160]
        self._y = [60, 100]
        self._horizontal_move_force: int = 70
        self._vertical_move_force: int = 200

    def __init__(self):
        # self.pen()
        self.mill()
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
        return self._input_path

    @input_path.setter
    def input_path(self, fp: str):
        if type(fp) != str:
            raise TypeError

        if not path.exists(fp):
            print(f'file not found: {fp}\nconfiguration unchanged')
            raise FileNotFoundError

        print(f'Input file set to {fp}')
        self._input_path = fp

    @property
    def tile_size(self):
        return self._tile_size

    @tile_size.setter
    def tile_size(self, data: any):
        self._tile_size = data

    @property
    def z_high(self):
        return self._z_high

    @z_high.setter
    def z_high(self, data: any):
        self._z_high = data

    @property
    def z_low(self):
        return self._z_low

    @z_low.setter
    def z_low(self, data: any):
        self._z_low = data

    @property
    def x(self):
        return self._x

    @x.setter
    def self(self, data: any):
        self._x = data

    @property
    def y(self):
        return self._y

    @y.setter
    def self(self, data: any):
        self._y = data

    @property
    def horizontal_move_force(self):
        return self._horizontal_move_force

    @horizontal_move_force.setter
    def horizontal_move_force(self, data: any):
        self._horizontal_move_force = data

    @property
    def vertical_move_force(self):
        return self._vertical_move_force

    @vertical_move_force.setter
    def vertical_move_force(self, data: any):
        self._vertical_move_force = data


if __name__ == '__main__':
    a = PlotterConfiguration()
    print(a)
