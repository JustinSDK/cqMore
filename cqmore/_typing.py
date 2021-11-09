from typing import Iterable, Union

from cadquery import Vector

Point2D = tuple[float, float]
Point3D = tuple[float, float, float]
FaceIndices = tuple[int, ...]
MeshGrid = Union[list[list[Point2D]], list[list[Point3D]], list[list[Vector]]]
Polygon = Iterable[Point2D]