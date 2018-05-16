from typing import List
from cmath import log10


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

    def __init__(self, start_point: complex, end_point: complex, steps: int, escape: float, iterations: int):
        super(IterativeDrawer, self).__init__(start_point, end_point, steps)
        self.escape = escape
        self.iterations = iterations
        self.total = 0

    def calculate_point(self, point_val: complex) -> float:
        self.total = 0 + 0j
        iters = 0
        while abs(self.total) <= self.escape and iters < self.iterations:
            self.total = self.apply_alg(self.total, point_val)
            iters += 1
        if iters == self.iterations:
            return 0.0
        else:
            return 0.0 + iters

    def apply_alg(self, total: complex, pointval: complex) -> complex:
        return self.escape + 0j


class LogDrawer(IterativeDrawer):

    """
    Instead of just returning the iterations, calculate a smooth mu
    """

    def __init__(self,
                 start_point: complex,
                 end_point: complex,
                 steps: int,
                 escape: float,
                 iterations: int,
                 power: complex):

        super(LogDrawer, self).__init__(start_point, end_point, steps, escape, iterations)
        self.power = power

    def calculate_point(self, point_val: complex) -> float:
        n = super(LogDrawer, self).calculate_point(point_val)
        if n == 0.0 :
            return 0.0
        mu = (n + 1) - (log10(log10(abs(self.total))) / log10(self.power))
        return abs(mu)

class MandelbrotDrawer(LogDrawer):

    """
    A Mandelbrot drawer creates mandelbrot style fractals with arbitrary (complex)
    powers
    """

    def apply_alg(self, total: complex, pointval: complex) -> complex:
        return (total ** self.power) + pointval

class JuliaDrawer(LogDrawer):

    """
    A Mandelbrot drawer creates mandelbrot style fractals with arbitrary (complex)
    powers
    """

    def __init__(self,
                 start_point: complex,
                 end_point: complex,
                 steps: int,
                 escape: float,
                 iterations: int,
                 power: complex,
                 constant: complex):
        super(JuliaDrawer, self).__init__(start_point, end_point, steps, escape, iterations, power)
        self.constant = constant

    def apply_alg(self, total: complex, pointval: complex) -> complex:
        if total == 0 + 0j:
            total = pointval
        return (total ** self.power) + self.constant
