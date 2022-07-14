# отрисовка конструкции в метапосте

import os
import shutil

from lib_vars import *
from lib_elements import *
from lib_commands import *

from construction import *

#--------------------------------------------------------------------------   

def test():
    '''
    Polyline(z6,z7,z0,z11,z10);
    Polygon(z8,z12,z16);
    Polyline(z9,z14,z19);
    RightAngleMark(z9,z14,z19);
    LineMark(z9,z14,2);
    LineMark(z14,z19,2);
    AngleMark(z7,z0,z11,2);
    label.urt(btex $A$ etex,z0);
    endfig;
    end
    '''
    return

def exportMP(constr: Construction, mp_path: str, mp_header_path: str):
    f = open(mp_header_path, "r")
    header = f.read()
    f.close()

    f = open(mp_path, "w")
    f.write(header)
    f.write("\n\nbeginfig(1)\n")
    f.write("\nu := 2cm;\n\n")

    '''
    f.write("% описание точек ? -----------------------\n\n")

    zpoints = {} #словарь имен точек для метапоста
    zn = 0

    for el in constr.elements:
        if type(el.data) == Point:
            f.write("z{} = ({}u, {}u)\n".format(zn, el.data.a[0], el.data.a[1]))
            zpoints[el.name] = "z" + str(zn)
            zn += 1
    '''

    f.write("% отрисовка элементов --------------------\n\n")

    # экспорт элементов
    for el in constr.elements:
        if not el.visible: continue

        if type(el.data) == Point:
            f.write("Point(({}u, {}u));\n".format(el.data.a[0], el.data.a[1]))

        elif type(el.data) == Segment:
            f.write("Segment(({}u, {}u), ({}u, {}u));\n".format(el.data.end_points[0][0], el.data.end_points[0][1], el.data.end_points[1][0], el.data.end_points[1][1]))

        elif type(el.data) == Circle:
            f.write("Circle(({}u, {}u), {}u);\n".format(el.data.c[0], el.data.c[1], el.data.r))

    f.write("\nendfig;\n")
    f.write("end\n")

    f.close()

def exportPDF(constr: Construction, pdf_path: str):
    n = pdf_path.rfind("/")
    if n < 0: dir = ""
    else: dir = pdf_path[:n] + "/"

    mp_path = pdf_path[:-4] + ".mp"
    mp_header_path = dir + "header.mp"

    exportMP(constr, mp_path, mp_header_path)

    os.system("mptopdf " + mp_path)