from helpers import *
import numpy as np
from numba import njit
import random
import matplotlib.pyplot as plt
import sys
import re
from collections import namedtuple
sys.path.append("../../")


def read_vector(f):
    return [float(v) for v in f.readline().strip().split(" ")]


def read_int_vector(f):
    return [int(v) for v in f.readline().strip().split(" ")]


def read_matrix3x3(f):
    m = []
    for i in range(3):
        m += read_vector(f)
    assert(len(m) == 9)
    return np.array(m, dtype=np.float32).reshape(3, 3)


Camera = namedtuple(
    "Camera", ["pos", "intr", "extr", "intr_extr", "inv_intr", "inv_rot"])


def load_camera_epfl(camera_data_file):
    with open(camera_data_file, "r") as f:
        intr = read_matrix3x3(f)
        inv_intr = np.ascontiguousarray(np.linalg.inv(intr))

        f.readline()  # Skip over radial distortion parameters

        inv_rotation = read_matrix3x3(f)
        rotation = np.ascontiguousarray(inv_rotation.T)

        pos = np.array(read_vector(f), np.float32)
        translation_vector = -np.dot(rotation, pos)

        extr = rotation.tolist()
        for i, t in enumerate(translation_vector):
            extr[i].append(t)
        extr = np.array(extr, np.float32)

    intr_extr = intr @ extr
    return Camera(pos, intr, extr, intr_extr, inv_intr, inv_rotation)


def load_points3D_epfl(points_data_file):
    with open(points_data_file, "r") as f:
        # Skip first line (contains dimension (=3) and num points)
        num_dims, num_points = read_int_vector(f)
        assert(num_dims == 3)
        points = [read_vector(f) for i in range(num_points)]
        return np.array(points, np.float32)


def load_camera(camera_file, source_type, *args, **kwargs):
    f = None
    if source_type == "epfl":
        f = load_camera_epfl
    elif source_type == "embree":
        f = load_camera_embree
    else:
        assert(False)

    return f(camera_file, *args, **kwargs)


def load_points3D(points_file, source_type, *args, **kwargs):
    f = None
    if source_type == "epfl":
        f = load_points3D_epfl
    elif source_type == "embree":
        f = load_points3D_embree
    else:
        assert(False)

    return f(points_file, *args, **kwargs)


def scale_camera(camera, scale):
    intr = camera.intr.copy()
    intr = intr * scale
    intr[2, 2] /= scale  # Undo scale of w component

    inv_intr = np.linalg.inv(intr)
    intr_extr = intr @ camera.extr
    return camera._replace(intr=intr, intr_extr=intr_extr, inv_intr=inv_intr)


def flip_camera_axis(camera):
    intr_in = camera.intr
    intr = intr_in.copy()
    intr[0, :] = intr_in[1, :]
    intr[1, :] = intr_in[0, :]
    intr[1, 0] *= -1

    inv_intr = np.linalg.inv(intr)
    intr_extr = intr @ camera.extr
    return camera._replace(intr=intr, intr_extr=intr_extr, inv_intr=inv_intr)


def flip_image_axis(image):
    return image.T[::-1, :]


def flip_color_image_axis(image):
    return np.swapaxes(image, 0, 1)[::-1, :, :]


@njit
def project_point(camera, point3D):
    M = camera.intr_extr

    point2D = np.dot(M, np.array(
        [point3D[0], point3D[1], point3D[2], 1], np.float32))
    return point2D[:2] / point2D[2]


@njit
def project_points(camera, points3D):
    M = camera.intr_extr

    num_points, _ = points3D.shape
    points2D = np.empty((num_points, 2), np.float32)
    for i in range(num_points):
        # Manual dot product is much more performant than messing around with numpy
        x, y, z = points3D[i, :]
        ox = M[0, 0] * x + M[0, 1] * y + M[0, 2] * z + M[0, 3]
        oy = M[1, 0] * x + M[1, 1] * y + M[1, 2] * z + M[1, 3]
        oz = M[2, 0] * x + M[2, 1] * y + M[2, 2] * z + M[2, 3]
        points2D[i, 0] = ox / oz
        points2D[i, 1] = oy / oz
    return points2D


@njit
def bresenham(p0, p1):  # p0 = input camera, p1 =
    x0, y0 = np.int32(p0)
    x1, y1 = np.int32(p1)

    pixels = []
    if x0 == x1 and y0 == y1:
        return pixels  # Returning [] does not compile because Numba can't infer type

    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) > abs(dy):
        derr = abs(dy / dx)
        error = 0.0
        y = y0
        for x in range(x0, x1, np.sign(dx)):
            pixels.append((x, y))
            error += derr
            if error >= 0.5:
                y += np.sign(dy)
                error -= 1
    else:
        derr = abs(dx / dy)
        error = 0.0
        x = x0
        for y in range(y0, y1, np.sign(dy)):
            pixels.append((x, y))
            error += derr
            if error >= 0.5:
                x += np.sign(dx)
                error -= 1
    return pixels


@njit
def snap_line_to_screen(p0, p1, resolution):
    height, width = resolution
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    tx0 = -p0[0] / dx  # x = p0 + t * dx = 0 => t = -p / dx
    tx1 = (width-1-p0[0]) / dx  # x = p0 + t * dx = width - 1 => t = (width-1-p0) / dx
    txmin = min(tx0, tx1)
    txmax = max(tx0, tx1)
    ty0 = -p0[1] / dy
    ty1 = (height-1-p0[1]) / dy
    tymin = min(ty0, ty1)
    tymax = max(ty0, ty1)
    tmin = max(txmin, tymin)
    tmax = min(txmax, tymax)

    x0 = p0[0] + tmin * dx
    y0 = p0[1] + tmin * dy
    x1 = p0[0] + tmax * dx
    y1 = p0[1] + tmax * dy
    return ((int(x0+0.5), int(y0+0.5)), (int(x1+0.5), int(y1+0.5)))

def draw_line_through_pixels(image, p0, p1, color):
    height, width, _ = image.shape

    result = image.copy()
    edge_p0, edge_p1 = snap_line_to_screen(p0, p1, (height, width)) # Pixels through line at edge of screen
    for x, y in bresenham(edge_p0, edge_p1):
        result[y, x, :] = color
    return result

@njit
def project_ray_to_visible_line_segment(camera, ray, resolution):
    origin, direction = ray
    p0 = project_point(camera, origin)
    p1 = project_point(camera, origin + direction)

    return snap_line_to_screen(p0, p1, resolution)

# Asume that pixel0 and pixel1 are inside the image but the support domain might not be. Image0 and image1 are assumed
# to be of the same size.
@njit
def get_support_domains(image0, image1, pixel0, pixel1, s):
    x0, y0 = pixel0
    x1, y1 = pixel1
    h, w = image0.shape

    sx_min = min(s, x0, x1)
    sy_min = min(s, y0, y1)
    sx_max = min(s, w-1-x0, w-1-x1)
    sy_max = min(s, h-1-y0, h-1-y1)

    support0 = image0[y0-sy_min:y0+sy_max+1, x0-sx_min:x0+sx_max+1]
    support1 = image1[y1-sy_min:y1+sy_max+1, x1-sx_min:x1+sx_max+1]
    return (support0, support1)


@njit
def get_support_domains_no_bounds_check(image0, image1, pixel0, pixel1, s):
    x0, y0 = pixel0
    x1, y1 = pixel1
    support0 = image0[y0-s:y0+s+1, x0-s:x0+s+1]
    support1 = image1[y1-s:y1+s+1, x1-s:x1+s+1]
    return (support0, support1)


@njit
def pixel_to_ray(camera, pixel):
    def screen_to_camera(p):
        x, y, z = p
        tmp = np.dot(camera.inv_intr, np.array([x, y, 1], np.float32)*z)
        return tmp.flatten()

    def camera_to_world(p):
        return np.dot(camera.inv_rot, p) + camera.pos

    x, y = pixel
    p_camera = screen_to_camera((x, y, 1))  # Screen to camera
    p_world = camera_to_world(p_camera)

    direction = p_world - camera.pos
    direction /= np.linalg.norm(direction)
    return (camera.pos, direction)


@njit
def pixels_to_world(camera, pixel, depths):
    points3D = np.empty((len(depths), 3))

    origin, direction = pixel_to_ray(camera, pixel)
    for j in range(3):
        for i, depth in enumerate(depths):
            points3D[i, j] = origin[j] + depth * direction[j]

    return points3D


# @njit
def compute_photo_consistency_along_ray(image0, image1, camera0, camera1, pixel0, photo_consistency_function, support_domain):
    # Estimate the depth of the ray through image0 at the given pixel by comparing the photoconsistency
    # along the viewing ray to image1
    height, width = image0.shape

    # Project 3D ray (from camera0) onto image1
    ray = pixel_to_ray(camera0, pixel0)  # 3D ray
    p0, p1 = project_ray_to_visible_line_segment(camera1, ray, image1.shape)

    pixels = []
    photo_consistencies = []
    for pixel1 in bresenham(p0, p1):
        x, y = pixel1
        if x < support_domain or x >= width - support_domain or y < support_domain or y >= height - support_domain:
            continue

        support0, support1 = get_support_domains_no_bounds_check(
            image0, image1, pixel0, pixel1, support_domain)
        photo_consistency = photo_consistency_function(support0, support1)

        pixels.append(pixel1)
        photo_consistencies.append(photo_consistency)

    if len(pixels) > 0:
        return (np.array(pixels, np.int32), np.array(photo_consistencies, np.float32))
    else:
        return (np.empty((0, 3), np.int32), np.empty((0), np.float32))


@njit
def compute_photo_consistency_along_ray_color_avg(image0, image1, camera0, camera1, pixel0, photo_consistency_function, support_domain):
    # Estimate the depth of the ray through image0 at the given pixel by comparing the photoconsistency
    # along the viewing ray to image1
    height, width, num_channels = image0.shape
    assert(image0.shape == image1.shape)

    assert(pixel0[0] >= support_domain and pixel0[0] < width-support_domain)
    assert(pixel0[1] >= support_domain and pixel0[1] < height-support_domain)

    # Project 3D ray (from camera0) onto image1
    ray = pixel_to_ray(camera0, pixel0)  # 3D ray
    p0, p1 = project_ray_to_visible_line_segment(camera1, ray, (height, width))

    pixels = []
    photo_consistencies = []
    for pixel1 in bresenham(p0, p1):
        x, y = pixel1
        if x < support_domain or x >= width - support_domain or y < support_domain or y >= height - support_domain:
            continue

        photo_consistency = 0.0
        for c in range(num_channels):
            support0, support1 = get_support_domains_no_bounds_check(
                image0[:, :, c], image1[:, :, c], pixel0, pixel1, support_domain)
            photo_consistency += photo_consistency_function(support0, support1)

        pixels.append(pixel1)
        photo_consistencies.append(photo_consistency / num_channels)

    if len(pixels) > 0:
        return (np.array(pixels, np.int32), np.array(photo_consistencies, np.float32))
    else:
        return (np.empty((0, 3), np.int32), np.empty((0), np.float32))


@njit
def compute_photo_consistency_along_ray_color_SSD(image0, image1, camera0, camera1, pixel0, photo_consistency_function, support_domain):
    # Estimate the depth of the ray through image0 at the given pixel by comparing the photoconsistency
    # along the viewing ray to image1
    height, width, num_channels = image0.shape

    # Project 3D ray (from camera0) onto image1
    ray = pixel_to_ray(camera0, pixel0)  # 3D ray
    p0, p1 = project_ray_to_visible_line_segment(camera1, ray, (height, width))

    pixels = []
    photo_consistencies = []
    for pixel1 in bresenham(p0, p1):
        x, y = pixel1
        if x < support_domain or x >= width - support_domain or y < support_domain or y >= height - support_domain:
            continue

        photo_consistency = 0.0
        for c in range(num_channels):
            support0, support1 = get_support_domains_no_bounds_check(
                image0[:, :, c], image1[:, :, c], pixel0, pixel1, support_domain)
            photo_consistency += photo_consistency_function(
                support0, support1) ** 2

        pixels.append(pixel1)
        photo_consistencies.append(photo_consistency / num_channels)

    if len(pixels) > 0:
        return (np.array(pixels, np.int32), np.array(photo_consistencies, np.float32))
    else:
        return (np.empty((0, 3), np.int32), np.empty((0), np.float32))


def plot_photoconsistency_along_ray(
        image0, image1, camera0, camera1, point3D, pc_func, support_domain):
    # Project points to 2D
    pixel0 = project_point(camera0, point3D).astype(np.int)
    pixel1 = project_point(camera1, point3D).astype(np.int)

    # Shoot a ray from camera0 through the pixel. Walk along it in image space (of image1) and compute photo consistency.
    pixels, photo_consistency = compute_photo_consistency_along_ray(
        image0, image1, camera0, camera1, pixel0, pc_func, support_domain)

    if len(pixels) == 0:
        print("Epipolar line not in image")
        return

    # Compute where along the ray the point should actually be
    pixel1_pos_along_ray = np.argmin(
        np.array([SSD(pixel, pixel1) for pixel in pixels]))

    print(f"Pixel with max photo consistency: {np.argmax(photo_consistency)}")
    print(f"Correct answer: {pixel1_pos_along_ray}")

    fig, ax = plt.subplots(figsize=default_fig_size)
    ax.set_title("Photo consistency measure along ray")
    ax.set_xlabel("Pixel along ray")
    # Draw vertical line where the point actually lies
    ax.axvline(pixel1_pos_along_ray, c="red")
    ax.plot(photo_consistency)
    # ax.plot(photo_consistency)
    fig.tight_layout()
    plt.show()

    best_pixel_index = np.argmax(photo_consistency)
    support0, support1 = get_support_domains(
        image0, image1, pixel0, pixels[best_pixel_index], 4)
    print(f"Photo consistency at pixel {best_pixel_index} (support domain shown below): ", pc_func(
        support0, support1))
    show_images({"Support domain image 0": support0,
                 "Support domain image 1": support1}, nrows=1, ncols=2)
