import numpy as np
import matplotlib.pyplot as plt
import cv2

class Vector3:
    def __init__(self, x, y, z):
        self.v = (x, y, z)
    def norm(self):
        return np.sqrt(self.v[0]**2 + self.v[1]**2 + self.v[2]**2)
    def scale(self, length = 1):
        if length == 0:
            self.v = (0, 0, 0)
            return
        d = length / self.norm()
        if d == 0:
            return
        self.v = (self.v[0] * d, self.v[1] * d, self.v[2] * d)
    def values(self):
        return self.v
    def __add__(self, other):
        return (self.v[0] + other.v[0], self.v[1] + other.v[1], self.v[2] + other.v[2])
    def __mul__(self, n):
        return (self.v[0] * n, self.v[1] * n, self.v[2] * n)
    def __rmul__(self, n):
        return (self.v[0] * n, self.v[1] * n, self.v[2] * n)
    def __str__(self):
        return f"{self.v}"
    def dot(self, other):
        return self.v[0] * other.v[0] + self.v[1]* other.v[1] + self.v[2] * other.v[2]
    def cross(self, other):
        return (
            self.v[1] * other.v[2] - other.v[1] * self.v[2],
            self.v[2] * other.v[0] - other.v[2] * self.v[0],
            self.v[0] * other.v[1] - other.v[0] * self.v[1],
        )

class Vector3Object:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
    def scale(self, length = 1):
        if length == 0:
            self.x, self.y, self.z = 0, 0, 0
            return
        d = np.sqrt(self.x**2 + self.y**2 + self.z**2) / length
        if d == 0:
            return
        self.x, self.y, self.z = self.x / d, self.y / d, self.z / d
    def values(self):
        return self.x, self.y, self.z
    def __add__(self, other):
        return Vector3Object(self.x + other.x, self.y + other.y, self.z + other.z)
    def __mul__(self, n):
        return Vector3Object(self.x * n, self.y * n, self.z * n)
    def __rmul__(self, n):
        return Vector3Object(self.x * n, self.y * n, self.z * n)
    def __str__(self):
        return f"[{self.x}, {self.y}, {self.z}]"
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    def cross(self, other):
        return Vector3Object(
            self.y * other.z - other.y * self.z,
            self.z * other.x - other.z * self.x,
            self.x * other.y - other.x * self.y
        )

class CameraInterface:
    def __init__(self, width, height):
        self.image = [[(0, 0, 0)] * width for i in range(height)]
    def change_pixel(self, x, y, pixel):
        if type(pixel) == tuple and len(pixel) == 3:
            self.image[y][x] = pixel
        else:
            print("ERROR")
    def show(self):
        plt.imshow(self.image, vmin=0, vmax=255)
        plt.show()
        plt.clf()
    def save(self, name):
        plt.imshow(self.image, vmin=0, vmax=255)
        plt.savefig(f"{name}.png")
        plt.clf()
        # cv2.imwrite(name, np.array(self.image))

class Camera(CameraInterface):
    def __init__(self, direction = [1, 0, 0], width = 101, height = 101, x_fov = np.pi / 2, y_fov = np.pi / 2):
        """ Normalize """
        self.x, self.y, self.z = self.scale(direction)
        """ Store variables """
        self.width = width
        self.height = height
        self.right = np.tan(x_fov / 2)
        self.top = np.tan(y_fov / 2)
        """ Call super class """
        super().__init__(width, height)
    def field(self, x_shift = 0, y_shift = 0):
        """ Returns shifted ray direction in FOV (using plane 1 direction unit vector away) """
        if self.x == 0 and self.z == 0:
            h_shift = self.scale([1, 0, 0], length = self.right * x_shift / self.width)
            v_shift = self.scale([0, 0, -1], length = self.top * y_shift / self.height)
        else:
            h_shift = self.scale([self.z, 0, -self.x], length = self.right * x_shift / self.width)
            v_shift = self.scale([-self.x*self.y, self.x**2+self.z**2, -self.y*self.z], length = self.top * y_shift / self.height)
        return self.scale([self.x + h_shift[0] + v_shift[0], self.y + h_shift[1] + v_shift[1], self.z + h_shift[2] + v_shift[2]])
    @staticmethod
    def scale(direction, length = 1):
        if length == 0:
            return [0, 0, 0]
        x, y, z = direction
        d = np.sqrt(x**2 + y**2 + z**2) / length
        if d == 0:
            return [0, 0, 0]
        return [x/d, y/d, z/d]
    def point(self, d = [1, 0, 0]):
        self.x, self.y, self.z = self.scale(d)

class CameraVector3(CameraInterface):
    """
    Camera with a rectangular vision plane
    
    The horizontal, vertical, and depth (in/out of the screen) axes of the screen coordinate system horizontal correspond to the x, y, z axes of the camera coordinate system respectively.
    """
    def __init__(self, d = Vector3(1, 0, 0), w = 101, h = 101, x_fov = np.pi / 2, y_fov = np.pi / 2):
        """
        Initialize a camera pointing at direction *d*, with the screen width and height being *w* and *h* pixels in length. The field of view angles on the horizontal and vertical axes of the screen are *x_fov* and *y_fov* respectively.
        """
        # Normalize
        self.direction = d
        self.direction.scale()
        self.x, self.y, self.z = self.direction.values()
        # Store variables
        self.width, self.height = w, h
        self.right, self.top = np.tan(x_fov / 2), np.tan(y_fov / 2)
        # Initialize image
        super().__init__(w, h)
    def field(self, x_shift = 0, y_shift = 0):
        # Returns shifted ray direction in FOV (using plane 1 direction unit vector away)
        if self.x == 0 and self.z == 0:
            h_shift = Vector3(1, 0, 0)
            v_shift = Vector3(0, 0, -1)
        else:
            h_shift = Vector3(self.z, 0, -self.x)
            v_shift = Vector3(-self.x*self.y, self.x**2+self.z**2, -self.y*self.z)
        h_shift.scale(self.right * x_shift / self.width)
        v_shift.scale(self.top * y_shift / self.height)
        total_shift = self.direction + h_shift + v_shift
        total_shift.scale()
        return total_shift
    def point(self, d = Vector3(1, 0, 0)):
        self.direction = d
        self.direction.scale()
        self.x, self.y, self.z = self.direction.values()

class CameraSpherical(CameraInterface):
    def __init__(self, direction = Vector3(1, 0, 0), width = 101, height = 101, x_fov = np.pi / 2, y_fov = np.pi / 2):
        # Normalize
        direction.scale()
        x, y, z = direction.values()
        # Vertical angle
        self.tilt = np.arcsin(y)
        # Horizontal angle
        self.azimuth = np.arccos(x / np.cos(self.tilt))
        # Store variables
        self.width = width
        self.height = height
        self.x_fov = x_fov
        self.y_fov = y_fov
        # Initialize image
        super().__init__()
    def field(self, x_shift = 0, y_shift = 0):
        # Returns shifted ray direction in FOV
        azimuth = self.azimuth - x_shift / self.width * self.x_fov
        tilt = self.tilt + y_shift / self.height * self.y_fov
        x = np.cos(azimuth) * np.cos(tilt)
        z = np.sin(azimuth) * np.cos(tilt)
        y = np.sin(tilt)
        return Vector3(x, y, z)

class RayTracing:
    def __init__(self, ray_object_intersection):
        self.func = ray_object_intersection
        self.cam = Camera()
        self.matrix = []
        for i in range(self.cam.height):
            self.matrix.append([-1] * self.cam.width)
    def test(self, *args, show = True, save = False, name = "image"):
        halfWidth, halfHeight = self.cam.width // 2, self.cam.height // 2
        self.cam.point(args[1])
        for j in range(self.cam.height):
            y_shift = halfHeight - j
            row = self.matrix[j]
            for i in range(self.cam.width):
                x_shift = i - halfWidth
                args = list(args)
                args[1] = self.cam.field(x_shift=x_shift, y_shift=y_shift)
                args = tuple(args)
                row[i] = self.func(*args)
        matrix_min, matrix_max = np.inf, 0
        for j in range(self.cam.height):
            for i in range(self.cam.width):
                value = self.matrix[j][i]
                if value != -1:
                    if value < matrix_min:
                        matrix_min = value
                    elif value > matrix_max:
                        matrix_max = value
        m = 250 / (matrix_min - matrix_max)
        b = 5 - m * matrix_max
        for j in range(self.cam.height):
            row = self.cam.image[j]
            for i in range(self.cam.width):
                value = self.matrix[j][i]
                if value == -1:
                    row[i] = (0, 0, 0)
                else:
                    rgb = int(m * value + b)
                    row[i] = (rgb, rgb, rgb)
        if save:
            self.cam.save(name)
        if show:
            self.cam.show()
        return self.matrix
