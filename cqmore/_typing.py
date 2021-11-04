from typing import Iterable, TypeVar, Union

from cadquery import Vector, Workplane


T = TypeVar('T', bound = 'Workplane')
Point2D = tuple[float, float]
Point3D = tuple[float, float, float]
VectorLike = Union[Point2D, Point3D, Vector]
FaceIndices = tuple[int, ...]
MeshGrid = Union[list[list[Point2D]], list[list[Point3D]], list[list[Vector]]]
Polygon = Iterable[Point2D]