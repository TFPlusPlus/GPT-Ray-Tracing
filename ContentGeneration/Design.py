import gpt4
import json

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
file = open("dump.txt", "w")
res = []

# print("#####")
for j in range(len(SHAPES)):
    shape = SHAPES[j]
    res.append([])
    for i in range(10):
        if shape[0] == "E":
            try:
                response = gpt4.ask_system(
                    "You are an instructor for an introductory Computer Graphics course in an university. You are currently writing Ray-Object Intersection exercises for an upcoming assessment related to Ray Tracing.",
                    f"Please write a Ray-Object Intersection programming question using an {shape}. Please use clear wording and avoid discrepancies in the solutions. Please ensure that any descriptions of the object correspond to the object uniquely.",
                    0.75
                )
            except:
                response = "ERROR"
        else:
            try:
                response = gpt4.ask_system(
                    "You are an instructor for an introductory Computer Graphics course in an university. You are currently writing Ray-Object Intersection exercises for an upcoming assessment related to Ray Tracing.",
                    f"Please write a Ray-Object Intersection programming question using a {shape}. Please use clear wording and avoid discrepancies in the solutions. Please ensure that any descriptions of the object correspond to the object uniquely.",
                    0.75
                )
            except:
                response = "ERROR"
        # print(f"{j}.{i}")
        # print(response)
        # print("\n#####")
        res[-1].append(response)

json.dump(res, file, indent=4)