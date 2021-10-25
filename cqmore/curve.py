"""
Provide parametric equations of curves.

"""

from math import sin, cos, tau, pi, e, log, sqrt
from typing import Any, Callable, Union

from .cq_typing import Point2D, Point3D

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
    coef = a * e ** (k * theta)
    return (coef * cos(theta), coef * sin(theta))
    

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
