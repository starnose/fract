from typing import List
from multiprocessing import Pool


def normalise_max_worker(row: List[float]):
    return max(row)


class Normaliser:

    """
    Take an array of data points, normalise them to a given integer-space
    """

    def __init__(self, data_range: int):
        self.range = data_range
        self.total_max = 0

    def normalise_point(self, point: float, max_value: float):
        return int((point * self.range) / max_value)

    def normalise(self, points: List[int]) -> List[int]:
        max_value = max(points)
        if max_value == 0:
            max_value = 1
        return [self.normalise_point(x, max_value) for x in points]

    def normalise_nest_flatten(self, points: List[List[int]]) -> List[int]:
        flat_list = [x for sublist in points for x in sublist]
        return self.normalise(flat_list)

    def normalise_worker(self, row: List[float]) -> List[int]:
        return [self.normalise_point(x, self.total_max) for x in row]

    def normalise_nest_no_flatten(self, points: List[List[float]], processes: int) -> List[List[int]]:
        # print('Normalising data - {}'.format(points))
        p = Pool(processes)
        # self.total_max = max([max(row) for row in points])
        self.total_max = max(p.map(normalise_max_worker, points))
        print('Max found - {}'.format(self.total_max))

        # output = [self.normalise_worker(total_max, row) for row in points]
        output = p.map(self.normalise_worker, points)
        # print('Normalised data - {}'.format(output))
        return output
