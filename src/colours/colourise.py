from typing import List, Tuple
from math import floor
from multiprocessing import Pool

colour_red = (255, 0, 0)
colour_green = (0, 255, 255)
colour_blue = (0, 0, 255)
colour_black = (0, 0, 0)
colour_white = (255, 255, 255)
colour_magenta = (255, 0, 255)
colour_yellow = (255, 255, 0)
colour_mid_grey = (127, 127, 127)
colour_dark_purple = (35, 16, 81)
colour_mid_teal = (66, 148, 155)
colour_orange = (255, 134, 5)
colour_lime_green = (200, 255, 5)
colour_sky_blue = (100, 233, 255)
colour_purple = (135, 32, 232)
colour_lilac = (230, 200, 255)

simple_transition_list = [colour_red, colour_green, colour_blue]

bgr_list = [colour_blue, colour_green, colour_red]

ship_list = [colour_mid_teal, colour_black, colour_orange, colour_red, colour_magenta, colour_purple]
ship_list2 = [colour_black, colour_mid_teal, colour_white, colour_sky_blue, colour_purples, colour_red, colour_magenta, colour_dark_purple]

black_purple_list = [colour_black, colour_purple,
                     colour_black, colour_purple,
                     colour_black, colour_purple,
                     colour_black, colour_purple]

many_transitions_list = [colour_purple, colour_green,
                         colour_blue, colour_black,
                         colour_red, colour_yellow,
                         colour_magenta, colour_orange,
                         colour_lime_green, colour_white,
                         colour_mid_teal, colour_dark_purple,
                         colour_sky_blue, colour_mid_grey]

# The highest point will equal the max point otherwise, fudge by 0.1%
fudge_factor = 1.001


class ColourRanger:

    """
    Use various colour lists to create transition palettes
    Then allow a lookup on that palette for a given point
    value (in a range when also given a max)
    """

    def __init__(self, colour_map: List[Tuple[int, int, int]]):
        self.segments = (len(colour_map) - 1)
        self.totalcolours = 255 * self.segments
        self.colour_map = colour_map

    # Given a float in the range 0.0-1.0, work out which colour it represents
    def get_colour_basic(self, proportion: float) -> (int, int, int):
        multi_segment_prop = proportion * self.segments
        segment = int(floor(multi_segment_prop))

        # print ("Choosing segment {} of {} because of {}".format(segment, self.segments, proportion))

        r1, g1, b1 = self.colour_map[segment]
        r2, g2, b2 = self.colour_map[segment + 1]

        inner_prop = multi_segment_prop - segment

        return int(r1 + inner_prop * (r2 - r1)), int(g1 + inner_prop * (g2 - g1)), int(b1 + inner_prop * (b2 - b1))

    def get_colour(self, point: float, point_max: float) -> (int, int, int):
        ratio = point / point_max
        return self.get_colour_basic(ratio)

    def get_colour_root(self, point: float, point_max: float) -> (int, int, int):
        ratio = point / point_max
        return self.get_colour_basic(ratio)

    def get_colour_log(self, point: float, point_max: float) -> (int, int, int):
        ratio = point / point_max
        return self.get_colour_basic(ratio)


class ColourRangerWithAbsBlack(ColourRanger):
    def get_colour_basic(self, proportion: float) -> (int, int, int):
        if proportion == 0.0:
            return colour_black
        return super(ColourRangerWithAbsBlack, self).get_colour_basic(proportion)


class ColourRangerWithExponentScaling(ColourRangerWithAbsBlack):
    def __init__(self, colour_map: List[Tuple[int, int, int]], power: float):
        self.power = power
        super(ColourRangerWithExponentScaling, self).__init__(colour_map)

    def get_colour(self, point: float, point_max: float) -> (int, int, int):
        ratio = point / point_max
        return self.get_colour_basic(ratio ** self.power)


def colourise_max_worker(data: List[float]) -> float:
    return max(data)


class Colouriser:

    """
    Take the raw data from the fractal generator, and apply colour maps to it
    """

    def __init__(self, ranger: ColourRanger, processors: int):
        self.range = ranger
        self.processors = processors
        self.total_max = 0

    def colourise_worker(self, data: List[float]) -> List[int]:
        return [x for point in data for x in self.range.get_colour(point, self.total_max)]

    def colourise(self, raw_data: List[List[float]]) -> List[List[int]]:
        p = Pool(self.processors)
        self.total_max = max(p.map(colourise_max_worker, raw_data)) * fudge_factor
        # print('total max - {}'.format(self.total_max))
        return p.map(self.colourise_worker, raw_data)
