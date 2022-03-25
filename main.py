import sys
from operations import *

ccli.add('input', select_input,
"""filepath
    select input file""")

ccli.add('run', run, 
"""compile gcode from the current configuration
""")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        ccli.funcs['input'](['input', sys.argv[1]])
    ccli.funcs['help']([])

    ccli.loop()