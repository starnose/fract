from typing import List, Callable
from cmath import log10, rect, phase


class LineDrawer:

    """
    A line drawer class that takes the start and end point of a line
    and creates the points along it
    """

    def __init__(self, start_point: complex, end_point: complex, steps: int):
        self.start_point = start_point
        self.end_point = end_point
        self.steps = steps
        self.points = []
        self.outpoints = []

    def create_range(self):
        # print("Input points are - {}, {}".format(self.start_point, self.end_point))
        if self.start_point.real != self.end_point.real:
            # print("step basis - {}".format(self.end_point.real - self.start_point.real))
            re_step = (self.end_point.real - self.start_point.real) / (self.steps - 1)
        else:
            re_step = 0 + 0j

        if self.start_point.imag != self.end_point.imag:
            im_step = (self.end_point.imag - self.start_point.imag) / (self.steps - 1)
        else:
            im_step = 0 + 0j

        # print("Step values are - {}, {}".format(re_step, im_step))

        int_points = range(0, self.steps, 1)

        self.points = [(x*re_step + self.start_point.real) + (x*im_step + self.start_point.imag)*1j for x in int_points]
        self.map_points()

    def map_points(self):
        pass

    def get_points(self) -> List[complex]:
        return self.points

    def get_output(self) -> List[float]:
        return self.outpoints

    def draw(self):
        self.outpoints = [self.calculate_point(x) for x in self.points]

    def calculate_point(self, pointval: complex) -> int:
        return 0


class IterativeDrawer(LineDrawer):

    """
    An iterative drawer applies a generic iterative method across all points
    in its range until an escape is reached
    """

    def __init__(self, start_point: complex, end_point: complex, steps: int, iterations: int):
        super(IterativeDrawer, self).__init__(start_point, end_point, steps)
        self.iterations = iterations
        self.total = 0

    def calculate_point(self, point_val: complex) -> float:
        self.total = 0 + 0j
        self.init_point(point_val)
        iters = 0
        while self.apply_condition(iters) and iters < self.iterations:
            self.total = self.apply_alg(self.total, point_val)
            iters += 1
        return self.calc_returnval(iters, point_val)

    def calc_returnval(self, iterations: float, point_val: complex) -> float:
        if iterations == self.iterations:
            return 0.0
        else:
            return 0.0 + iterations

    def apply_condition(self, iters: int) -> bool:
        return False

    def init_point(self, point_val: complex):
        pass

    def apply_alg(self, total: complex, pointval: complex) -> complex:
        return 0 + 0j


class PowerAndEscapeDrawer(IterativeDrawer):
    def __init__(self,
                 start_point: complex,
                 end_point: complex,
                 steps: int,
                 iterations: int,
                 power: complex,
                 escape: float):
        super(PowerAndEscapeDrawer, self).__init__(start_point, end_point, steps, iterations)
        self.escape = escape
        self.power = power

    def apply_condition(self, iters: int) -> bool:
        return abs(self.total) <= self.escape

    def init_point(self, point_val: complex):
        self.total = point_val


class LogDrawer(PowerAndEscapeDrawer):

    """
    Instead of just returning the iterations, calculate a smooth mu
    """

    def calc_returnval(self, iterations: float, point_val: complex) -> float:
        n = super(LogDrawer, self).calc_returnval(iterations, point_val)
        if n == 0.0:
            return 0.0
        mu = (n + 1) - (log10(log10(abs(self.total))) / log10(self.power))
        return abs(mu)


class PolarInverterDrawer(LineDrawer):
    """
    Invert all points in the unit circle before drawing
    """
    def map_points(self):
        self.points = [rect(1.0/abs(x), phase(x)) for x in self.points]


class MandelbrotDrawer(LogDrawer):

    """
    A Mandelbrot drawer creates mandelbrot style fractals with arbitrary (complex)
    powers
    """

    def apply_alg(self, total: complex, pointval: complex) -> complex:
        return (total ** self.power) + pointval


class SafeMandelbrotDrawer(MandelbrotDrawer):

    """
    A Mandelbrot drawer creates mandelbrot style fractals with arbitrary (complex)
    powers but that is safe for negative powers at the origin point
    """
    def calculate_point(self, point_val: complex) -> float:
        if point_val == 0.0 + 0.0j:
            return 0.0
        return super(SafeMandelbrotDrawer, self).calculate_point(point_val)


class ShipDrawer(LogDrawer):

    """
    A burning ship drawer
    """

    # Flip the image upside down before starting
    def map_points(self):
        self.points = [x.real + (x.imag * -1.0j) for x in self.points]

    def apply_alg(self, total: complex, pointval: complex) -> complex:
        return ((abs(total.real) + (1j * abs(total.imag))) ** self.power) + pointval


class NewtonDrawer(IterativeDrawer):
    def __init__(self,
                 start_point: complex,
                 end_point: complex,
                 steps: int,
                 iterations: int,
                 tolerance: float,
                 constant: complex,
                 main_function: Callable[[complex], complex],
                 derivative: Callable[[complex], complex]):

        super(NewtonDrawer, self).__init__(start_point, end_point, steps, iterations)
        self.tolerance = tolerance
        self.constant = constant
        self.last_value = 100000.0 + 0.0j
        self.function = main_function
        self.derivative = derivative

    def init_point(self, point_val: complex):
        self.total = point_val

    def apply_condition(self, iters: int) -> bool:
        return (abs(self.last_value.real - self.total.real) > self.tolerance) \
               or (abs(self.last_value.imag - self.total.imag) > self.tolerance)

    def apply_alg(self, total: complex, pointval: complex) -> complex:
        self.last_value = self.total
        denominator = self.derivative(self.total)
        if denominator.real == 0.0 and denominator.imag == 0.0:

            return self.last_value
        return self.total - (self.constant * (self.function(self.total)/denominator))


class NewtonStalkDrawer(LogDrawer):
    def __init__(self,
                 start_point: complex,
                 end_point: complex,
                 steps: int,
                 iterations: int,
                 tolerance: float,
                 constant: complex,
                 main_function: Callable[[complex], complex],
                 derivative: Callable[[complex], complex]):

        super(NewtonStalkDrawer, self).__init__(start_point, end_point, steps, iterations, 3, 0)
        self.tolerance = tolerance
        self.constant = constant
        self.last_value = 100000.0 + 0.0j
        self.function = main_function
        self.derivative = derivative

    def init_point(self, point_val: complex):
        self.total = point_val

    def apply_condition(self, iters: int) -> bool:
        return (abs(self.last_value.real - self.total.real) > self.tolerance) or (
                    abs(self.last_value.imag - self.total.imag) > self.tolerance)

    def apply_alg(self, total: complex, pointval: complex) -> complex:
        self.last_value = self.total
        denominator = self.derivative(self.total)
        if denominator.real == 0.0 and denominator.imag == 0.0:
            return self.last_value
        return self.total - (self.constant * (self.function(self.total) / denominator))


class MandelDropDrawer(PolarInverterDrawer, MandelbrotDrawer):
    def apply_condition(self, iters: int) -> bool:
        return abs(self.total) <= self.escape or iters == 0


class MandelLambdaDrawer(SafeMandelbrotDrawer):
    def __init__(self,
                 start: complex,
                 end: complex,
                 steps: int,
                 iterations: int,
                 power: complex,
                 escape: float,
                 main_function: Callable[[complex, complex], complex]):
        super(MandelLambdaDrawer, self).__init__(start, end, steps, iterations, power, escape)
        self.function = main_function

    def apply_alg(self, total: complex, pointval: complex):
        return self.function(total, pointval)


class PickoverDrawer(MandelLambdaDrawer):

    def apply_condition(self, iters: int) -> bool:
        return abs(self.total.imag) <= self.escape and abs(self.total.real) <= self.escape

    def calc_returnval(self, iterations: float, point_val: complex) -> float:
        if iterations == self.iterations:
            return 0.0
        else:
            return abs(self.total.imag) + abs(self.total.real)


class PickoverDrawer2(PowerAndEscapeDrawer):
    def __init__(self,
                 start: complex,
                 end: complex,
                 steps: int,
                 iterations: int,
                 power: complex,
                 escape: float,
                 main_function: Callable[[complex, complex], complex]):
        super(PickoverDrawer2, self).__init__(start, end, steps, iterations, power, escape)
        self.function = main_function

    def apply_condition(self, iters: int) -> bool:
        if abs(self.total.imag) <= self.escape and abs(self.total.real) <= self.escape:
            return True
        else:
            return False

    def calc_returnval(self, iterations: float, point_val: complex) -> float:
        if iterations == self.iterations:
            return 0.0
        else:
            return abs(self.total.imag) + abs(self.total.real)

    def apply_alg(self, total: complex, pointval: complex):
        return self.function(total, pointval)