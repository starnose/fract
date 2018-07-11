from calculators.linedrawer import *


class LineFactory:
    def get_drawer(self, start: complex, end: complex, steps: int) -> LineDrawer:
        pass


class MandelFactory(LineFactory):
    def __init__(self, escape: float, iterations: int, power: complex):
        super(MandelFactory, self).__init__()
        self.escapeval = escape
        self.iterations = iterations
        self.power = power

    def get_drawer(self, start: complex, end: complex, steps: int) -> LineDrawer:
        return SafeMandelbrotDrawer(start, end, steps, self.iterations, self.power, self.escapeval)


class MandelDropFactory(MandelFactory):
    def get_drawer(self, start: complex, end: complex, steps: int) -> LineDrawer:
        return MandelDropDrawer(start, end, steps, self.iterations, self.power, self.escapeval)


class ShipFactory(MandelFactory):
    def get_drawer(self, start: complex, end: complex, steps: int) -> LineDrawer:
        return ShipDrawer(start, end, steps, self.iterations, self.power, self.escapeval)


class NewtonFactory(LineFactory):
    def __init__(self,
                 iterations: int,
                 tolerance: float,
                 constant: complex,
                 mainfunction: Callable[[complex], complex],
                 derivative: Callable[[complex], complex]):
        super(NewtonFactory, self).__init__()
        self.iterations = iterations
        self.tolerance = tolerance
        self.constant = constant
        self.function = mainfunction
        self.derivative = derivative

    def get_drawer(self, start: complex, end: complex, steps: int) -> LineDrawer:
        return NewtonDrawer(start,
                            end,
                            steps,
                            self.iterations,
                            self.tolerance,
                            self.constant,
                            self.function,
                            self.derivative)


class NewtonStalkFactory(NewtonFactory):
    def get_drawer(self, start: complex, end: complex, steps: int) -> LineDrawer:
        return NewtonStalkDrawer(start,
                                 end,
                                 steps,
                                 self.iterations,
                                 self.tolerance,
                                 self.constant,
                                 self.function,
                                 self.derivative)


class MandelLambdaFactory(MandelFactory):
    def __init__(self,
                 escape: float,
                 iterations: int,
                 power: complex,
                 main_function: Callable[[complex, complex], complex]):
        super(MandelLambdaFactory, self).__init__(escape, iterations, power)
        self.function = main_function

    def get_drawer(self, start: complex, end: complex, steps: int):
        return MandelLambdaDrawer(start, end, steps, self.iterations, self.power, self.escapeval, self.function)


class PickoverFactory(MandelLambdaFactory):
    def get_drawer(self, start: complex, end: complex, steps: int) -> LineDrawer:
        return PickoverDrawer(start, end, steps, self.iterations, self.power, self.escapeval, self.function)


class PickoverFactory2(MandelLambdaFactory):
    def get_drawer(self, start: complex, end: complex, steps: int) -> LineDrawer:
        return PickoverDrawer2(start, end, steps, self.iterations, self.power, self.escapeval, self.function)
