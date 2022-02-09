# numpy-stl 2.16 or later is required.
from stl.mesh import Mesh
from cqmore import Workplane

def import_stl(fileName):
    vectors = Mesh.from_file(fileName).vectors
    points = tuple(map(tuple, vectors.reshape((vectors.shape[0] * vectors.shape[1], 3))))
    faces = [(i, i + 1, i + 2) for i in range(0, len(points), 3)]
    return Workplane().polyhedron(points, faces)

stl = import_stl('yourfile.stl')