# scikit-image 0.18 or later is required.

import numpy as np
from skimage import measure
from cqmore import Workplane
from cadquery import exporters

def gray_scott(feel, kill, generation, space_size = 200, init_size = 20, dx = 0.01, dt = 1):
    Du = 2e-5
    Dv = 1e-5

    u = np.ones((space_size, space_size))
    v = np.zeros((space_size, space_size))

    half_space_size = space_size // 2
    half_init_size = init_size // 2
    square_low = half_space_size - half_init_size
    square_high = half_space_size + half_init_size

    u[square_low:square_high, square_low:square_high] = 0.5
    v[square_low:square_high, square_low:square_high] = 0.25

    u += np.random.rand(space_size, space_size) * 0.1
    v += np.random.rand(space_size, space_size) * 0.1

    for _ in range(generation):
        laplacian_u = (np.roll(u, 1, axis=0) + np.roll(u, -1, axis=0) +
                        np.roll(u, 1, axis=1) + np.roll(u, -1, axis=1) - 4 * u) / (dx * dx)
        laplacian_v = (np.roll(v, 1, axis=0) + np.roll(v, -1, axis=0) +
                        np.roll(v, 1, axis=1) + np.roll(v, -1, axis=1) - 4 * v) / (dx * dx)

        dudt = Du * laplacian_u - u * v * v + feel * (1 - u)
        dvdt = Dv * laplacian_v + u * v * v - (feel + kill) * v
        u += dt * dudt
        v += dt * dvdt
 
    return u

feel, kill = 0.04, 0.06      # amorphous
# feel, kill = 0.035, 0.065  # spots
# feel, kill = 0.012, 0.05   # wandering bubbles
# feel, kill = 0.025, 0.05   # waves
generation = 2500
density_threshold = .5
layer_h = 2
line_w = 2
space_size = 200

contours = measure.find_contours(
    gray_scott(feel, kill, generation, space_size), 
    density_threshold
)

all = Workplane()
for contour in contours:
    xs = contour[:, 1]
    ys = contour[:, 0]
    coords = [tuple(coord) for coord in np.dstack([xs, ys])[0]]
    scope = Workplane().polyline(coords).close()
    offset = Workplane().polyline(coords).close().offset2D(-line_w)
    all.add(scope.cut2D(offset).extrude(layer_h * 2))

all = all.combine()
output = (Workplane().rect(space_size, space_size).extrude(layer_h)
                     .translate((space_size / 2, space_size / 2, -layer_h / 2))
                     .cut(all))

show_object(output) # type: ignore

# exporters.export(
#     output, 
#     'reaction-diffusion.stl'
# )