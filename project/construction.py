import numpy as np


from lib_vars import *
from lib_elements import *
from lib_commands import *
from lib_expressions import *

#--------------------------------------------------------------------------

class Construction:
    def __init__(self):
        self.vars = []
        self.elements = [
            Element("xAxis", Line((0, 1), 0), visible=False),
            Element("yAxis", Line((1, 0), 0), visible=False)
        ]
        self.commands = []

    def __repr__(self):
        str_out = "-------------------\n[[construction]]:\n"

        str_out += "\n[{} vars]:".format(len(self.vars)) + '\n'
        for var in self.vars: str_out += str(var) + '\n'
       
        str_out += "\n[{} elements]:".format(len(self.elements)) + '\n'
        for element in self.elements: str_out += str(element) + '\n'
        
        str_out += "\n[{} commands]:".format(len(self.commands)) + '\n'
        for command in self.commands: str_out += str(command) + '\n'

        str_out += "-------------------\n"
        return str_out

    def new_repr(self):
        return "-------------------\n[[construction]]:\n" + \
            f"\n[{len(self.vars)} vars]:\n" + '\n'.join(map(str, self.vars)) + "\n" + \
                f"\n[{len(self.elements)} elements]:\n" + '\n'.join(map(str, self.elements)) + "\n" + \
                    f"\n[{len(self.commands)} commands]:\n" + '\n'.join(map(str, self.commands)) + "\n" + \
                        "-------------------\n"

    def add(self, obj):
        if isinstance(obj, Var): self.vars.append(obj)
        elif isinstance(obj, Element): self.elements.append(obj)
        elif isinstance(obj, Command): self.commands.append(obj)
        
    def elementByName(self, name: str) -> Element | None:
        result = list(filter(lambda elem: elem.name == name, self.elements))
        return result[0] if result else None

    def varByName(self, name:str) -> Var | None:
        result = list(filter(lambda var: var.name == name, self.vars))
        return result[0] if result else None

    def objectByName(self, name: str) -> Element | Var | None:
        result_element = list(filter(lambda elem: elem.name == name, self.elements))
        result_var = list(filter(lambda var: var.name == name, self.vars))
        result = result_element + result_var
        return result[0] if result else None

    def commandByElementName(self, name: str) -> Command | None:
        result = list(filter(lambda comm: comm.outputs[0] == name, self.commands))
        return result[0] if result else None

    def dataByStr(self, text):
        obj = self.objectByName(text)
        if obj is not None: return obj.data

        if is_number(text): return float(text)

        if is_angle_degrees(text): return AngleSizeFromDegrees(text)

        #raise Exception("Not found object(s) '{}' or not processing".format(text))
        return None

    def prepareInputs(self, command):
        for i in range(len(command.inputs)):
            if isinstance(command.inputs[i], str):
                command.inputs[i] = self.dataByStr(command.inputs[i])

    def rebuild(self):
        for command in self.commands: self.apply(command)

    def copy(self, command):
        assert(isinstance(command, Command))
        command_copy = Command(command.name, list(command.inputs).copy(), list(command.outputs).copy())
        return command_copy

    def apply(self, command_original):
        command = self.copy(command_original)
        self.prepareInputs(command)
        input_data = [obj.data if hasattr(obj,"data") else obj for obj in command.inputs]

        f = command.func()

        if f is not None:
            output_data = f(*input_data)
            if not isinstance(output_data, list): output_data = [output_data]
            print("{}: {} >> {}".format(f.__name__, output_data, command.outputs))

            # здесь идет проверка выходных данных output_data и запись соответствующих данных в command.outputs

            for i in range(len(output_data)):
                if i < len(command.outputs) and output_data[i] is not None:
                    if self.objectByName(command.outputs[i]) is None:
                        if isinstance(output_data[i], (Point, Line, Angle, Polygon, Circle, Vector)):
                            self.add(Element(command.outputs[i], output_data[i]))
                        elif isinstance(output_data[i], (int, float, Boolean, Measure, AngleSize)):
                            self.add(Var(command.outputs[i], output_data[i]))
                    else:
                        self.objectByName(command.outputs[i]).data = output_data[i]
        else:
            print("NONE {}: {}".format(strFullCommand(command.name, command.inputs), command.inputs))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_angle_degrees(s):
    try:
        assert(s[-1] == '°')
        float(s[:-1])
        return True
    except:
        return False