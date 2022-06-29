from lib_vars import *
from lib_expressions import *
from lib_elements import *
from lib_commands import *

#--------------------------------------------------------------------------

class Construction:
    def __init__(self, display_size = (100,100), min_border = 0.1, max_border = 0.25):
        self.corners = np.array(((0,0), display_size))
        self.min_border = min_border
        self.max_border = max_border
        self.nc_commands = []
        self.to_prove = None
        self.element_dict = dict()
        self.elements = []

    def render(self, cr, elements = None): # default: render all elements
        if elements is None: elements = self.elements

        for el in elements:
            el.draw(cr, self.corners)

    def render_to_numpy(self, elements = None):
        surface = cairo.ImageSurface(cairo.FORMAT_A8, self.width, self.height)
        cr = cairo.Context(surface)
        self.render(cr, elements)

        data = surface.get_data()
        data = np.array(data, dtype = float)/255
        data = data.reshape([self.height, surface.get_stride()])
        data = data[:,:self.width]
        return data

    def load(self, filename):
        self.nc_commands = []
        self.to_prove = None
        self.element_dict = dict()
        with open(filename, 'r') as f:
            for line in f:
                command = parse_command(line, self.element_dict)
                if isinstance(command, ConstCommand): command.apply()
                elif isinstance(command, Command):
                    if command.name == "prove":
                        [inp] = command.input_elements
                        [out] = command.output_elements
                        if out is not None: del self.element_dict[out.label]
                        assert(self.to_prove is None)
                        self.to_prove = inp

                    else: self.nc_commands.append(command)

        assert(self.to_prove is not None)
        self.elements = list(self.element_dict.values())

    def run_commands(self):
        for command in self.nc_commands: command.apply()

    def generate(self, require_theorem = True, max_attempts = 100): # max_attempts = 0 -> inf
        while True:
            try:
                self.run_commands()
            except:
                max_attempts -= 1
                if max_attempts == 0: raise
                continue
            if require_theorem and not self.to_prove.data.b: continue
            break

        self.fit_to_window()

    def fit_to_window(self):
        important_points = []
        for el in self.elements: important_points += el.important_points()
        if len(important_points) == 0: return
        src_corners = np.stack([
            np.min(important_points, axis = 0),
            np.max(important_points, axis = 0),
        ])
        src_size = np.maximum(0.01, src_corners[1] - src_corners[0])

        dest_size = self.corners[1] - self.corners[0]
        dest_corners_shift = np.random.random(size = [2,2])
        dest_corners_shift *= self.max_border - self.min_border
        dest_corners_shift += self.min_border
        dest_corners_shift *= np.array((1,-1)).reshape((2,1)) * dest_size
        dest_corners = self.corners + dest_corners_shift
        dest_size = dest_corners[1] - dest_corners[0]

        scale = np.min(dest_size / src_size)
        src_corners *= scale
        shift = np.average(dest_corners, axis = 0) - np.average(src_corners, axis = 0)
        for el in self.elements:
            if isinstance(el.data, (int, float)): continue
            el.data.scale(scale)
            el.data.translate(shift)

        important_points = []
        for el in self.elements: important_points += el.important_points()
        corners = np.stack([
            np.min(important_points, axis = 0),
            np.max(important_points, axis = 0),
        ])

    def test(self, num_tests = 100):
        constr_fail, check_fail, success = 0, 0, 0
        for _ in range(num_tests):
            try:
                self.run_commands()
                if self.to_prove.data.b: success += 1
                else: check_fail += 1
            except:
                constr_fail += 1

        constr_fail, check_fail, success = [
            100*x / num_tests
            for x in (constr_fail, check_fail, success)
        ]
        print("{:.2f}% failed constructions, {:.2f}% false, {:.2f}% true".format(
            constr_fail, check_fail, success
        ))
