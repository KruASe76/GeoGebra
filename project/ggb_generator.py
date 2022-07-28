# TODO: ggb_generator.save(construction, path)
# Later it will be construction.Construction()'s method

import os
import shutil
from xml.etree import ElementTree

from folder2zip import convert

from construction import Construction
from lib_commands import Command
from lib_elements import Element, Point, Line

from ggb_parser import load


temp_path = os.path.join(os.getcwd(), "temp")
source_path = os.path.join(os.getcwd(), "project", "source")


def line_coords(comm: Command, constr: Construction) -> tuple[int, int, int]:  # line equation coefficients
    elem1, elem2 = map(lambda name: constr.elementByName(name), comm.inputs)
    if comm.name in ("Line", "Ray", "Segment"):
        if isinstance(elem1.data, Point) and isinstance(elem2.data, Point):
            left_multiplier = elem2.data.a[1] - elem1.data.a[1]
            right_multiplier = elem2.data.a[0] - elem1.data.a[0]
            return -left_multiplier, right_multiplier, -elem1.data.a[0] * left_multiplier - elem1.data.a[1] * right_multiplier
        else:  # elem2.data is Line
            reference_line_comm = constr.commandByElementName(elem2.name)
            a, b, _ = line_coords(reference_line_comm, constr)
            return a, b, -(a * elem1.data.a[0] + b * elem1.data.a[1])  # free coefficient for that point
    elif comm.name == "OrthogonalLine":  # elem2.data is Line
        reference_line_comm = constr.commandByElementName(elem2.name)
        a, b, _ = line_coords(reference_line_comm, constr)
        a, b = -b, a
        return a, b, -(a * elem1.data.a[0] + b * elem1.data.a[1])


def get_point_elem(comm: Command, constr: Construction) -> ElementTree.Element:
    elem = ElementTree.Element(
        "element",
        attrib={
            "type": "point",
            "label": comm.outputs[0]
        }
    )
    elem.extend(
        [
            ElementTree.Element(
                "show",
                attrib = {
                    "object": str(constr.elementByName(comm.outputs[0]).visible).lower(),
                    "label": "true"
                }
            ),
            ElementTree.Element(
                "objColor",
                attrib = {
                    "r": "0",
                    "g": "0",
                    "b": "0",
                    "alpha": "0"
                }
            ),
            ElementTree.Element(
                "layer",
                attrib = {
                    "val": "0"
                }
            ),
            ElementTree.Element(
                "labelMode",
                attrib = {
                    "val": "0"
                }
            ),
            ElementTree.Element(
                "animation",
                attrib = {
                    "step": "0.1",
                    "speed": "1",
                    "type": "1",
                    "playing": "false"
                }
            ),
            ElementTree.Element(
                "auxiliary",
                attrib = {
                    "val": "false"
                }
            ),
            ElementTree.Element(
                "coords",
                attrib = {
                    "x": comm.inputs[0],
                    "y": comm.inputs[1],
                    "z": "1"
                }
            ),
            ElementTree.Element(
                "pointSize",
                attrib = {
                    "val": "5"
                }
            ),
            ElementTree.Element(
                "pointStyle",
                attrib = {
                    "val": "10"
                }
            )
        ]
    )
    return elem

def get_lines_elems(comm: Command, constr: Construction) -> ElementTree.Element:
    a, b, c = line_coords(comm, constr)
    
    comm_elem = ElementTree.Element(
        "command",
        attrib={
            "name": comm.name
        }
    )
    comm_elem.extend(
        [
            ElementTree.Element(
                "input",
                attrib={
                    "a0": comm.inputs[0],
                    "a1": comm.inputs[1]
                }
            ),
            ElementTree.Element(
                "output",
                attrib={
                    "a0": comm.outputs[0]
                }
            )
        ]
    )
    
    elem_elem = ElementTree.Element(
        "element",
        attrib={
            "type": comm.name.lower(),
            "label": comm.outputs[0]
        }
    )
    elem_elem.extend(
        [
            ElementTree.Element(
                "show",
                attrib = {
                    "object": str(constr.elementByName(comm.outputs[0]).visible).lower(),
                    "label": "false"
                }
            ),
            ElementTree.Element(
                "objColor",
                attrib = {
                    "r": "97",
                    "g": "97",
                    "b": "97",
                    "alpha": "0"
                }
            ),
            ElementTree.Element(
                "layer",
                attrib = {
                    "val": "0"
                }
            ),
            ElementTree.Element(
                "labelMode",
                attrib = {
                    "val": "0"
                }
            ),
            ElementTree.Element(
                "coords",
                attrib = {
                    "x": str(a),
                    "y": str(b),
                    "z": str(c)
                }
            ),
            ElementTree.Element(
                "lineStyle",
                attrib={
                    "thickness": "5",
                    "type": "0",
                    "typeHidden": "1",
                    "opacity": "204"
                }
            ),
            ElementTree.Element(
                "eqnStyle",
                attrib={
                    "style": "explicit"
                }
            )
        ]
    )
    if comm.name in ("Ray", "Segment"):
        elem_elem.extend(
            [
                ElementTree.Element(
                    "outlyingIntersections",
                    attrib={
                        "val": "false"
                    }
                ),
                ElementTree.Element(
                    "keepTypeOnTransform",
                    attrib={
                        "val": "true"
                    }
                )
            ]
        )
    
    return comm_elem, elem_elem


def save(constr: Construction, path: str) -> None:
    shutil.copytree(source_path, temp_path)
    
    xml = ElementTree.parse(os.path.join(temp_path, "geogebra.xml"))
    constr_elem = xml.find("construction")
    
    for comm in constr.commands:
        if comm.name == "Point" and len(comm.inputs) == 2:
            elem = get_point_elem(comm, constr)
            constr_elem.append(elem)
        elif comm.name in ("Line", "OrthogonalLine", "Ray", "Segment"):
            elems = get_lines_elems(comm, constr)
            constr_elem.extend(elems)

    xml.write(os.path.join(temp_path, "geogebra.xml"))
    
    convert(temp_path, path)
    if os.access(path, os.F_OK):
        os.remove(path)
    os.rename(f"{path}.zip", path)
    
    shutil.rmtree(temp_path)


if __name__ == "__main__":
    constr = load(os.path.join("files", "all_elements.ggb"))
    save(constr, os.path.join("files", "temp.ggb"))
