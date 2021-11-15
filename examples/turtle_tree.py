from cqmore.matrix import rotation, translation
from cqmore import Workplane
from cqmore.polyhedron import tetrahedron

class Turtle:
    def __init__(self, pos = (0, 0, 0)):
        self.coordinateVt = pos
        self.xAxis = (1, 0, 0)
        self.yAxis = (0, 1, 0)
        self.zAxis = (0, 0, 1)


    def forward(self, leng):
        m = translation(tuple(elem * leng for elem in self.xAxis)) # type: ignore
        self.coordinateVt = m.transform(self.coordinateVt)
        return self


    def roll(self, angle):
        xr = rotation(self.xAxis, angle)
        self.yAxis = xr.transform(self.yAxis)
        self.zAxis = xr.transform(self.zAxis)
        return self


    def pitch(self, angle):
        yr = rotation(self.yAxis, -angle)
        self.xAxis = yr.transform(self.xAxis)
        self.zAxis = yr.transform(self.zAxis)
        return self


    def turn(self, angle):
        zr = rotation(self.zAxis, angle)
        self.xAxis = zr.transform(self.xAxis)
        self.yAxis = zr.transform(self.yAxis)
        return self


    def pos(self):
        return self.coordinateVt
    

    def copy(self):
        t = Turtle()
        t.coordinateVt = self.coordinateVt
        t.xAxis = self.xAxis
        t.yAxis = self.yAxis
        t.zAxis = self.zAxis
        return t

def turtle_tree(leng, leng_scale1, leng_scale2, limit, turnAngle, rollAngle, line_diameter):
    _LINE_WORKPLANE = Workplane()
    _LINE_JOIN = _LINE_WORKPLANE.polyhedron(*tetrahedron(line_diameter / 2))
    def line(p1, p2):
        return _LINE_WORKPLANE.polylineJoin([p1, p2], _LINE_JOIN)

    def _turtle_tree(workplane, turtle, leng, leng_scale1, leng_scale2, limit, turnAngle, rollAngle):
        if leng > limit:
            workplane = workplane.add(
                line(turtle.pos(), turtle.forward(leng).pos())
            ) 

            workplane = _turtle_tree(
                workplane, 
                turtle.copy().turn(turnAngle), 
                leng * leng_scale1, 
                leng_scale1, 
                leng_scale2, 
                limit, 
                turnAngle, 
                rollAngle
            )

            return _turtle_tree(
                workplane, 
                turtle.copy().roll(rollAngle), 
                leng * leng_scale2, 
                leng_scale1, 
                leng_scale2, 
                limit, 
                turnAngle, 
                rollAngle
            )

        return workplane

    return _turtle_tree(
        Workplane(), 
        Turtle(), 
        leng, 
        leng_scale1, 
        leng_scale2, 
        limit, 
        turnAngle, 
        rollAngle
    ).combine()


leng = 20
limit = 1
leng_scale1 = 0.4
leng_scale2 = 0.9
turnAngle = 60
rollAngle = 135
line_diameter = 4


tree = turtle_tree(
    leng, 
    leng_scale1, 
    leng_scale2, 
    limit, 
    turnAngle, 
    rollAngle,
    line_diameter
)