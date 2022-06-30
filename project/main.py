import os

from construction import *

import short_parser
import ggb_parser
import draw

#--------------------------------------------------------------------------

if __name__ == "__main__":
    #construction = shortpy_parser.load("shortpy_test.txt")
    #construction = short_parser.load("short_test.txt")
    #construction = ggb_parser.load("test.ggb")

    construction = Construction()

    construction.add(Var("x", 5))
    #construction.add(Var("y", "x + 5"))
    construction.add(Command("Assign", Expression("x + 5"), "y"))

    construction.add(Command("Point", ["x", "y"], "Smth"))
    construction.add(Command("Point", [1.5, 2], "A"))
    construction.add(Command("Point", ["XCoord(Smth)", "YCoord(Smth) + 2"], "B"))

    #...

    short_parser.save(construction, "somefile.txt")

