#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make and show simulated camera images using the "mock" simulator with a
rectangular camera (random simulation).

Inspired by ctapipe/examples/camera_animation.py

Cf. also: https://cta-observatory.github.io/ctapipe/reco/index.html
"""

from astropy import units as u

import numpy as np
import matplotlib.pylab as plt

from ctapipe import io, visualization
from ctapipe.reco import mock

# INIT MATPLOTLIB #############################################################

plt.style.use("ggplot")
fig, ax = plt.subplots()

# LOAD THE CAMERA #############################################################

geom = io.make_rectangular_camera_geometry()    # rectangular geometry

disp = visualization.CameraDisplay(geom, ax=ax)
disp.cmap = plt.cm.terrain
disp.add_colorbar(ax=ax)

# GENERATE A (RANDOM) 2D SHOWER MODEL #########################################

centroid = np.random.uniform(-0.5, 0.5, size=2)
width = np.random.uniform(0, 0.01)
length = np.random.uniform(0, 0.03) + width
angle = np.random.uniform(0, 360)
intens = np.random.exponential(2) * 50

model = mock.generate_2d_shower_model(centroid=centroid,
                                      width=width,
                                      length=length,
                                      psi=angle * u.deg)

# MAKE THE IMAGE ##############################################################

# image = c * (sig + bg)
# - "image" is the noisy image (a 1D Numpy array with one value per pixel).
# - "sig" is the clean image (a 1D Numpy array with one value per pixel).
# - "bg" is the background noise (a 1D Numpy array with one value per pixel).
image, sig, bg = mock.make_mock_shower_image(geom,
                                             model.pdf,
                                             intensity=intens,
                                             nsb_level_pe=5000)

# NORMALIZE PIXELS VALUE ######################################################

image -= image.min()
image /= image.max()

# PLOT ########################################################################

disp.image = image   # Show the noised signal
#disp.image = sig    # Show the clean (unnoised) signal
#disp.image = bg     # Show the background noise

plt.show()

