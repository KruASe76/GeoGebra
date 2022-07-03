import numpy as np


from lib_vars import *
from lib_elements import *
from lib_commands import *
from lib_expressions import *

#--------------------------------------------------------------------------

class Construction:
    def __init__(self):
        self.vars = []
        self.elements = []
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

    def add(self, obj):
        if isinstance(obj, Var): self.vars.append(obj)
        elif isinstance(obj, Element): self.elements.append(obj)
        elif isinstance(obj, Command): self.commands.append(obj)

    def varByName(self, name):
        for var in self.vars:
            if var.name is name: return var
        return None

    def elementByName(self, name):
        for element in self.elements:
            if element.name is name: return element
        return None

    def objectByName(self, name):
        obj = None
        for var in self.vars:
            if var.name is name: obj = var
        for element in self.elements:
            if element.name is name: obj = element
        return obj

    def dataByStr(self, text):
        obj = self.objectByName(text)
        if obj is not None: return obj.data

        if is_number(text): return float(text)

        #raise Exception("Not found object(s) '{}' or not processing".format(text))
        return None

    def prepareInputs(self, command):
        for i in range(len(command.inputs)):
            if isinstance(command.inputs[i], str):
                command.inputs[i] = self.dataByStr(command.inputs[i])

    def rebuild(self):
        for command in self.commands: self.apply(command)

    def apply(self, command):
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


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False