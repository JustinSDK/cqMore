from cadquery import (
    Vector,
    Wire, 
    Workplane,
    DirectionSelector
)

from typing import (
    TypeVar,
    Iterable,
    Tuple,
    Union
)

T = TypeVar('T', bound = 'Workplane')
VectorLike = Union[Tuple[float, float], Tuple[float, float, float], Vector]
    
def intersect2D(workplane: T, toIntersect: T) -> T:
    return bool2D(workplane, toIntersect, 'intersect')
    
def union2D(workplane: T, toUnion: T) -> T:
    return bool2D(workplane, toUnion, 'union')

def cut2D(workplane: T, toCut: T) -> T:
    return bool2D(workplane, toCut, 'cut')

def bool2D(workplane: T, toBool: T, boolMethod: str) -> T:
    toExtruded = (
        Workplane(toBool.plane)
            .add(toBool.vals())
            .toPending()
    )
    booled = Workplane.__dict__[boolMethod](workplane.extrude(1), toExtruded.extrude(1))
    planeZdir = DirectionSelector(-workplane.plane.zDir)
    return booled.faces(planeZdir).wires().toPending()

def makePolygon(workplane: T, listOfXYTuple: Iterable[VectorLike], forConstruction: bool = False) -> T:
    def _makePolygon(points, forConstruction):
        return Wire.makePolygon((
                 Vector(*p) for p in points + [points[0]]
            ), 
            forConstruction
        )
    p = _makePolygon(listOfXYTuple, forConstruction)
    return workplane.eachpoint(lambda loc: p.moved(loc), True)