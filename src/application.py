from calculators.linedrawer import *
from output import png_output
from colours import normalise
from colours.colourise import *
from multiprocessing import Pool, cpu_count
from typing import List


def proc_draw(drawer) -> List[float]:
    drawer.create_range()
    drawer.draw()
    return drawer.get_output()


def print_grey(points: List[List[float]], writer: png_output.PngWriter, cpus: int, greylevels: int):
    norm = normalise.Normaliser(greylevels)
    normed = norm.normalise_nest_no_flatten(points, cpus)
    writer.add_greyscale(normed)
    writer.close()


def print_colour(points: List[List[float]], writer: png_output.PngWriter, cpus: int, ranger: ColourRanger):
    col = Colouriser(ranger, cpus)
    print('Colourising and writing')
    writer.add_colour(col.colourise(points))
    writer.close()
    print('Done')


def draw_fractal(factory: LineDrawerFactory,
                 cpus: int,
                 width: int,
                 height: int,
                 region: List[complex],
                 colouriser: ColourRanger,
                 filename: str):

    """
    Given a line-calculator factory with the fractal type and parameters pre-encoded in it
    create an image

    :param factory: The line-drawer-generator for the fractal
    :param cpus: The number of processes to use
    :param width: The image width to produce
    :param height: The image height to produce
    :param region: The window onto the fractal we're interested in
    :param colouriser: The raw->colour pixel generator
    :param filename: The name of the image to write out
    :return:
    """

    # hold IM constant (a line from +imag to -imag)
    vertical = LineDrawer(region[0], region[0].real + region[1].imag*1j, height)
    vertical.create_range()

    # Create a line-drawer for each horizontal line, holding RE constant
    all_drawers = [factory.get_drawer(x, region[1].real + x.imag * 1j, width) for x in vertical.get_points()]

    print('Drawing Starting....')
    p = Pool(cpus)
    final_grid = p.map(proc_draw, all_drawers)
    print('Drawing complete')
    print('Output Starting....')
    writer = png_output.PngWriter(filename, width, height)
    print_colour(final_grid, writer, cpus, colouriser)
    # print_grey(final_grid, writer, cpus, 255)


# There are here simply because python's default pickle cannot cope with lambdas
# It should be possible (with a bit of work) to make multiprocess use 'dill' instead
# of the default pickle, which has support for lambda pickling
def simple_newton_function(x: complex) -> complex:
    return (x**3) - 1


def simple_newton_derivative(x: complex) -> complex:
    return 2*(x**2)


def main():
    cpus = cpu_count()
    if cpus == 0:
        print('Defaulting to 4 processes')
        cpus = 4
    else:
        print('Using {} processes'.format(cpus))

    draw_fractal(MandelFactory(3, 500, 2), cpus, 384, 216, [-2.5 + 1.125j, 1.5 - 1.125j],
                 ColourRangerWithExponentScaling(many_transitions_list, 0.25), './mandel.png')

    draw_fractal(MandelFactory(10, 1000, -2), cpus, 384, 216, [-2.5 + 1.125j, 1.5 - 1.125j],
                 ColourRangerWithAbsBlack(many_transitions_list), './negative.png')

    drop_factory = MandelDropFactory(3, 500, 2)
    draw_fractal(drop_factory, cpus, 384, 216, [-2.5 + 2.25j, 5.5 - 2.25j],
                 ColourRangerWithExponentScaling(simple_transition_list, 0.25), './drop.png')

    # julia_factory = JuliaFactory(4, 5000, 3, 0.4 + 0.002275j)
    # julia_factory = JuliaFactory(4, 5000, 4, 0.559 - 0.0481j)
    julia_factory = JuliaFactory(4, 5000, 6, 0.736 - 0.417355j)
    draw_fractal(julia_factory, cpus, 384, 216, [-2.0 + 1.125j, 2.0 - 1.125j],
                 ColourRangerWithAbsBlack(many_transitions_list), './julia.png')

    draw_fractal(JuliaFactory(4, 5000, 1.5, -0.1948 + 0j),
                 cpus, 216, 384, [-0.6947218749999999 + 0.28875000000000006j, -0.369878125 - 0.28875000000000006j],
                 ColourRangerWithAbsBlack(many_transitions_list), './tree.png')

    draw_fractal(ShipFactory(4, 5000, 2), cpus, 384, 216, [-1.68 + 0.07125j, -1.58 - 0.02875j],
                 ColourRangerWithExponentScaling(ship_list, 0.25), './ship.png')

    newton_factory = NewtonFactory(500, 0.0001, 1.0 + 0.0j, simple_newton_function, simple_newton_derivative)
    draw_fractal(newton_factory, cpus, 384, 216, [-2.0 + 1.125j, 2.0 - 1.125j],
                 ColourRangerWithAbsBlack(bgr_list), './newt.png')

    stalk_factory = NewtonStalkFactory(500, 0.0001, 1.0 + 0.0j, simple_newton_function, simple_newton_derivative)
    draw_fractal(stalk_factory, cpus, 384, 216, [-2.0 + 1.125j, 2.0 - 1.125j],
                 ColourRangerWithAbsBlack(many_transitions_list), './stalk.png')


if __name__ == "__main__":
    main()
