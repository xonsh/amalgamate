import os
import sys

local_root = os.path.dirname(os.path.dirname(__file__))

if local_root not in sys.path:
    sys.path.insert(0, local_root)
