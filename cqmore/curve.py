"""
Provide parametric equations of curves.

"""

from math import sin, cos, tau, pi, e, log, sqrt
from typing import Any, Callable, Union

from ._typing import Point2D, Point3D


def circle(t: float, radius: float) -> Point2D:
    '''
    The parametric equation of a circle.

    ## Parameters

    - `t`: a parametric variable in the range 0 to 1.
    - `radius`: the circle radius. 

    ## Examples 

        from cqmore import Workplane
        from cqmore.curve import circle

        radius = 1

        c = (Workplane()
                .parametricCurve(lambda t: circle(t, radius))
                .center(radius * 3, 0)
                .polyline([circle(t / 10, radius) for t in range(6)]).close()
                .extrude(1)
            )

    '''
    
    theta = t * tau
    return (radius * cos(theta), radius * sin(theta))


def logarithmicSpiral(t: float, a: float = 1, k: float = 0.306349) -> Point2D:
    '''
    The parametric equation of a [logarithmic spiral](https://en.wikipedia.org/wiki/Logarithmic_spiral). 
    Default to a golden spiral.

    ## Parameters

    - `t`: as it increases, the point traces a right-handed spiral about the z-axis, 
           in a right-handed coordinate system.
    - `a`: the a parameter of the logarithmic spiral. 
    - `k`: the k parameter of the logarithmic spiral. 

    ## Examples 

        from cqmore import Workplane
        from cqmore.curve import logarithmicSpiral

        spiral = (Workplane()
                    .polyline([logarithmicSpiral(t / 360) for t in range(360 * 5)])
                 )

    '''

    theta = t * tau
    r = a * e ** (k * theta)
    return (r * cos(theta), r * sin(theta))
    

def archimedeanSpiral(t: float, a: float, b: float) -> Point2D:
    '''
    The parametric equation of a [archimedean spiral](https://en.wikipedia.org/wiki/Archimedean_spiral). 

    ## Parameters

    - `t`: as it increases, the point traces a right-handed spiral about the z-axis, 
           in a right-handed coordinate system.
    - `a`: move the centerpoint of the spiral outward from the origin. 
    - `b`: control the distance between loops.

    ## Examples 

        from cqmore import Workplane
        from cqmore.curve import archimedeanSpiral

        spiral = (Workplane()
                    .polyline([archimedeanSpiral(t / 360, 1, 1) for t in range(360 * 5)])
                )

    '''

    theta = t * tau
    r = a + b * theta
    return (r * cos(theta), r * sin(theta))


def helix(t: float, radius: float, slope: float) -> Point3D:
    '''
    The parametric equation of a helix.

    ## Parameters

    - `t`: as it increases, the point traces a right-handed helix about the z-axis, 
           in a right-handed coordinate system.
    - `radius`: the helix radius. 
    - `slope `: the helix slope. 

    ## Examples 

        from cqmore import Workplane
        from cqmore.curve import helix

        radius = 1
        slope = 1

        c = (Workplane()
                .parametricCurve(lambda t: helix(t, radius, slope), stop = 3)
            )

    '''

    theta = t * tau
    return (radius * cos(theta), radius * sin(theta), radius * slope * t)


def sphericalSpiral(t: float, radius: float, c: float = 2) -> Point3D:
    '''
    The parametric equation of a [spherical spiral](https://en.wikipedia.org/wiki/Spiral#Spherical_spirals).

    ## Parameters

    - `t`: a parametric variable in the range 0 to 1.
    - `radius`: the sphere radius. 
    - `c `: equal to twice the number of turns. 

    ## Examples 

        from cqmore import Workplane
        from cqmore.curve import sphericalSpiral

        radius = 10
        c = 10

        spiral = (Workplane()
                    .parametricCurve(lambda t: sphericalSpiral(t, radius, c))
                )

    '''

    theta = t * pi
    sinTheta = sin(theta)
    cosTheta = cos(theta)
    sinCTheta = sin(c * theta)
    cosCTheta = cos(c * theta)
    return (
               radius * sinTheta * cosCTheta, 
               radius * sinTheta * sinCTheta,
               radius * cosTheta
           )


def torusKnot(t: float, p: int, q: int) -> Point3D:
    '''
    The parametric equation of a [torus knot](https://en.wikipedia.org/wiki/Torus_knot).

    ## Parameters

    - `t`: a parametric variable in the range 0 to 1.
    - `p`: the p parameter of the (p,q)-torus knot.
    - `q`: the q parameter of the (p,q)-torus knot.

    ## Examples 

        from cqmore import Workplane
        from cqmore.curve import torusKnot

        p = 11
        q = 13

        c = (Workplane()
                .polyline([torusKnot(t / 360, p, q) for t in range(360)])
                .close()
            )

    '''

    phi = t * tau
    q_phi = q * phi
    p_phi = p * phi
    r = cos(q_phi) + 2
    return (r * cos(p_phi), r * sin(p_phi), -sin(q_phi))


def superformula(t: float, m: float, n1: float, n2: float, n3: float, a: float = 1, b: float = 1) -> Point2D:
    '''
    The parametric equation of a [superformula](https://en.wikipedia.org/wiki/Superformula).

    ## Parameters

    - `t`: a parametric variable in the range 0 to 1.
    - `m`: the m parameter of the superformula.
    - `n1`: the n1 parameter of the superformula.
    - `n2`: the n2 parameter of the superformula.
    - `n3`: the n3 parameter of the superformula.
    - `a = 1`: the a parameter of the superformula.
    - `b = 1`: the b parameter of the superformula.
    

    ## Examples 

        from cqmore import Workplane
        from cqmore.curve import superformula

        params = [
            [3, 4.5, 10, 10],
            [4, 12, 15, 15],
            [7, 10, 6, 6],
            [5, 4, 4, 4],
            [5, 2, 7, 7]
        ]

        r1 = Workplane()
        for i in range(5):
            r1 = (r1.center(4, 0)
                    .parametricCurve(lambda t: superformula(t, *params[i]))
                    .extrude(1)
                 )

    '''

    phi = t * tau
    r = pow(
        pow(abs(cos(m * phi / 4) / a), n2) + 
        pow(abs(sin(m * phi / 4) / b), n3),
        - 1 / n1    
    )
    return (r * cos(phi), r * sin(phi))


def parametricEquation(func: Callable[..., Union[Point2D, Point3D]], *args: Any, **kwargs: Any) -> Callable[[float], Union[Point2D, Point3D]]:
    '''
    Convert `func` into a function f(t) used by `Workplane.parametricCurve`.

    ## Parameters

    - `func`: the parametric equation of a curve.
    - `*args`: the positional arguments.
    - `**kwargs`: the keyword arguments.

    ## Examples 

        from cqmore import Workplane
        from cqmore.curve import torusKnot, parametricEquation

        p = 4
        q = 9

        c = (Workplane()
                .parametricCurve(parametricEquation(torusKnot, p = p, q = q))
            )

    '''

    return lambda t: func(t, *args, **kwargs)
