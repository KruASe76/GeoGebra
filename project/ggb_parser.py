# Later it will be construction.Construction()'s classmethod

import os
import shutil
from zipfile import ZipFile
from xml.etree import ElementTree

from construction import Construction
from lib_commands import Command


temp_path = os.path.join(os.getcwd(), "temp")


def get_constr_elem(ggb_path: str) -> ElementTree.Element:
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

def parce(constr_elem: ElementTree.Element) -> Construction:
    constr = Construction()
    elems_left_to_pass = 0
    
    for elem in constr_elem:
        if elems_left_to_pass:
            elems_left_to_pass -= 1
            continue
        if elem.tag == "expression":
            elems_left_to_pass = 1
            continue
        if elem.tag == "command":
            comm_name = elem.attrib["name"]
            if comm_name == "PointIn":
                elems_left_to_pass = 1
                continue
            
            input_elem = elem.find("input")
            output_elem = elem.find("output")
            
            constr.add(Command(comm_name, list(input_elem.attrib.values()), list(output_elem.attrib.values())))
            elems_left_to_pass = len(output_elem.attrib)
        else:  # elem has to be commandless point
            if elem.tag != "element" and elem.attrib["type"] != "point":
                raise ElementTree.ParseError(f"Unexpected element met:\n<{elem.tag}>, {elem.attrib}")
            coords = list(elem.find("coords").attrib.values())
            coords.pop(-1) #  removing z coordinate
            constr.add(Command("Point", coords, elem.attrib["label"]))
    
    constr.rebuild()
    return constr


def load(ggb_path: str) -> Construction:
    constr_elem = get_constr_elem(ggb_path)
    constr = parce(constr_elem)
    
    return constr
