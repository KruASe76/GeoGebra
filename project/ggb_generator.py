# TODO: ggb_generator.save(construction, path)
# Later it will be construction.Construction()'s method

import os
import shutil
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from folder2zip import convert

from construction import Construction
from lib_commands import Command

from ggb_parser import load


temp_path = os.path.join(os.getcwd(), "GeoGebra", "temp")
source_path = os.path.join(os.getcwd(), "GeoGebra", "project", "source")


def get_point_elem(comm: Command) -> Element:
    elem = Element(
        "element",
        attrib={
            "type": "point",
            "label": comm.outputs[0]
        }
    )
    elem.extend(
        [
            Element(
                "show",
                attrib = {
                    "object": "true",
                    "label": "true"
                }
            ),
            Element(
                "objColor",
                attrib = {
                    "r": "0",
                    "g": "0",
                    "b": "0",
                    "a": "0"
                }
            ),
            Element(
                "layer",
                attrib = {
                    "val": "0"
                }
            ),
            Element(
                "labelMode",
                attrib = {
                    "val": "0"
                }
            ),
            Element(
                "animation",
                attrib = {
                    "step": "0.1",
                    "speed": "1",
                    "type": "1",
                    "playing": "false"
                }
            ),
            Element(
                "auxiliary",
                attrib = {
                    "val": "false"
                }
            ),
            Element(
                "coords",
                attrib = {
                    "x": comm.inputs[0],
                    "y": comm.inputs[1],
                    "z": "1"
                }
            ),
            Element(
                "pointSize",
                attrib = {
                    "val": "5"
                }
            ),
            Element(
                "pointStyle",
                attrib = {
                    "val": "10"
                }
            )
        ]
    )
    return elem


def save(constr: Construction, path: str) -> None:
    shutil.copytree(source_path, temp_path)
    
    xml = ElementTree.parse(os.path.join(temp_path, "geogebra.xml"))
    constr_elem = xml.find("construction")
    
    for comm in constr.commands:
        if comm.name == "Point" and len(comm.inputs) == 2:
            elem = get_point_elem(comm)
            constr_elem.append(elem)

    xml.write(os.path.join(temp_path, "geogebra.xml"))
    
    convert(temp_path, path)
    os.rename(f"{path}.zip", path)
    
    shutil.rmtree(temp_path)


if __name__ == "__main__":
    constr = load(os.path.join("files", "all_elements.ggb"))
    save(constr, os.path.join("files", "test.ggb"))
