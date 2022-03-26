import sys
from operations import *

ccli.add('input', select_input,
"""filepath
    select input file""")

ccli.add('run', run, 
"""compile gcode from the current configuration""")

ccli.add('print', display_configuration,
"""display current configuration""")

if __name__ == "__main__":
    # input file can by passed from command line
    if len(sys.argv) > 1 and sys.argv[1]:
        ccli.funcs['input'](['input', sys.argv[1]])
    ccli.funcs['help']([])

    ccli.loop()