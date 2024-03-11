import numpy as np

def shape0(origin, direction):
    """
    The object is a sphere centered at (0, 0, 0) with radius 1.
    """
    Ox, Oy, Oz = origin
    Dx, Dy, Dz = direction
    a = Dx ** 2 + Dy ** 2 + Dz ** 2
    b = 2 * (Ox * Dx + Oy * Dy + Oz * Dz)
    c = Ox ** 2 + Oy ** 2 + Oz ** 2 - 1
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return -1
    sqrt_disc = np.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2 * a)
    t2 = (-b + sqrt_disc) / (2 * a)
    if t1 < 0:
        if t2 < 0:
            return -1
        return t2
    return t1

def shape1(origin, direction):
    """
    The object is an axis-aligned unit cube with one corner at (0, 0, 0), and the opposite corner at (1, 1, 1), i.e. extending 1 unit on each axis.
    """
    # Helper function (check 0 <= n <= 1)
    def in_unit(n):
        return n >= 0 and n <= 1
    # Unpack tuples
    a, b, c = origin
    d, e, f = direction
    t_list = []
    if d != 0:
        # Plane x = 0
        t = -a / d
        if t > 0 and in_unit(b + t * e) and in_unit(c + t * f):
            t_list.append(t)
        # Plane x = 1
        t = (1 - a) / d
        if t > 0 and in_unit(b + t * e) and in_unit(c + t * f):
            t_list.append(t)
    if e != 0:
        # Plane y = 0
        t = -b / e
        if t > 0 and in_unit(a + t * d) and in_unit(c + t * f):
            t_list.append(t)
        # Plane y = 1
        t = (1 - b) / e
        if t > 0 and in_unit(a + t * d) and in_unit(c + t * f):
            t_list.append(t)
    if f != 0:
        # Plane z = 0
        t = -c / f
        if t > 0 and in_unit(a + t * d) and in_unit(b + t * e):
            t_list.append(t)
        # Plane z = 1
        t = (1 - c) / f
        if t > 0 and in_unit(a + t * d) and in_unit(b + t * e):
            t_list.append(t)
    if len(t_list) == 0:
        return -1
    else:
        return min(t_list)

def shape2(origin, direction):
    """
    The object is a square with the corners (0, 0, 0), (1, 0, 0), (1, 1, 0), and (0, 1, 0) in counterclockwise order.
    """
    # Helper function (check 0 <= n <= 1)
    def in_unit(n):
        return n >= 0 and n <= 1
    # Unpack tuples
    a, b, c = origin
    d, e, f = direction
    if f != 0:
        # Plane z = 0
        t = -c / f
        if t > 0 and in_unit(a + t * d) and in_unit(b + t * e):
            return t
    return -1

def shape3(origin, direction):
    """
    The object is a cylinder. The base of the cylinder is a circle with center (0, 0, 0) and radius 1. The cylinder aligns with the y-axis, and it has height 1 towards the positive y-axis, which means that the top of the cylinder is centered at (0, 1, 0) with radius 1.
    """
    # Helper function (check 0 <= n <= 1)
    def in_unit(n):
        return n >= 0 and n <= 1
    # Solve quadratic for t (O + tD and x^2 + z^2 = 1)
    Ox, Oy, Oz = origin
    Dx, Dy, Dz = direction
    a = Dx ** 2 + Dz ** 2
    b = 2 * (Ox * Dx + Oz * Dz)
    c = Ox ** 2 + Oz ** 2 - 1
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return -1
    sqrt_disc = np.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2 * a)
    t2 = (-b + sqrt_disc) / (2 * a)
    if t2 < 0:
        return -1
    y1 = Oy + Dy * t1
    y2 = Oy + Dy * t2
    if in_unit(y1):
        return t1
    if in_unit(y2) or (y1 > 0.5 and 0.5 > y2) or (y2 > 0.5 and 0.5 > y1):
        if y1 > y2:
            return (1 - Oy) / Dy
        else:
            return -Oy / Dy
    return -1

def shape4(origin, direction):
    """
    The object is a combination of two spheres fused together. The first sphere is centered at (0, 0, 0) with radius 1. The second sphere is centered (1, 0, 0) with radius 1.
    """
    origin2 = list(origin)
    origin2[0] = origin2[0] - 1
    origin2 = tuple(origin2)
    t1 = shape0(origin, direction)
    t2 = shape0(origin2, direction)
    if t1 == -1:
        if t2 == -1:
            return -1
        return t2
    if t2 == -1:
        return t1
    return min(t1, t2)

def shape5(origin, direction):
    """
    The object is a disc (2D circle in 3D space). The disc is centered at (0, 0, 0) with radius 1, and its normal is (1, 1, 1).
    """
    Ox, Oy, Oz = origin
    Dx, Dy, Dz = direction
    t = -(Ox + Oy + Oz) / (Dx + Dy + Dz)
    if t < 0:
        return -1
    Px, Py, Pz = Ox + t * Dx, Oy + t * Dy, Oz + t * Dz
    if Px ** 2 + Py ** 2 + Pz ** 2 > 1:
        return -1
    return t

def shape6(origin, direction):
    """
    The object is a quad with a circular hole. The quad is a trapezoid with the corners (1, 1, 1), (-1, 1, -1), (-2, -1, -2), and (2, -1, 2) in counterclockwise order. The circular hole is centered at (0, 0, 0) with radius 1. Light can pass through the circular hole but not the quad.
    """
    Ox, Oy, Oz = origin
    Dx, Dy, Dz = direction
    if Dx == Dz:
        return -1
    t = (Ox - Oz) / (Dz - Dx)
    if t < 0:
        return -1
    Py = Oy + t * Dy
    if Py < -1 or Py > 1:
        return -1
    Px, Pz = Ox + t * Dx, Oz + t * Dz
    lower_limit, upper_limit = 0.5 * Py - 1.5, -0.5 * Py + 1.5
    if Px < lower_limit or Px > upper_limit or Pz < lower_limit or Pz > upper_limit:
        return -1
    if Px ** 2 + Py ** 2 + Pz ** 2 < 1:
        return -1
    return t

def shape7(origin, direction):
    """
    The object is a plane with a triangular hole. The plane is y = z. The triangular hole has corners (1, 1, 1), (-1, 0, 0), and (0, -1, -1) in counterclockwise order. Light can pass through the triangular hole but not the plane.
    """
    Ox, Oy, Oz = origin
    Dx, Dy, Dz = direction
    if Dy == Dz:
        return -1
    t = (Oy - Oz) / (Dz - Dy)
    if t < 0:
        return -1
    Px, Py = Ox + t * Dx, Oy + t * Dy
    # Barycentric coordinates: p = p0 + (p1 - p0) * a + (p2 - p0) * b
    # p0 = (-1, 0, 0), p1 = (1, 1, 1), p2 = (0, -1, -1)
    a = (Px + Py + 1) / 3
    b = a - Py
    if a < 0 or a > 1 or b < 0 or b > 1 or a + b > 1:
        return t
    return -1

def shape8(origin, direction):
    """
    The object is an axis-aligned ellipsoid centered at (1, 1, 1). The length of its x, y, z semi-axes are 2, 3, 4 respectively. This object can be represented using the equation (x-1)^2/(2)^2 + (y-1)^2/(3)^2 + (z-1)^2/(4)^2 = 1
    """
    origin = ((origin[0] - 1) / 2, (origin[1] - 1) / 3, (origin[2] - 1) / 4)
    direction = (direction[0] / 2, direction[1] / 3, direction[2] / 4)
    return shape0(origin, direction)

def shape9(origin, direction):
    """
    The object is sphere cut by a plane. The sphere is centered at (0, 0, 0) with radius 1. The plane is x + y = 1. The smaller portion of the sphere is removed. The sphere is solid, hence the intersections between the ray and the cross-section at the cut need to be considered.
    """
    Ox, Oy, Oz = origin
    Dx, Dy, Dz = direction
    t = shape0(origin, direction)
    Px, Py, Pz = Ox + t * Dx, Oy + t * Dy, Oz + t * Dz
    if Px + Py > 1:
        # # This gives an interesting pattern due to floating point errors
        # if Px ** 2 + Py ** 2 + Pz ** 2 > 1:
        #     return -1
        if Dx == -Dy:
            return -1
        t = (1 - Ox - Oy) / (Dx + Dy)
        if t < 0:
            return -1
        Px, Py, Pz = Ox + t * Dx, Oy + t * Dy, Oz + t * Dz
        if Px ** 2 + Py ** 2 + Pz ** 2 > 1:
            return -1
        return t
    return t
