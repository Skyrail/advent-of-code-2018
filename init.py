from core import Core
import sys

if len(sys.argv) != 2:
    raise ValueError('Please supply the day to be processed')

day = sys.argv[1]

core = Core(day)

core.getInputFromRemote()