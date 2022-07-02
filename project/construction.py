import numpy as np
import cmath

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
        str_out = "-- construction: --\n"

        str_out += "----- vars ({}):".format(len(self.vars)) + '\n'
        for var in self.vars: str_out += str(var) + '\n'
       
        str_out += "----- elements ({}):".format(len(self.elements)) + '\n'
        for element in self.elements: str_out += str(element) + '\n'
        
        str_out += "----- commands ({}):".format(len(self.commands)) + '\n'
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

    def objectByStr(self, text):
        findByName = self.objectByName(text)
        if findByName is not None: return findByName

        if not cmath.isnan(text): return float(text)

        raise Exception("{}: not found variable(s) or not processing".format(text))
        return None

    def prepareInOut(self, command):
        for i in range(len(command.inputs)):
            if isinstance(command.inputs[i], str):
                command.inputs[i] = self.objectByStr(command.inputs[i])
        
        for i in range(len(command.outputs)):
            if isinstance(command.outputs[i], str):
                command.outputs[i] = self.objectByStr(command.outputs[i]) 

    def rebuild(self):
        for command in self.commands: self.apply(command)

    def apply(self, command):
        self.prepareInOut(command)
        input_data = [obj.data if hasattr(obj,"data") else obj for obj in command.inputs]

        f = command.func()

        output_data = f(*input_data)
        if not isinstance(output_data, list): output_data = [output_data]

        # здесь должна быть проверка выходных данных output_data и запись соответствующих данных в command.outputs
        # проверка производится по количеству данных, по типу, сравнение с None(нужно ли?)
        # ...

        '''
        assert(len(output_data) == len(command.outputs))
        for data_from, obj_to in zip(output_data, command.outputs):
            if hasattr(obj_to, "data"): obj_to.data = data_from
            else: obj_to = data_from
        
        '''
