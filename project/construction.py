from lib_vars import *
from lib_elements import *
from lib_expressions import *
from lib_commands import *

#--------------------------------------------------------------------------

class Construction:
    def __init__(self):
        self.vars = []
        self.elements = []
        self.expressions = []
        self.commands = []

    def add(self, var):
        self.vars.append(var)

    def add(self, element):
        self.elements.append(element)

    def add(self, command):
        self.commands.append(command)

    def rebuild(self):
        for command in self.commands: self.apply(command)

    def apply(self, command):
        input_data = [x.data for x in self.inputs]
        name = command_types_name(self.name, input_data)

        '''
        if name not in command_dict: name = self.name
        f = command_dict[name]
        output_data = f(*input_data)
        if not isinstance(output_data, (tuple, list)): output_data = (output_data,)
        assert(len(output_data) == len(self.output_elements))
        for x,o in zip(output_data, self.output_elements):
            if o is not None: o.data = x
            '''

