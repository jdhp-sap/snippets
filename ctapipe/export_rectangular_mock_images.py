#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make simulated Camera images using the "mock" simulator (random simulation).

Taken from ctapipe/examples/camera_animation.py

Cf. also: https://cta-observatory.github.io/ctapipe/reco/index.html
"""

import argparse

from ctapipe import io, visualization
from ctapipe.reco import mock

from astropy import units as u

import math
import numpy as np

import PIL.Image as pil_img # PIL.Image is a module not a class...


def make_an_image(image_name):

    # LOAD THE CAMERA #########################################

    geom = io.make_rectangular_camera_geometry()

    # MAKE THE IMAGE ##########################################

    centroid = np.random.uniform(-0.5, 0.5, size=2)
    width = np.random.uniform(0, 0.01)
    length = np.random.uniform(0, 0.03) + width
    angle = np.random.uniform(0, 360)
    intens = np.random.exponential(2) * 50

    model = mock.generate_2d_shower_model(centroid=centroid,
                                          width=width,
                                          length=length,
                                          psi=angle * u.deg)

    image, sig, bg = mock.make_mock_shower_image(geom,
                                                 model.pdf,
                                                 intensity=intens,
                                                 nsb_level_pe=5000)

    # NORMALIZE PIXELS VALUE ##################################

    image -= image.min()
    image /= image.max()
    
    image = np.array([pixel * 255 for pixel in image])

    # SAVE THE IMAGE ##########################################

    mode = "L"       # Grayscale
    size = int(math.sqrt(image.size))

    pil_image = pil_img.new(mode, (size, size))
    pil_image.putdata(image)

    pil_image.save(image_name)


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='Make simulated Camera images using the "mock" simulator (random simulation).')

    parser.add_argument("--number", "-n", type=int, default=1, metavar="INTEGER", 
                        help="The number of images to make")
    args = parser.parse_args()

    number_of_images = args.number

    # MAKE IMAGES #############################################################

    for i in range(number_of_images):
        make_an_image("ctapipe_{}.png".format(i))

