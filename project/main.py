import os

from construction import *

import ggb_parser
import short_parser
import draw

#--------------------------------------------------------------------------

if __name__ == "__main__":
    #construction = ggb_parser.load("somefile.txt")
    construction = ggb_parser.load("somefile.ggb")

    #здесь можно менять construction, запускать визуализацию и тп

    short_parser.save(construction, "somefile.txt")

