import numpy as np

import lib_vars as vars
import lib_elements as elements
import lib_commands as commands

#--------------------------------------------------------------------------

class Expression:
    def __init__(self, name, data = None):
        self.name = name
        self.data = data
        self.value = None   #= parse(data)

#--------------------------------------------------------------------------
