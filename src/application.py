from calculators import linedrawer
from output import png_output
from colours import normalise, colourise
from multiprocessing import Pool, cpu_count
from typing import List

width = 1920
height = 1080
region = [-2.0 + 1.125j, 2.0 - 1.125j]
iterations = 5000
escapeval = 4
greylevels = 255
power = 1.5
constant = -0.1948

def proc_draw (drawer) -> List[float]:
    drawer.draw()
    return drawer.get_output()

def main():
    cpus = cpu_count()

    if cpus == 0:
        print('Defaulting to 4 processes')
        cpus = 4
    else:
        print('Using {} processes'.format(cpus))

    p = Pool(cpus)

    # hold IM constant (a line from +imag to -imag)
    vertical = linedrawer.LineDrawer(region[0], region[0].real + region[1].imag*1j, height)
    vertical.create_range()

    # print('Vert range {}'.format(vertical.get_points()))

    # Create a line-drawer for each horizontal line, holding RE constant
    # all_drawers = [linedrawer.MandelbrotDrawer(x, region[1].real + x.imag*1j, width, escapeval, iterations, power) for x in vertical.get_points()]
    all_drawers = [linedrawer.JuliaDrawer(x, region[1].real + x.imag * 1j, width, escapeval, iterations, power, constant) for
                   x in vertical.get_points()]

    for drawer in all_drawers:
        drawer.create_range()

    print('Point field created')

    # for drawer in all_drawers:
    # drawer.draw()

    # final_grid = [x.get_output() for x in all_drawers]

    final_grid = p.map(proc_draw, all_drawers)
    print('Drawing complete')

    # norm = normalise.Normaliser(greylevels)
    col = colourise.Colouriser(colourise.get_default_ranger(), cpus)
    writer = png_output.PngWriter('./mandy.png', width, height)

    print('Colourising and writing')
    writer.add_colour(col.colourise(final_grid))
    writer.close()
    print('Done')


if __name__ == "__main__":
    main()