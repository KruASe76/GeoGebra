# Later it will be construction.Construction()'s classmethod

import os
import shutil
from xml.etree import ElementTree

from folder2zip import convert

from construction import Construction
from lib_commands import Command
from lib_elements import *

from ggb_parser import load


temp_path = os.path.join(os.getcwd(), "temp")
source_path = os.path.join(os.getcwd(), "project", "source")


def get_comm_elem(comm: Command) -> ElementTree.Element:
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
                attrib={f"a{ind}": input for ind, input in enumerate(comm.inputs)}
            ),
            ElementTree.Element(
                "output",
                attrib={f"a{ind}": output for ind, output in enumerate(comm.outputs)}
            )
        ]
    )

    return comm_elem


def line_coords(data: Line | Ray | Segment) -> tuple[int, int, int]:  # line equation coefficients
    return *data.n, -data.c
    # some useless but working code (if comm: Command and constr: Construction are passed):
    """    
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
    """

def conic_matrix(data: Circle | Arc) -> tuple[int, int, int, int, int, int]:
    return 1, 1, data.c[0]**2 + data.c[1]**2 - data.r_squared, 0, -data.c[0], -data.c[1]


def get_points_elems(comm: Command, constr: Construction) -> tuple[ElementTree.Element]:
    point_elem = constr.elementByName(comm.outputs[0])
    
    elem_elem = ElementTree.Element(
        "element",
        attrib={
            "type": "point",
            "label": comm.outputs[0]
        }
    )
    elem_elem.extend(
        [
            ElementTree.Element(
                "show",
                attrib = {
                    "object": str(point_elem.visible).lower(),
                    "label": "true"
                }
            ),
            ElementTree.Element(
                "objColor",
                attrib={name: str(value) for name, value in zip(("r", "g", "b", "alpha"), (97, 97, 97, 0) if comm.name == "Intersect" else (21, 101, 192, 0))}
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
                    "x": str(point_elem.data.a[0]),
                    "y": str(point_elem.data.a[1]),
                    "z": "1"
                }
            ),
            ElementTree.Element(
                "pointSize",
                attrib = {
                    "val": "4" if comm.name == "Intersect" else "5"
                }
            ),
            ElementTree.Element(
                "pointStyle",
                attrib = {
                    "val": "0"
                }
            )
        ]
    )
    
    if comm.name == "Point" and len(comm.inputs) == 2:
        return (elem_elem,)
    
    return get_comm_elem(comm), elem_elem

def get_lines_elems(comm: Command, constr: Construction) -> tuple[ElementTree.Element]:
    line_elem = constr.elementByName(comm.outputs[0])
    coords = line_coords(line_elem.data)
    
    elem_elem = ElementTree.Element(
        "element",
        attrib={
            "type": "line" if comm.name == "OrthogonalLine" else comm.name.lower(),
            "label": comm.outputs[0]
        }
    )
    elem_elem.extend(
        [
            ElementTree.Element(
                "show",
                attrib = {
                    "object": str(line_elem.visible).lower(),
                    "label": "false"
                }
            ),
            ElementTree.Element(
                "objColor",
                aattrib={name: str(value) for name, value in zip(("r", "g", "b", "alpha"), (97, 97, 97, 0))}
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
                attrib = {name: str(value) for name, value in zip("xyz", coords)}
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
    
    return get_comm_elem(comm), elem_elem

def get_conics_elems(comm: Command, constr: Construction) -> tuple[ElementTree.Element]:
    matrix = conic_matrix(constr.elementByName(comm.outputs[0]).data)

    elem_elem = ElementTree.Element(
        "element",
        attrib={
            "type": "conic" if comm.name == "Circle" else "conicpart",
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
                attrib={name: str(value) for name, value in zip(("r", "g", "b", "alpha"), (97, 97, 97, 0))}
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
                "lineStyle",
                attrib={
                    "thickness": "5",
                    "type": "0",
                    "typeHidden": "1",
                    "opacity": "204"
                }
            ),
            ElementTree.Element(
                "eigenvectors",
                attrib={name: str(value) for name, value in zip(("x0", "y0", "z0", "x1", "y1", "z1"), (1, 0, 1.0, 0, 1, 1.0))}
            ),
            ElementTree.Element(
                "matrix",
                attrib={f"A{ind}": str(value) for ind, value, in enumerate(matrix)}
            ),
            ElementTree.Element(
                "eqnStyle",
                attrib={
                    "style": "specific"
                }
            )
        ]
    )
    if comm.name == "Semicircle":
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
    
    return get_comm_elem(comm), elem_elem


def save(constr: Construction, path: str) -> None:
    shutil.copytree(source_path, temp_path)
    
    xml = ElementTree.parse(os.path.join(temp_path, "geogebra.xml"))
    constr_elem = xml.find("construction")
    
    for comm in constr.commands:
        if comm.name in ("Point", "Intersect", "Rotate"):
            elems = get_points_elems(comm, constr)
            constr_elem.extend(elems)
        elif comm.name in ("Line", "OrthogonalLine", "Ray", "Segment"):
            elems = get_lines_elems(comm, constr)
            constr_elem.extend(elems)
        elif comm.name in ("Circle", "Semicircle"):
            elems = get_conics_elems(comm, constr)
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
