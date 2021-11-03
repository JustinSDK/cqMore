# `cqmore.matrix`

Provide the `Matrix3D` class and functions for performing matrix and vector operations. Here's an example to build a translation matrix for translating a point.

    from cqmore.matrix import translation

    point = (10, 10, 10)
    m = translation((10, 0, 0))    # return a Matrix3D instance
    new_point = m.transform(point) # (20, 10, 10)

`Matrix3D` supports matrix multiplication. You can combine multiple transformations in a single matrix. Say you have a point (10, 0, 0) and you want to translate it by (5, 0, 0) and then rotate it around the z-axis by 45 degrees. You can do it like:

    from cqmore.matrix import translation, rotationZ

    point = (10, 0, 0)
    m = rotationZ(45) @ translation((5, 0, 0))
    new_point = m.transform(point) 

The right-most matrix is first multiplied with the point so you should read the multiplications from right to left. 

## Classes

 Signature | Description
--|--
`Matrix3D(m)` | Define a 4x4 matrix for 3D transformation.

## `Matrix3D` Operations

 Signature | Description
--|--
`transform(point)` | Transform a point.
`transformAll(points)` | Transform a list of points.


## Functions

 Signature | Description
--|--
`identity()` | Create an identity matrix.
`scaling(v)` | Create a scaling matrix.
`translation(v)` | Create a translation matrix.
`mirror(v)` | Create a mirror matrix.
`rotationX(angle)` | Create an rotation matrix around the x-axis.
`rotationY(angle)` | Create an rotation matrix around the y-axis.
`rotationZ(angle)` | Create an rotation matrix around the z-axis.
`rotation(direction, angle)` | Create an rotation matrix around the given direction.

----

## Under construction
