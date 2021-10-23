from math import sin, cos, tau
from typing import Any, Callable, Union

from .cq_typing import Point2D, Point3D

def circle(t: float, radius: float) -> Point2D:
    theta = t * tau
    return (radius * cos(theta), radius * sin(theta))


def helix(t: float, radius: float, slope: float) -> Point3D:
    theta = t * tau
    return (radius * cos(theta), radius * sin(theta), radius * slope * t)


def torusKnot(t: float, p: int, q: int) -> Point3D:
    phi = t * tau
    q_phi = q * phi
    p_phi = p * phi
    r = cos(q_phi) + 2
    return (r * cos(p_phi), r * sin(p_phi), -sin(q_phi))


def parametricEquation(f: Callable[..., Union[Point2D, Point3D]], *args: Any, **kwargs: Any) -> Callable[[float], Union[Point2D, Point3D]]:
    return lambda t: f(t, *args, **kwargs)
