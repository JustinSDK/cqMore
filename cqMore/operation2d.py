from cadquery import (
    Vector,
    Wire, 
    Workplane,
    DirectionSelector
)
    
def intersect2D(workplane, toIntersect):
    return bool2D(workplane, toIntersect, 'intersect')
    
def union2D(workplane, toUnion):
    return bool2D(workplane, toUnion, 'union')

def cut2D(workplane, toCut):
    return bool2D(workplane, toCut, 'cut')

def bool2D(workplane, toBool, boolMethod):
    toExtruded = (
        Workplane(toBool.plane)
            .add(toBool.vals())
            .toPending()
    )
    booled = Workplane.__dict__[boolMethod](workplane.extrude(1), toExtruded.extrude(1))
    planeZdir = DirectionSelector(-workplane.plane.zDir)
    return booled.faces(planeZdir).wires().toPending()

def makePolygon(workplane, listOfXYTuple, forConstruction = False):
    def _makePolygon(points, forConstruction):
        return Wire.makePolygon((
                 Vector(*p) for p in points + [points[0]]
            ), 
            forConstruction
        )
    p = _makePolygon(listOfXYTuple, forConstruction)
    return workplane.eachpoint(lambda loc: p.moved(loc), True)