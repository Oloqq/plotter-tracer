import sys
from operations import *

ccli.add('input', select_input,
"""filepath
    select input file""")

ccli.add('run', run, 
"""compile gcode from the current configuration
""")

# TODO print configuration + print one value
# TODO import/export configuration with JSON
# TODO command to execute commands from a file

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        ccli.funcs['input'](['input', sys.argv[1]])
    ccli.funcs['help']([])

    ccli.loop()