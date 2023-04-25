from typing import Tuple, List, Callable
from math import sin, cos
from matplotlib.pyplot import pcolormesh, show, close

from exercise2 import Point2D
from exercise3 import Rectangle

# Task 0: add a docstring to this file
# Task A: add missing documentation for the public functions of the `Raster` class
# Task B: add documentation for the `Raster` class itself

"""
This file contains a class that represents a raster image.
"""

DataArray = List[List[float]]

class Raster:
    """A class that represents a raster image. The image is defined by a frame
    
    Attributes:asdfa
        frame: The frame of the raster image
        resolution: The resolution of the raster image as (x_resolution, y_resolution)
        spacing: The spacing between two adjacent pixels as (x_spacing, y_spacing)
        values: The values of the raster image as a 2D array
    """
    
    def __init__(self, frame: Rectangle, resolution: Tuple[int, int]) -> None:
        """
        Initialize a raster image.
        """
        self._frame = frame
        self._resolution = resolution
        self._spacing = (
            (frame.upper_right.x - frame.lower_left.x)/resolution[0],
            (frame.upper_right.y - frame.lower_left.y)/resolution[1]
        )
        self._values = self._make_data_array()

    @property
    def resolution(self) -> Tuple[int, int]:
        """Return the raster resolution as (x_resolution, y_resolution)"""
        return self._resolution

    def set_at(self, index: Tuple[int, int], value: float) -> None:
        """Set the value at the given index"""
        self._values[index[0]][index[1]] = value

    def set_from(self, function: Callable[[Point2D], float]) -> None:
        """
        Set the values of the raster from a function. 
        The function is called with a `Point2D` object as argument and should return a float.
        """
        for i in range(self._x_resolution()):
            for j in range(self._y_resolution()):
                idx = (i, j)
                point = self._get_point(idx)
                self.set_at(idx, function(point))

    def show(self) -> None:
        """Show the raster image"""
        pcolormesh(self._values)
        show()
        close() 

    def _make_data_array(self) -> DataArray:
        return [
            [0.0 for _ in range(self._x_resolution())]
            for _ in range(self._y_resolution())
        ]

    def _x_resolution(self) -> int:
        return self._resolution[0]

    def _y_resolution(self) -> int:
        return self._resolution[1]

    def _get_point(self, index: Tuple[int, int]) -> Point2D:
        x = self._frame.lower_left.x + (index[0] + 0.5)*self._spacing[0]
        y = self._frame.lower_left.y + (index[1] + 0.5)*self._spacing[1]
        return Point2D(x, y)


def test_raster_construction() -> None:
    raster = Raster(
        Rectangle(Point2D(0.0, 0.0), 1.0, 1.0),
        resolution=(100, 150)
    )
    assert raster.resolution[0] == 100
    assert raster.resolution[1] == 150


def test_raster_construction_from_function() -> None:
    raster = Raster(
        Rectangle(Point2D(0.0, 0.0), 1.0, 1.0),
        resolution=(100, 100)
    )
    raster.set_from(lambda p: sin(p.x)*cos(p.y))


if __name__ == "__main__":
    raster = Raster(
        Rectangle(Point2D(0.0, 0.0), 1.0, 1.0),
        resolution=(100, 100)
    )
    raster.set_from(lambda p: sin(p.x)*cos(p.y))
    raster.show()
