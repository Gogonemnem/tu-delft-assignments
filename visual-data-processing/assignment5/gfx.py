from numba import jit, njit
import numba
import numpy as np
import math
from numba.experimental import jitclass

vec3_type = numba.float32[:]
@njit
def make_vec3_f32(input_maybe_f64):
    return np.array([input_maybe_f64[0], input_maybe_f64[1], input_maybe_f64[2]], np.float32)

@njit
def Vec3(x, y, z):
    return np.array([x, y, z], np.float32)

@njit
def Vec2(x, y):
    return np.array([x, y], np.float32)

@njit
def normalize(v):
    return v / np.linalg.norm(v)


@njit
def cross(a, b):
    return Vec3(
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0])

@njit
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


sphere_spec = [
    ("__center", vec3_type),
    ("__radius2", numba.float32)
]
@jitclass(sphere_spec)
class Sphere:
    def __init__(self, center, radius):
        self.__center = center
        self.__radius2 = radius * radius

    def intersect(self, ray):
        origin, direction = ray

        L = self.__center - origin
        tca = dot(L, direction)
        d2 = dot(L, L) - tca * tca
        if d2 > self.__radius2:
            return None

        thc = math.sqrt(self.__radius2 - d2)
        t0 = tca - thc
        t1 = tca + thc

        if t0 > t1:
            tmp = t0
            t0 = t1
            t1 = t0

        hit_pos = origin + t0 * direction
        hit_normal = normalize(hit_pos - self.__center)
        return (t0, hit_pos, hit_normal)


camera_spec = [
    ("__position", vec3_type),
    ("__forward", vec3_type),
    ("__right", vec3_type),
    ("__up", vec3_type),
    ("__tan_fovy", numba.float32),
    ("__tan_fovx", numba.float32),
]
@jitclass(camera_spec)
class Camera:
    def __init__(self, position, lookat, up, fovy_degrees, aspect):
        fovy_radians = math.radians(fovy_degrees)
        self.__position = position
        self.__forward = normalize(lookat - position)
        self.__right = cross(normalize(up), self.__forward)
        self.__up = cross(self.__forward, self.__right)

        self.__tan_fovy = math.tan(fovy_radians / 2)
        fovx_radians = aspect * fovy_radians
        self.__tan_fovx = math.tan(fovx_radians / 2)

    def ray_through_pixel(self, x, y):
        direction = self.__forward.copy()
        direction += self.__right * (x * 2 - 1) * self.__tan_fovx
        direction += self.__up * (y * 2 - 1) * self.__tan_fovy
        direction = normalize(direction)
        return (self.__position, direction)

    @property
    def position(self):
        return self.__position


point_light_spec = [
    ("__position", vec3_type),
    ("__intensity", vec3_type),
]
@jitclass(point_light_spec)
class PointLight:
    def __init__(self, position, intensity):
        self.__position = position
        self.__intensity = intensity

    def light_at_point(self, point):
        light_vec = self.__position - point
        dist2 = dot(light_vec, light_vec)
        return (normalize(light_vec), self.__intensity / dist2)


directional_light_spec = [
    ("__out_direction", vec3_type),
    ("__intensity", vec3_type),
]
@jitclass(directional_light_spec)
class DirectionalLight:
    def __init__(self, direction, intensity):
        self.__out_direction = -normalize(direction)
        self.__intensity = intensity

    def light_at_point(self, point):
        return (self.__out_direction, self.__intensity)


@njit
def reflect(N, L):
    return (2*N*dot(L, N) - L).astype(np.float32)


@jitclass([("__diffuse", vec3_type)])
class LambertBRDF:
    def __init__(self, diffuse):
        self.__diffuse = np.float32(diffuse)

    def evaluate(self, N, L, V):  # N = normal, L = light, E = eye
        return self.__diffuse * dot(N, L)


@jitclass([("__diffuse", vec3_type), ("__specular", vec3_type), ("__shininess", numba.float32)])
class PhongBRDF:
    def __init__(self, diffuse, specular, shininess):
        # Sanitize input to hopefully prevent np.float64 errors
        self.__diffuse = make_vec3_f32(diffuse)
        self.__specular = make_vec3_f32(specular)
        self.__shininess = numba.float32(shininess)

    def evaluate(self, N, L, V):  # N = normal, L = light, V = view
        R = reflect(N, L)

        diffuse = self.__diffuse * dot(N, L)
        specular = self.__specular * \
            np.float32(max(dot(R, V), 0)) ** self.__shininess
        return diffuse + specular

    @property
    def kd(self):
        return self.__diffuse


@njit
def render(camera, sphere, light, brdf, screen_width, screen_height):
    frame_buffer_color = np.zeros((screen_width, screen_height, 3), np.float32)
    frame_buffer_position = np.zeros(
        (screen_width, screen_height, 3), np.float32)
    frame_buffer_normal = np.zeros(
        (screen_width, screen_height, 3), np.float32)

    for y in range(screen_height):
        for x in range(screen_width):
            ray = camera.ray_through_pixel(
                x / screen_width, 1 - y / screen_height)
            hit = sphere.intersect(ray)
            if hit is not None:
                t, hit_pos, hit_normal = hit

                light_vec, Li = light.light_at_point(hit_pos)
                origin, direction = ray
                if dot(hit_normal, light_vec) > 0.0:
                    R = brdf.evaluate(hit_normal, light_vec, -direction)
                    L = Li * R
                else:
                    L = Vec3(0, 0, 0)

                frame_buffer_color[y, x, 0] = L[0]
                frame_buffer_color[y, x, 1] = L[1]
                frame_buffer_color[y, x, 2] = L[2]

                frame_buffer_position[y, x, 0] = hit_pos[0]
                frame_buffer_position[y, x, 1] = hit_pos[1]
                frame_buffer_position[y, x, 2] = hit_pos[2]

                frame_buffer_normal[y, x, 0] = hit_normal[0]
                frame_buffer_normal[y, x, 1] = hit_normal[1]
                frame_buffer_normal[y, x, 2] = hit_normal[2]

    return (frame_buffer_color, frame_buffer_position, frame_buffer_normal)


@njit
def render_heterogeneous_kd(camera, sphere, brdfs, material_map, width, height):
    framebuffer = np.zeros((height, width, 3), np.float32)
    mmap_height, mmap_width = material_map.shape

    def sample_material_map(u, v):
        # https://gamedev.stackexchange.com/questions/114412/how-to-get-uv-coordinates-for-sphere-cylindrical-projection
        ui = max(0, min(mmap_width-1, int(u * mmap_width + 0.5)))
        vi = max(0, min(mmap_height-1, int(v * mmap_height + 0.5)))
        return material_map[vi, ui]

    for y in range(height):
        for x in range(width):
            ray = camera.ray_through_pixel(x / width, 1 - y / height)
            hit = sphere.intersect(ray)
            if hit is not None:
                t, pos, N = hit

                u = np.arctan2(N[0], N[2]) / (2 * np.pi) + 0.5
                v = N[1] * 0.5 + 0.5

                brdf_index = sample_material_map(u, v)
                framebuffer[y, x] = brdfs[brdf_index].kd

    return framebuffer

@njit
def render_heterogeneous(camera, sphere, light, brdfs, material_map, width, height):
    frame_buffer_color = np.zeros((height, width, 3), np.float32)
    frame_buffer_position = np.zeros((height, width, 3), np.float32)
    frame_buffer_normal = np.zeros((height, width, 3), np.float32)

    mmap_height, mmap_width = material_map.shape

    def sample_material_map(u, v):
        # https://gamedev.stackexchange.com/questions/114412/how-to-get-uv-coordinates-for-sphere-cylindrical-projection
        ui = max(0, min(mmap_width-1, int(u * mmap_width + 0.5)))
        vi = max(0, min(mmap_height-1, int(v * mmap_height + 0.5)))
        return material_map[vi, ui]

    for y in range(height):
        for x in range(width):
            ray = camera.ray_through_pixel(x / width, 1 - y / height)
            hit = sphere.intersect(ray)
            if hit is not None:
                t, pos, N = hit

                u = np.arctan2(N[0], N[2]) / (2 * np.pi) + 0.5
                v = N[1] * 0.5 + 0.5

                L, Li = light.light_at_point(pos)
                origin, direction = ray
                if dot(N, L) > 0.0:
                    brdf_index = sample_material_map(u, v)
                    brdf = brdfs[brdf_index]
                    R = brdf.evaluate(N, L, -direction)
                    Lo = Li * R
                else:
                    Lo = Vec3(0, 0, 0)

                frame_buffer_color[y, x, 0] = Lo[0]
                frame_buffer_color[y, x, 1] = Lo[1]
                frame_buffer_color[y, x, 2] = Lo[2]

                frame_buffer_position[y, x, 0] = pos[0]
                frame_buffer_position[y, x, 1] = pos[1]
                frame_buffer_position[y, x, 2] = pos[2]

                frame_buffer_normal[y, x, 0] = N[0]
                frame_buffer_normal[y, x, 1] = N[1]
                frame_buffer_normal[y, x, 2] = N[2]

    return (frame_buffer_color, frame_buffer_position, frame_buffer_normal)


@njit
def render_heterogeneous_single_view(camera, sphere, light, brdfs, material_map):
    height, width = material_map.shape
    frame_buffer_color = np.zeros((height, width, 3), np.float32)
    frame_buffer_position = np.zeros((height, width, 3), np.float32)
    frame_buffer_normal = np.zeros((height, width, 3), np.float32)

    for y in range(height):
        for x in range(width):
            ray = camera.ray_through_pixel(x / width, 1 - y / height)
            hit = sphere.intersect(ray)
            if hit is not None:
                t, pos, N = hit

                L, Li = light.light_at_point(pos)
                origin, direction = ray
                if dot(N, L) > 0.0:
                    brdf_index = material_map[y, x]
                    if brdf_index >= len(brdfs):
                        frame_buffer_color[y, x] = (1,0,0)
                        continue
                    brdf = brdfs[brdf_index]
                    R = brdf.evaluate(N, L, -direction)
                    Lo = Li * R
                else:
                    Lo = Vec3(0, 0, 0)

                frame_buffer_color[y, x, 0] = Lo[0]
                frame_buffer_color[y, x, 1] = Lo[1]
                frame_buffer_color[y, x, 2] = Lo[2]

                frame_buffer_position[y, x, 0] = pos[0]
                frame_buffer_position[y, x, 1] = pos[1]
                frame_buffer_position[y, x, 2] = pos[2]

                frame_buffer_normal[y, x, 0] = N[0]
                frame_buffer_normal[y, x, 1] = N[1]
                frame_buffer_normal[y, x, 2] = N[2]

    return (frame_buffer_color, frame_buffer_position, frame_buffer_normal)


def sample_uniform_hemisphere():
    # http://www.rorydriscoll.com/2009/01/07/better-sampling/
    u1, u2 = np.random.rand(2).astype(np.float32)
    r = np.sqrt(1 - u1*u1)
    phi = 2 * math.pi * u2
    return Vec3(np.cos(phi) * r, np.sin(phi) * r, u1)


def sample_cosine_hemisphere():
    # http://www.rorydriscoll.com/2009/01/07/better-sampling/
    u1, u2 = np.random.rand(2).astype(np.float32)
    r = np.sqrt(u1)
    theta = 2 * math.pi * u2

    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return Vec3(x, y, np.sqrt(max(1 - u1, 0)))


def sample_uniform_sphere():
    # http://corysimon.github.io/articles/uniformdistn-on-sphere/
    u1, u2 = np.random.rand(2).astype(np.float32)
    theta = 2 * math.pi * u1
    phi = np.arccos(1 - 2 * u2)
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    return Vec3(x, y, z)
