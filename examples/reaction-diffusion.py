# scikit-image 0.18 or later is required.

from logging.config import valid_ident
import numpy as np
from skimage import measure
from cqmore import Workplane
from cadquery import exporters
from cqmore.polyhedron import gridSurface


def gray_scott(feel, kill, generation, space_size = 200, init_size = 20, init_u = 0.5, init_v = 0.25, Du = 2e-5, Dv = 1e-5, dx = 0.01, dt = 1):
    def laplacian(u):
        return (np.roll(u, 1, axis=0) + np.roll(u, -1, axis=0) +
                np.roll(u, 1, axis=1) + np.roll(u, -1, axis=1) - 4 * u) / (dx * dx)

    u = np.ones((space_size, space_size))
    v = np.zeros((space_size, space_size))

    half_space_size = space_size // 2
    half_init_size = init_size // 2
    square_low = half_space_size - half_init_size
    square_high = half_space_size + half_init_size

    u[square_low:square_high, square_low:square_high] = init_u
    v[square_low:square_high, square_low:square_high] = init_v

    u += np.random.rand(space_size, space_size) * 0.1
    v += np.random.rand(space_size, space_size) * 0.1

    for _ in range(generation):
        reaction = u * v * v
        dudt = Du * laplacian(u) - reaction + feel * (1 - u)
        dvdt = Dv * laplacian(v) + reaction - (feel + kill) * v
        u += dt * dudt
        v += dt * dvdt
 
    return u


def surface(u, amplitude = 1, thickness = 1):
    v = [[(float(x), float(y), float(d) * amplitude) for x, d in enumerate(r)] for y, r in enumerate(u)]
    return Workplane().polyhedron(*gridSurface(v, thickness))


def contours(u, space_size, density_threshold = .5, layer_h = 2, line_w = 2):
    all = Workplane()
    for contour in measure.find_contours(u, density_threshold):
        xs = contour[:, 1]
        ys = contour[:, 0]
        coords = [tuple(coord) for coord in np.dstack([xs, ys])[0]]
        scope = Workplane().polyline(coords).close()
        offset = Workplane().polyline(coords).close().offset2D(-line_w)
        all.add(scope.cut2D(offset).extrude(layer_h * 2))

    all = all.combine()
    return (Workplane().rect(space_size, space_size).extrude(layer_h)
                       .translate((space_size / 2, space_size / 2, -layer_h / 2))
                       .cut(all))


feel, kill = 0.04, 0.06      # amorphous
# feel, kill = 0.035, 0.065  # spots
# feel, kill = 0.012, 0.05   # wandering bubbles
# feel, kill = 0.025, 0.05   # waves
generation = 1000
space_size = 150

u = gray_scott(feel, kill, generation, space_size)
r = contours(u, space_size)
# r = surface(u, amplitude = 15)

# exporters.export(r, 'reaction-diffusion.stl')