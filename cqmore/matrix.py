"""
Provide the `Matrix3D` class and functions for performing matrix and vector operations. 
Here's an example to build a translation matrix for translating a point.

    from cqmore.matrix import translation

    point = (10, 10, 10)
    m = translation((10, 0, 0))    # return a Matrix3D instance
    new_point = m.transform(point) # (20, 10, 10)

`Matrix3D` supports matrix multiplication. You can combine multiple transformations in 
a single matrix. Say you have a point (10, 0, 0) and you want to translate it by (5, 0, 0)
and then rotate it around the z-axis by 45 degrees. You can do it like:

    from cqmore.matrix import translation, rotationZ

    point = (10, 0, 0)
    m = rotationZ(45) @ translation((5, 0, 0))
    new_point = m.transform(point) 

The right-most matrix is first multiplied with the point so you should read the 
multiplications from right to left. 

"""

from typing import Iterable, Union, cast

from cadquery import Vector

from ._typing import Point3D

from math import cos, sin, radians
import numpy


class Matrix3D:
    def __init__(self, m: Iterable[Iterable[float]]):
        '''
        Create a matrix from an array-like object.

        ## Parameters

        - `m`: an array-like object.

        ## Examples 

            from cqmore.matrix import Matrix3D

            v = (5, 5, 5)

            # Create a translation matrix
            translation = Matrix3D([
                [1, 0, 0, v[0]],
                [0, 1, 0, v[1]],
                [0, 0, 1, v[2]],
                [0, 0, 0, 1]
            ])

        '''

        if isinstance(m, numpy.ndarray):
            self.wrapped = m
        else:
            self.wrapped = numpy.array(m)


    def __matmul__(self, that: 'Matrix3D') -> 'Matrix3D':
        return Matrix3D(self.wrapped @ that.wrapped)


    def transform(self, point: Union[Point3D, Vector]) -> Point3D:
        '''
        Use the current matrix to transform a point.

        ## Parameters

        - `point`: the point to transform.

        ## Examples 

            from cqmore.matrix import Matrix3D

            translation = Matrix3D([
                [1, 0, 0, 5],
                [0, 1, 0, 5],
                [0, 0, 1, 5],
                [0, 0, 0, 1]
            ])

            point = (10, 20, 30)
            translated = translation.transform(point) # (15, 25, 35)

        '''

        vt = (point.x, point.y, point.z, 1) if isinstance(point, Vector) else point + (1,)
        return cast(Point3D, tuple((self.wrapped @ vt))[:-1])


    def transformAll(self, points: Union[Iterable[Point3D], Iterable[Vector]]) -> tuple[Point3D]:
        '''
        Use the current matrix to transform a list of points.

        ## Parameters

        - `points`: a list of points to transform.

        ## Examples 

            from cqmore.matrix import Matrix3D

            translation = Matrix3D([
                [1, 0, 0, 5],
                [0, 1, 0, 5],
                [0, 0, 1, 5],
                [0, 0, 0, 1]
            ])

            points = [(10, 20, 30), (0, 0, 0), (-10, -20, -30)]

            # ((15, 25, 35), (5, 5, 5), (-5, -15, -25))
            translated = translation.transformAll(points) 

        '''

        it = iter(points)
        if isinstance(next(it), Vector):
            r = (tuple((self.wrapped @ (v.x, v.y, v.z, 1)))[:-1] for v in cast(Iterable[Vector], points))
        else:
            r = (tuple((self.wrapped @ (p + (1,))))[:-1] for p in cast(Iterable[Point3D], points))
        
        return cast(tuple[Point3D], tuple(r))
        

_identity = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

def identity() -> Matrix3D:
    '''
    Create an identity matrix.

    ## Examples 

        from cqmore.matrix import identity

        m = identity()

    '''

    return Matrix3D(numpy.array(_identity))


def scaling(v: Union[Point3D, Vector]) -> Matrix3D:
    '''
    Create a scaling matrix.

    ## Parameters

    - `v`: scaling vector.

    ## Examples 

        from cqmore.matrix import scaling
        from cqmore.polyhedron import uvSphere
        from cqmore import Workplane

        sphere = uvSphere(1, widthSegments = 12, heightSegments = 6)

        m = scaling((2, 1, 1)) 
        scaled_points = m.transformAll(sphere.points)

        r = Workplane().polyhedron(scaled_points, sphere.faces)

    '''

    return Matrix3D(_scaling(v))


def translation(v: Union[Point3D, Vector]) -> Matrix3D:
    '''
    Create a translation matrix.

    ## Parameters

    - `v`: translation vector.

    ## Examples 

        from cqmore.matrix import scaling, translation
        from cqmore.polyhedron import uvSphere
        from cqmore import Workplane

        sphere = uvSphere(1, widthSegments = 12, heightSegments = 6)

        r1 = Workplane().polyhedron(*sphere)
        s = scaling((2, 2, 2)) 
        t = translation((3, 0, 0))

        transformed_pts = (t @ s).transformAll(sphere.points)
        r2 = Workplane().polyhedron(transformed_pts, sphere.faces)

    '''

    return Matrix3D(_translation(v))


def mirror(v: Union[Point3D, Vector]) -> Matrix3D:
    '''
    Create a mirror matrix.

    ## Parameters

    - `v`: mirror vector.

    ## Examples 

        from cqmore.matrix import mirror, translation
        from cqmore.polyhedron import tetrahedron
        from cqmore import Workplane

        t = tetrahedron(1)

        pts = translation((1, 0, 0)).transformAll(t.points)
        r1 = Workplane().polyhedron(pts, t.faces)

        mirrored_pts = mirror((1, 0, 0)).transformAll(pts)
        r2 = Workplane().polyhedron(mirrored_pts, t.faces)

    '''

    return Matrix3D(_mirror(v))


def rotationX(angle: float) -> Matrix3D:
    '''
    Create a rotation matrix around the x-axis.

    ## Parameters

    - `angle`: angle degrees.

    ## Examples 

        from cqmore.matrix import translation, rotationX
        from cqmore.polyhedron import tetrahedron
        from cqmore import Workplane

        t = tetrahedron(1)
        pts = translation((0, 3, 0)).transformAll(t.points)

        for a in range(0, 360, 30):
            rotated_pts = rotationX(a).transformAll(pts)
            show_object(Workplane().polyhedron(rotated_pts, t.faces))

    '''

    return Matrix3D(_rotationX(angle))


def rotationY(angle: float) -> Matrix3D:
    '''
    Create a rotation matrix around the y-axis.

    ## Parameters

    - `angle`: angle degrees.

    ## Examples 

        from cqmore.matrix import translation, rotationY
        from cqmore.polyhedron import tetrahedron
        from cqmore import Workplane

        t = tetrahedron(1)

        for i in range(20):
            rotated_pts = (rotationY(i * 36) @ translation((3, i, 0))).transformAll(t.points)
            show_object(Workplane().polyhedron(rotated_pts, t.faces))

    '''

    return Matrix3D(_rotationY(angle))


def rotationZ(angle: float) -> Matrix3D:
    '''
    Create a rotation matrix around the z-axis.

    ## Parameters

    - `angle`: angle degrees.

    ## Examples 

        from cqmore import Workplane
        from cqmore.matrix import translation, rotationX, rotationZ
        from cqmore.polyhedron import sweep

        def mobius_strip(radius, frags):
            profile = [(10, -1, 0), (10, 1, 0), (-10, 1, 0), (-10, -1, 0)]

            translationX20 = translation((radius, 0, 0))
            rotationX90 = rotationX(90)

            angle_step = 360 / frags
            profiles = []
            for i in range(frags):
                m = rotationZ(i * angle_step) @ translationX20 @ rotationX90 @ rotationZ(i * angle_step / 2)
                profiles.append(m.transformAll(profile))

            return Workplane().polyhedron(*sweep(profiles, closeIdx = 2))

        radius = 20
        frags = 24

        strip = mobius_strip(radius, frags)

    '''
    
    return Matrix3D(_rotationZ(angle))


def rotation(direction: Union[Point3D, Vector], angle: float) -> Matrix3D:
    '''
    Create a rotation matrix around the given direction.

    ## Parameters

    - `direction`: axis of rotation.
    - `angle`: angle degrees.

    ## Examples 

        from cqmore.matrix import rotation, translation, rotationY
        from cqmore.polyhedron import tetrahedron
        from cqmore import Workplane

        t = tetrahedron(1)
        pts = translation((6, 6, 3)).transformAll(t.points)
        direction = (10, 10, 10)

        for a in range(0, 360, 30):
            rotated_pts = rotation(direction, a).transformAll(pts)
            show_object(Workplane().polyhedron(rotated_pts, t.faces))

        show_object(
            Workplane().polylineJoin(
                [(0, 0, 0), direction], 
                Workplane().box(.1, .1, .1)
            )
        )

    '''

    return Matrix3D(_rotation(direction, angle))


def _scaling(v: Union[Point3D, Vector]) -> numpy.ndarray:
    vt = (v.x, v.y, v.z) if isinstance(v, Vector) else v
    return numpy.array([
        [vt[0], 0, 0, 0],
        [0, vt[1], 0, 0],
        [0, 0, vt[2], 0],
        [0, 0, 0, 1]
    ]) 


def _translation(v: Union[Point3D, Vector]) -> numpy.ndarray:
    vt = (v.x, v.y, v.z) if isinstance(v, Vector) else v
    return numpy.array([
        [1, 0, 0, vt[0]],
        [0, 1, 0, vt[1]],
        [0, 0, 1, vt[2]],
        [0, 0, 0, 1]
    ]) 


def _mirror(v: Union[Point3D, Vector]) -> numpy.ndarray:
    vt = (v if isinstance(v, Vector) else Vector(*v)).normalized()
    txx = -2* vt.x * vt.x
    txy = -2* vt.x * vt.y
    txz = -2* vt.x * vt.z
    tyy = -2* vt.y * vt.y
    tyz = -2* vt.y * vt.z
    tzz = -2* vt.z * vt.z

    return numpy.array([
        [1 + txx, txy, txz, 0],
        [txy, 1 + tyy, tyz, 0],
        [txz, tyz, 1 + tzz, 0],
        [0, 0, 0, 1]
    ]) 


def _rotationX(angle: float) -> numpy.ndarray:
    rad = radians(angle)
    c = cos(rad)
    s = sin(rad)
    return numpy.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ]) 


def _rotationY(angle: float) -> numpy.ndarray:
    rad = radians(angle)
    c = cos(rad)
    s = sin(rad)
    return numpy.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ]) 


def _rotationZ(angle: float) -> numpy.ndarray:
    rad = radians(angle)
    c = cos(rad)
    s = sin(rad)
    return numpy.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]) 


# Quaternions and spatial rotation
def _rotation(direction: Union[Point3D, Vector], angle: float) -> numpy.ndarray:
    dir = direction if isinstance(direction, Vector) else Vector(*direction)
    axis = dir.normalized()
    half_a = radians(angle / 2)
    s = sin(half_a)
    x = s * axis.x
    y = s * axis.y
    z = s * axis.z
    w = cos(half_a)
    x2 = x + x
    y2 = y + y
    z2 = z + z
    xx = x * x2
    yx = y * x2
    yy = y * y2
    zx = z * x2
    zy = z * y2
    zz = z * z2
    wx = w * x2
    wy = w * y2
    wz = w * z2  
    return numpy.array([
        [1 - yy - zz, yx - wz, zx + wy, 0],
        [yx + wz, 1 - xx - zz, zy - wx, 0],
        [zx - wy, zy + wx, 1 - xx - yy, 0],
        [0, 0, 0, 1]
    ]) 

