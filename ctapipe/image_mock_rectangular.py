#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example of drawing a Camera using a mock shower images (random simulation).

Taken from ctapipe/examples/camera_animation.py

Cf. also: https://cta-observatory.github.io/ctapipe/reco/index.html
"""

import matplotlib.pylab as plt
from ctapipe import io, visualization
from ctapipe.reco import mock

import numpy as np
from matplotlib.animation import FuncAnimation

from astropy import units as u

# Init matplotlib
plt.style.use("ggplot")
fig, ax = plt.subplots()

# Load the camera
#geom = io.CameraGeometry.from_name("hess", 1)
geom = io.make_rectangular_camera_geometry()

disp = visualization.CameraDisplay(geom, ax=ax)
disp.cmap = plt.cm.terrain
disp.add_colorbar(ax=ax)

# Plot
centroid = np.random.uniform(-0.5, 0.5, size=2)
width = np.random.uniform(0, 0.01)
length = np.random.uniform(0, 0.03) + width
angle = np.random.uniform(0, 360)
intens = np.random.exponential(2) * 50

model = mock.generate_2d_shower_model(centroid=centroid,
                                      width=width,
                                      length=length,
                                      psi=angle * u.deg)

# The generated image "image" is a 1D Numpy array.
# image est probablement l'image bruitée: sig + bg
# 
#  image.ndim = 1
#  image.shape = (960,)
#
# sig is an numpy array (what it is used for ?)
# sig est probablement l'image non bruitée
#
#  sig.ndim = 1
#  sig.shape = (960,)
#
# bg is an numpy array (what it is used for ?)
# bg est probablement le bruit
#
#  bg.ndim = 1
#  bg.shape = (960,)
#
image, sig, bg = mock.make_mock_shower_image(geom,
                                             model.pdf,
                                             intensity=intens,
                                             nsb_level_pe=5000)

# Normalize pixels value
image /= image.max()

disp.image = image
plt.show()

print(image)
print(type(image))
print(image.shape)
print(image.ndim)
print(image[0])
print(image.min())
print(image.max())

#print(sig)
#print(type(sig))
#print(sig.shape)
#print(sig.ndim)
#print(sig[0])

#print(bg)
#print(type(bg))
#print(bg.shape)
#print(bg.ndim)
#print(bg[0])

