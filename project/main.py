from lib_vars import *
from lib_elements import *
from lib_commands import *
from lib_expressions import *

from construction import *

#import short_parser
import ggb_parser
import ggb_generator

import draw_simple
import draw_mp

import os

#--------------------------------------------------------------------------

def testConstruction():
    constr = Construction()

    # длины сторон треугольника a, b, c
    constr.add(Var("a", 6.5))
    constr.add(Var("b", 8))
    constr.add(Var("c", 4))

    # треугольник ABC по трем сторонам a, b, c
    constr.add(Command("Point", ["0", "0"], "A"))
    constr.add(Command("Point", ["c", "0"], "B"))
    constr.add(Command("Circle", ["A", "b"], "ω1"))
    constr.add(Command("Circle", ["B", "a"], "ω2"))
    constr.add(Command("Intersect", ["ω1", "ω2"], ["C_1", "C"]))
    constr.add(Command("Polygon", ["A", "B", "C"], "triang")) #пока не создается
    constr.add(Command("Segment", ["A", "B"], "s1"))
    constr.add(Command("Segment", ["B", "C"], "s2"))
    constr.add(Command("Segment", ["A", "C"], "s3"))

    # центр вписанной окружности для треугольника ABC
    constr.add(Command("AngularBisector", ["C", "A", "B"], "l1"))
    constr.add(Command("AngularBisector", ["C", "B", "A"], "l2"))
    constr.add(Command("Intersect", ["l1", "l2"], "O"))
    
    # вписанная окружность треугольника ABC
    constr.add(Command("Line", ["A", "B"], "l"))
    constr.add(Command("OrthogonalLine", ["O", "l"], "h"))
    constr.add(Command("Intersect", ["h", "l"], "H"))
    constr.add(Command("Circle", ["O", "H"], "ω"))

    constr.rebuild()

    constr.elementByName("ω1").visible = False
    constr.elementByName("ω2").visible = False
    constr.elementByName("l1").visible = False
    constr.elementByName("l2").visible = False
    constr.elementByName("l").visible = False
    constr.elementByName("h").visible = False
    constr.elementByName("H").visible = False

    return constr

def test1():
    constr = testConstruction()

    #print("AFTER:\n" + str(constr))

    draw_simple.Add(constr)

    constr.varByName("c").data = 10
    constr.rebuild()
    draw_simple.Add(constr)

    constr.varByName("c").data = 13
    constr.rebuild()
    draw_simple.Add(constr)

    draw_simple.Show()

def test2():
    constr = ggb_parser.load("GeoGebra/files/all_elements.ggb")
    print(constr)
    draw_mp.exportPDF(constr, "GeoGebra/files/metapost/test.pdf")

def test3():
    #constr = ggb_parser.load("GeoGebra/files/all_elements.ggb")
    constr = testConstruction()
    print(constr)
    ggb_generator.save(constr, "files/testConstruction.ggb")

#--------------------------------------------------------------------------

if __name__ == "__main__":
    test3()
