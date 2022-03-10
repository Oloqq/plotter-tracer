from ccli import CCLI
from configuration import PlotterConfiguration
from gcoding import Gcoder
from plopping import make_plopchart
from navigating import closing_circles, longstroke, squiggler

ccli = CCLI()
conf = PlotterConfiguration()
A = list[str]

def run(args: A):
    # TODO conf.validate() see configuration.py

    # TODO refactor plopchart into 'extract' function
    # taking any image and returning 2D array
    # that will be passed to navigating algorithm 
    plopchart = make_plopchart(conf.input_path, save=False, show=False)
    moves = squiggler(plopchart) # TODO make algortihm configurable

    # TODO move this to 'visualize' command
    # width, height = plopchart.size
    # the result is saved in data/visualiser_out
    # visualize(moves, width, height, show=True)

    # TODO move this to a separate 'load' command
    # settings = json.load(open('prof.json'))

    gcoder = Gcoder(conf)
    gcoder.encode(moves, save='data/output.gcode') # TODO make output path configurable

def select_input(args: A):
    if type(args) != list or len(args) < 2:
        print('bad format, no change')
        return
    try:
        conf.input_path = args[1]
    except FileNotFoundError:
        pass