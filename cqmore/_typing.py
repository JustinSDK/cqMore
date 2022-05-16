from typing import Iterable, Union, Tuple, List

from cadquery import Vector

Point2D = Tuple[float, float]
Point3D = Tuple[float, float, float]
FaceIndices = Tuple[int, ...]
MeshGrid = Union[List[List[Point2D]], List[List[Point3D]], List[List[Vector]]]
Polygon = Iterable[Point2D]
