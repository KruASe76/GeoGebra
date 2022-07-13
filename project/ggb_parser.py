import os
import shutil
from zipfile import ZipFile
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from construction import Construction
from lib_commands import Command


temp_path = os.path.join(os.getcwd(), "temp")


def get_constr_elem(ggb_path: str) -> Element:
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
    return root.find("construction")


def apply_points(constr_elem: Element) -> None:
    global constr
    
    for point_elem in constr_elem.findall('element[@type="point"]'):
        coords = list(point_elem.find("coords").attrib.values())
        coords.pop(-1) # removing z coordinate
        constr.add(Command("Point", coords, point_elem.attrib["label"]))
        
def apply_commands(constr_elem: Element) -> None:
    global constr
    
    for comm_elem in constr_elem.findall("command"):
        comm_type = comm_elem.attrib["name"]
        input_elem = comm_elem.find("input")
        output_elem = comm_elem.find("output")
        constr.add(Command(comm_type, list(input_elem.attrib.values()), list(output_elem.attrib.values())))


def load(ggb_path: str) -> Construction:
    global constr
    
    constr = Construction()
    constr_elem = get_constr_elem(ggb_path)
    
    apply_points(constr_elem)
    apply_commands(constr_elem)
    constr.rebuild()
    
    shutil.rmtree(temp_path)
    
    return constr
