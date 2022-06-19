from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import os
import shutil
import zipfile
from dataclasses import dataclass
from folder2zip import convert

@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int

@dataclass
class Coords:
    x: float
    y: float
    z: int

@dataclass
class PointAnimation:
    step: float
    speed: int
    type: int
    playing: bool

@dataclass
class Point:
    label: str
    show_object: bool
    show_label: bool
    color: Color
    layer: int
    label_offset: Coords # without z
    label_mode: int
    animation: PointAnimation
    auxiliary: bool
    coords: Coords
    size: int
    style: int
    
    @classmethod
    def from_element(self, element: Element):
        show_elem = element.find("show")
        label_offset_elem = element.find("labelOffset")
        animation_elem = element.find("animation")
        auxiliary_elem = element.find("auxiliary")
        return Point(
            label = element.attrib["label"],
            show_object = False if show_elem.attrib["object"] == "false" else True,
            show_label = False if show_elem.attrib["label"] == "false" else True,
            color = Color(*map(int, element.find("objColor").attrib.values())),
            layer = int(element.find("layer").attrib["val"]),
            label_offset = Coords(*map(float, label_offset_elem.attrib.values()), 0) if label_offset_elem else Coords(0, 0, 0),
            label_mode = int(element.find("labelMode").attrib["val"]),
            animation = PointAnimation(
                step = float(animation_elem.attrib["step"]),
                speed = int(animation_elem.attrib["speed"]),
                type = int(animation_elem.attrib["type"]),
                playing = False if animation_elem.attrib["playing"] == "false" else True
            ) if animation_elem else PointAnimation(step=0.1, speed=1, type=1, playing=False),
            auxiliary = False if not auxiliary_elem or auxiliary_elem.atttib["val"] == "false" else True,
            coords = Coords(*map(float, element.find("coords").attrib.values())),
            size = int(element.find("pointSize").attrib["val"]),
            style = int(element.find("pointStyle").attrib["val"])
        )
    
    def commit(self, element: Element) -> None:
        for child in element:
            element.remove(child)
        
        element.extend(
            [
                Element(
                    "show",
                    attrib = {
                        "object": str(self.show_object).lower(),
                        "label": str(self.show_label).lower()
                    }
                ),
                Element(
                    "objColor",
                    attrib = {
                        "r": str(self.color.r),
                        "g": str(self.color.g),
                        "b": str(self.color.b),
                        "a": str(self.color.a)
                    }
                ),
                Element(
                    "layer",
                    attrib = {
                        "val": str(self.layer)
                    }
                ),
                Element(
                    "labelMode",
                    attrib = {
                        "val": str(self.label_mode)
                    }
                ),
                Element(
                    "animation",
                    attrib = {
                        "step": str(self.animation.step),
                        "speed": str(self.animation.speed),
                        "type": str(self.animation.type),
                        "playing": str(self.animation.playing).lower()
                    }
                ),
                Element(
                    "auxiliary",
                    attrib = {
                        "val": str(self.auxiliary).lower()
                    }
                ),
                Element(
                    "coords",
                    attrib = {
                        "x": str(self.coords.x),
                        "y": str(self.coords.y),
                        "z": str(self.coords.z)
                    }
                ),
                Element(
                    "pointSize",
                    attrib = {
                        "val": str(self.size)
                    }
                ),
                Element(
                    "pointStyle",
                    attrib = {
                        "val": str(self.style)
                    }
                )
            ]
        )
    
    def to_element(self) -> Element: # Delete?
        element = Element(
            "element",
            attrib = {
                "type": "point",
                "label": self.label
            }
        )
        element.extend(
            [
                Element(
                    "show",
                    attrib = {
                        "object": str(self.show_object).lower(),
                        "label": str(self.show_label).lower()
                    }
                ),
                Element(
                    "objColor",
                    attrib = {
                        "r": self.color.r,
                        "g": self.color.g,
                        "b": self.color.b,
                        "a": self.color.a
                    }
                ),
                Element(
                    "layer",
                    attrib = {
                        "val": self.layer
                    }
                ),
                Element(
                    "labelMode",
                    attrib = {
                        "val": self.label_mode
                    }
                ),
                Element(
                    "animation",
                    attrib = {
                        "step": self.animation.step,
                        "speed": self.animation.speed,
                        "type": self.animation.type,
                        "playing": str(self.animation.playing).lower()
                    }
                ),
                Element(
                    "auxiliary",
                    attrib = {
                        "val": self.auxiliary
                    }
                ),
                Element(
                    "coords",
                    attrib = {
                        "x": self.coords.x,
                        "y": self.coords.y,
                        "z": self.coords.z
                    }
                ),
                Element(
                    "pointSize",
                    attrib = {
                        "val": self.size
                    }
                ),
                Element(
                    "pointStyle",
                    attrib = {
                        "val": self.style
                    }
                )
            ]
        )
        return element


temp_path = os.path.join(os.getcwd(), "temp")
files_path = os.path.join(os.getcwd(), "files")

# ggb_path = input(f"Input .ggb plan path (Current: {os.getcwd()})\n>> ")
# if not ggb_path.endswith(".ggb"):
#     raise ValueError("Plan path is not ending with '.ggb'")
ggb_path = os.path.join("files", "all_elements.ggb")

try:    
    os.mkdir("temp")
except FileExistsError:
    pass
shutil.copyfile(ggb_path, os.path.join(temp_path, "temp.ggb"))

ggb = zipfile.ZipFile(os.path.join(temp_path, "temp.ggb"))
ggb.extractall(temp_path)
ggb.close()
os.remove(os.path.join(temp_path, "temp.ggb"))

tree = ElementTree.parse(os.path.join(temp_path, "geogebra.xml"))
root = tree.getroot()

construction: Element = root.find("construction")

for point_elem in construction.findall('element[@type="point"]'):
    # point = Point.from_element(point_elem)
    # print(point)
    # new_point_elem = point.to_element()
    # print(list(new_point_elem))
    # new_point = Point.from_element(new_point_elem)
    # print(point == new_point)
    # exit()
    
    point = Point.from_element(point_elem)
    
    point.style = 4
    point.color = Color(0, 255, 0, 0)
    
    point.commit(point_elem)

tree.write(os.path.join(temp_path, "geogebra.xml"))

try:
    os.remove(os.path.join(files_path, "new_all_elements.ggb"))
except FileNotFoundError:
    pass
convert(temp_path, os.path.join(files_path, "new_all_elements"))
shutil.rmtree(temp_path)
os.rename(os.path.join(files_path, "new_all_elements.zip"), os.path.join(files_path, "new_all_elements.ggb"))
