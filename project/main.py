import lib_vars
import lib_elements
import lib_commands
import lib_expressions

from lib_vars import *
from lib_elements import *
from lib_commands import *
from lib_expressions import *

from construction import *

#import short_parser
#import ggb_parser

import draw_simple

#--------------------------------------------------------------------------

if __name__ == "__main__":
    #construction = shortpy_parser.load("shortpy_test.txt")
    #construction = short_parser.load("short_test.txt")
    #construction = ggb_parser.load("test.ggb")

    constr = Construction()

    constr.add(Var("x", 5))
    constr.add(Var("y", 7))
    #construction.add(Var("y", "x + 5"))
    #construction.add(Command("Assign", Expression("x + 5"), "y"))

    constr.add(Command("Point", ["x", "y"], "A"))
    constr.add(Command("Point", [1.5, 2], "B"))
    constr.add(Command("Line", ["A", "B"], "l"))

    constr.add(Command("Circle", ["A", "B"], "ω"))
    constr.add(Command("Intersect", ["ω", "l"], ["C", "D"]))

    constr.add(Command("OrthogonalLine", ["A", "l"], "l2"))
    constr.add(Command("Intersect", ["l2", "ω"], ["E", "F"]))
    
    print("BEFORE:\n" + str(constr))

    constr.rebuild()

    print("AFTER:\n" + str(constr))

    #constr.add(Command("Point", ["XCoord(Smth)", "YCoord(Smth) + 2"], "B"))

    #...

    #short_parser.save(construction, "somefile.txt")

    draw_simple.Show(constr)