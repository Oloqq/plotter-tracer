from .ccli import CCLI
from .configuration import PlotterConfiguration
from .gcoding import Gcoder
from .plopping import make_plopchart
from .navigating import *
from .visualiser import visualize

ccli = CCLI()
conf = PlotterConfiguration()
A = list[str]


def run(args: A):
    plopchart = make_plopchart(conf.input_path, save=False, show=False)
    moves = squiggler(plopchart)
    visualize(moves, 100, 100)

    gcoder = Gcoder(conf)
    gcoder.encode(moves, save='data/output.gcode')


def select_input(args: A):
    if type(args) != list or len(args) < 2:
        print('bad format, no change')
        return
    try:
        conf.input_path = args[1]
    except FileNotFoundError:
        pass


def display_configuration(args: A):
    print(conf)
