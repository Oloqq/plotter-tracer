from ccli import CCLI
from gcoding import sample_configuation
import json
import sys
from os import path

ccli = CCLI()
conf = sample_configuation.copy()

def select_input(args: list[str]):
    if type(args) != list or len(args) < 2:
        print('bad format, no change')
        return
    filepath = args[1]
    if not path.exists(filepath):
        print(f'file not found {filepath}')

    conf['input'] = filepath
    print(f'Input file set to {filepath}')


ccli.add('input', select_input,
"""filepath
    select input file
""")

if __name__ == "__main__":
    # conf = json.load(open('prof.json'))
    # TODO change z_high into rise_height

    if len(sys.argv) > 1 and sys.argv[1]:
        ccli.funcs['input'](sys.argv[1])
    ccli.funcs['help']([])

    ccli.loop()
    print(conf)