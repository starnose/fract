from calculators.factories import *
from output import png_output
from colours import normalise
from colours.colourise import *
from multiprocessing import cpu_count
from multiprocessing_on_dill.pool import Pool
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


def draw_fractal(factory: LineFactory,
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
    pool = Pool(cpus)
    final_grid = pool.map(proc_draw, all_drawers)
    pool.close()
    print('Drawing complete')
    print('Output Starting....')
    writer = png_output.PngWriter(filename, width, height)
    print_colour(final_grid, writer, cpus, colouriser)
    # print_grey(final_grid, writer, cpus, 255)


def tech_demo(processes: int, xres: int, yres: int):

    # The regions/windows onto all the fractals below are 16:9, so the resolutions
    # probably should be too

    draw_fractal(MandelLambdaFactory(8, 500, 2, lambda z, c: z ** 2 + c),
                 processes, xres, yres, [-2.5 + 1.125j, 1.5 - 1.125j],
                 ColourRangerWithExponentScaling(many_transitions_list, 0.25), './mandel.png')

    draw_fractal(MandelLambdaFactory(8, 500, -2, lambda z, c: z ** -2 + c),
                 processes, xres, yres, [-2.5 + 1.125j, 1.5 - 1.125j],
                 ColourRangerWithExponentScaling(many_transitions_list, 0.25), './negative.png')

    draw_fractal(MandelLambdaFactory(3, 500, 2, lambda z, c: (z.conjugate() ** 2) + c),
                 processes, xres, yres, [-4.0 + 2.25j, 4.0 - 2.25j],
                 ColourRangerWithExponentScaling(many_transitions_list, 0.25), './mandelbar.png')

    draw_fractal(MandelLambdaFactory(4, 5000, 3, lambda z, c: (z ** 3) + 0.4 + 0.002275j),
                 processes, xres, yres, [-2.0 + 1.125j, 2.0 - 1.125j],
                 ColourRangerWithExponentScaling(many_transitions_list, 0.25), './julia3.png')

    draw_fractal(MandelLambdaFactory(4, 5000, 4, lambda z, c: (z ** 4) + 0.559 - 0.0481j),
                 processes, xres, yres, [-2.0 + 1.125j, 2.0 - 1.125j],
                 ColourRangerWithExponentScaling(many_transitions_list, 0.25), './julia4.png')

    draw_fractal(MandelLambdaFactory(4, 5000, 6, lambda z, c: (z ** 6) + 0.736 - 0.417355j),
                 processes, xres, yres, [-2.0 + 1.125j, 2.0 - 1.125j],
                 ColourRangerWithExponentScaling(many_transitions_list, 0.25), './julia6.png')

    draw_fractal(MandelLambdaFactory(4, 500, -2, lambda z, c: (z ** -2) + 0.653125 + 0.510337j),
                 processes, xres, yres, [-2.0 + 1.125j, 2.0 - 1.125j],
                 ColourRangerWithExponentScaling(many_transitions_list, 1.0), './julia-negative.png')

    #draw_fractal(MandelLambdaFactory(4, 500, -4, lambda z, c: (z ** -4) + -0.791 - 0.07j), # -0.1, -0.04
    #             processes, xres, yres, [-4.0 + 2.5j, 4.0 - 2.5j],
    #             ColourRangerWithExponentScaling(many_transitions_list, 1.0), './julia-negative-auto-big2.png')

    draw_fractal(MandelLambdaFactory(4, 5000, 1.5, lambda z, c: (z ** 1.5) + -0.1948 + 0j),
                 processes, yres, xres, [-0.6947218749999999 + 0.28875000000000006j, -0.369878125 - 0.28875000000000006j],
                 ColourRangerWithExponentScaling(many_transitions_list, 1.0), './glynn-tree.png')

    # Mandeldrops require a polar inversion of all points before running, so need a different factory
    draw_fractal(MandelDropFactory(3, 500, 2), processes, xres, yres, [-2.5 + 2.25j, 5.5 - 2.25j],
                 ColourRangerWithExponentScaling(simple_transition_list, 0.25), './drop.png')

    draw_fractal(MandelDropFactory(3, 500, 3), processes, xres, yres, [-4 + 2.25j, 4 - 2.25j],
                 ColourRangerWithExponentScaling(simple_transition_list, 0.25), './drop3.png')

    draw_fractal(MandelDropFactory(3, 500, 4), processes, xres, yres, [-4 + 2.25j, 4 - 2.25j],
                 ColourRangerWithExponentScaling(simple_transition_list, 0.25), './drop4.png')

    draw_fractal(MandelLambdaFactory(8, 500, -4, lambda z, c: (1 - z**(5))/(z**2 - c)), processes, xres, yres,
                 [-0.925 + 0.06328125j, -0.675 - 0.06328125j],
                 ColourRangerWithExponentScaling(many_transitions_list, 1.0), './multipower.png')

    # Ships get a reflection in the x axis before drawing
    draw_fractal(ShipFactory(4, 5000, 2), processes, xres, yres, [-1.68 + 0.07125j, -1.58 - 0.02875j],
                 ColourRangerWithExponentScaling(ship_list, 0.25), './burning-ship.png')

    # Newton fractals are a little different...
    draw_fractal(NewtonFactory(500, 0.0001, 1.0 + 0.0j, lambda z: (z**3) - 1, lambda z: 3*(z**2)),
                 processes, xres, yres, [-2.0 + 1.125j, 2.0 - 1.125j],
                 ColourRangerWithExponentScaling(bgr_list, 1.0), './newt.png')

    # For... reasons, this gives us interesting stalks, but cannot be run with its real derivative
    draw_fractal(NewtonStalkFactory(500, 0.0001, 1.0 + 0.0j, lambda z: (z**3) - 1, lambda z: 2*(z**2)),
                 processes, xres, yres, [-2.0 + 1.125j, 2.0 - 1.125j],
                 ColourRangerWithExponentScaling(ship_list2, 1.0), './stalk.png')

    # A pickover drawer which uses a component as test instead of abs()
    draw_fractal(PickoverFactory(3, 500, 3, lambda z, c: (z**3) + -1 + 1j),
                 processes, xres, yres, [-4 + 2.25j, 4 - 2.25j],
                 ColourRangerWithExponentScaling(bgr_list, 0.5), './pickover.png')

    draw_fractal(PickoverFactory2(10, 500, 5, lambda z, c: (z**5) + 1 + 1j),
                 processes, xres, yres, [-3.0 + 1.6875j, 3.0 - 1.6875j],
                 ColourRangerWithExponentScaling(many_transitions_list, 0.5), './pickover2.png')


def main():
    processes = cpu_count()
    if processes == 0:
        print('Defaulting to 4 processes')
        processes = 4
    else:
        print('Using {} processes'.format(processes))

    tech_demo(processes, 384, 216)


if __name__ == "__main__":
    main()
