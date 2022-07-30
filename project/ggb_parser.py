# Later it will be construction.Construction()'s classmethod

import os
import shutil
from zipfile import ZipFile
from xml.etree import ElementTree
from xml.etree.ElementTree import Element as XElement  # shortened "XML Element"

from construction import Construction
from lib_commands import Command
from lib_vars import Var, AngleSize


temp_path = os.path.join(os.getcwd(), "temp")


def get_constr_xelem(ggb_path: str) -> XElement:
    try:    
        os.mkdir(temp_path)
    except FileExistsError:
        pass
    shutil.copyfile(ggb_path, os.path.join(temp_path, "temp.ggb"))
    
    ggb = ZipFile(os.path.join(temp_path, "temp.ggb"))
    ggb.extractall(temp_path)
    ggb.close()
    os.remove(os.path.join(temp_path, "temp.ggb"))
    
    tree = ElementTree.parse(os.path.join(temp_path, "geogebra.xml"))
    root = tree.getroot()
    
    shutil.rmtree(temp_path)
    
    return root.find("construction")

def parse(constr_xelem: XElement) -> Construction:
    constr = Construction()
    xelems_left_to_pass = 0
    
    for xelem in constr_xelem:
        if xelems_left_to_pass:
            xelems_left_to_pass -= 1
            continue
        if xelem.tag == "expression":
            xelems_left_to_pass = 1
            continue
        if xelem.tag == "command":
            comm_name = xelem.attrib["name"]
            if comm_name == "PointIn":
                xelems_left_to_pass = 1
                continue
            
            input_xelem = xelem.find("input")
            output_xelem = xelem.find("output")
            
            constr.add(Command(comm_name, list(input_xelem.attrib.values()), list(output_xelem.attrib.values())))
            xelems_left_to_pass = len(output_xelem.attrib)
            continue
        
        # Here xelem has to be a commandless point or numeric (Var)
        
        if xelem.tag == "element":
            if xelem.attrib["type"] == "point":
                coords = list(xelem.find("coords").attrib.values())
                coords.pop(-1) #  removing z coordinate
                constr.add(Command("Point", coords, xelem.attrib["label"]))
                continue
            if xelem.attrib["type"] == "numeric":
                value_xelem = xelem.find("value")
                constr.add(Var(xelem.attrib["label"], float(value_xelem.attrib["val"])))
                continue
            if xelem.attrib["type"] == "angle":
                value_xelem = xelem.find("value")
                constr.add(Var(xelem.attrib["label"], AngleSize(float(value_xelem.attrib["val"]))))
                continue
        
        raise ElementTree.ParseError(f"Unexpected XElement met:\n\t<{xelem.tag}>, {xelem.attrib}")
    
    constr.rebuild()
    return constr


def load(ggb_path: str) -> Construction:
    constr_xelem = get_constr_xelem(ggb_path)
    constr = parse(constr_xelem)
    
    return constr
