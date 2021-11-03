from typing import List
import png


class PngWriter:

    """
    Write out a PNG, either in greyscale or colour
    """

    def __init__(self, filename: str, width: int, height: int):
        self.image_file = open(filename, 'wb')
        self.width = width
        self.height = height

    def add_greyscale(self, data_points: List[List[int]]):
        image_writer = png.Writer(width=self.width, height=self.height, greyscale=True, bitdepth=8)
        image_writer.write(self.image_file, data_points)

    def add_colour(self, data_points: List[List[int]]):
        image_writer = png.Writer(width=self.width, height=self.height, greyscale=False)
        image_writer.write(self.image_file, data_points)

    def close(self):
        self.image_file.close()
