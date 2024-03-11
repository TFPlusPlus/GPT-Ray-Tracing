import gpt4
import json

LANGUAGES = [
    "Python",
    "C++",
]

SHAPES = [
    "Sphere",
    "Cube",
    "Square",
    "Cylinder",
    "Two Spheres",
    "Disc",
    "Quad with Circle Hole",
    "Plane with Triangle Hole",
    "Ellipsoid",
    "Cut Sphere",
]

DESCRIPTIONS = [
    "The object is a sphere centered at (0, 0, 0) with radius 1.",
    "The object is an axis-aligned unit cube with one corner at (0, 0, 0), and the opposite corner at (1, 1, 1), i.e. extending 1 unit on each axis.",
    "The object is a square with the corners (0, 0, 0), (1, 0, 0), (1, 1, 0), and (0, 1, 0) in counterclockwise order.",
    "The object is a cylinder. The base of the cylinder is a circle with center (0, 0, 0) and radius 1. The cylinder aligns with the y-axis, and it has height 1 towards the positive y-axis, which means that the top of the cylinder is centered at (0, 1, 0) with radius 1.",
    "The object is a combination of two spheres fused together. The first sphere is centered at (0, 0, 0) with radius 1. The second sphere is centered (1, 0, 0) with radius 1.",
    "The object is a disc (2D circle in 3D space). The disc is centered at (0, 0, 0) with radius 1, and its normal is (1, 1, 1).",
    "The object is a quad with a circular hole. The quad is a trapezoid with the corners (1, 1, 1), (-1, 1, -1), (-2, -1, -2), and (2, -1, 2) in counterclockwise order. The circular hole is centered at (0, 0, 0) with radius 1. Light can pass through the circular hole but not the quad.",
    "The object is a plane with a triangular hole. The plane is y = z. The triangular hole has corners (1, 1, 1), (-1, 0, 0), and (0, -1, -1) in counterclockwise order. Light can pass through the triangular hole but not the plane.",
    "The object is an axis-aligned ellipsoid centered at (1, 1, 1). The length of its x, y, z semi-axes are 2, 3, 4 respectively. This object can be represented using the equation (x-1)^2/(2)^2 + (y-1)^2/(3)^2 + (z-1)^2/(4)^2 = 1",
    "The object is a sphere cut by a plane. The sphere is centered at (0, 0, 0) with radius 1. The plane is x + y = 1. The smaller portion of the sphere is removed. The sphere is solid, hence the intersections between the ray and the cross-section at the cut need to be considered.",
]

file = open("dump.txt", "w")
res = []

for j in range(len(LANGUAGES)):
    for k in range(len(SHAPES)):
        language = LANGUAGES[j]
        shape = SHAPES[k]
        description = DESCRIPTIONS[k]
        res.append([])
        for i in range(10):
            if shape[0] == "E":
                try:
                    response = gpt4.ask_system(
                        "You are an instructor for an introductory Computer Graphics course in a university. You are currently writing Ray-Object Intersection exercises for an upcoming assessment related to Ray Tracing.",
                        f"Please provide a model solution in {language} for the following Ray-Object Intersection programming question. Please only include the function definition and no other text in the response.\n\nIn this exercise you need to write a function computing the intersection between a ray and an {shape} in a 3D scene.\nThe ray is defined by its origin O and direction D, and it is represented as R(t) = O + tD, where t is a scalar indicating the distance of a point from the ray origin. The function takes two parameters: 'O' for ray origin and 'D' for ray direction. They are both tuples of 3 floats in the form of (x, y, z). The function returns a float 't'. If an intersection exists, then 't' is the distance from the ray origin to the closest intersection. If no intersections exist, then 't' is -1 indicating the lack of intersections.\n{description}\nYou may assume that the ray always starts outside the object, and points where the ray grazes the object at one single point are considered as intersections.",
                        0.75
                    )
                except:
                    response = "ERROR"
            else:
                try:
                    response = gpt4.ask_system(
                        "You are an instructor for an introductory Computer Graphics course in a university. You are currently writing Ray-Object Intersection exercises for an upcoming assessment related to Ray Tracing.",
                        f"Please provide a model solution in {language} for the following Ray-Object Intersection programming question. Please only include the function definition and no other text in the response.\n\nIn this exercise you need to write a function computing the intersection between a ray and a {shape} in a 3D scene.\nThe ray is defined by its origin O and direction D, and it is represented as R(t) = O + tD, where t is a scalar indicating the distance of a point from the ray origin. The function takes two parameters: 'O' for ray origin and 'D' for ray direction. They are both tuples of 3 floats in the form of (x, y, z). The function returns a float 't'. If an intersection exists, then 't' is the distance from the ray origin to the closest intersection. If no intersections exist, then 't' is -1 indicating the lack of intersections.\n{description}\nYou may assume that the ray always starts outside the object, and points where the ray grazes the object at one single point are considered as intersections.",
                        0.75
                    )
                except:
                    response = "ERROR"
            res[-1].append(response)

json.dump(res, file, indent=4)