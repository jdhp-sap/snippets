#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Display simulated camera images from a JSON file.
"""

import argparse
import astropy

import ctapipe
import ctapipe.io
import ctapipe.visualization

import json

from matplotlib import pyplot as plt
import numpy as np

import os


def plot_json_image(json_file_path, output_file_path, json_geometry_file_path, quiet=False, plot_title=None):

    # GET THE TELESCOPE'S GEOMETRY ##########################################
    # TODO...

    #geom = ctapipe.io.CameraGeometry.from_name("LST", 1)  # This doesn't work (bug in ctapipe ?)

    with open(json_geometry_file_path, "r") as fd:
        camera_geometry_dict = json.load(fd)

    x = astropy.units.quantity.Quantity(camera_geometry_dict['pixel_pos_x']) * astropy.units.m
    y = astropy.units.quantity.Quantity(camera_geometry_dict['pixel_pos_y']) * astropy.units.m
    foclen = camera_geometry_dict['foclen'] * astropy.units.m

    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

    # GET IMAGE #############################################################

    with open(json_file_path, "r") as fd:
        image_list = json.load(fd)

    image_array = np.array(image_list)

    # INIT PLOT #############################################################

    disp = ctapipe.visualization.CameraDisplay(geom)
    disp.enable_pixel_picker()
    disp.add_colorbar()

    if plot_title is None:
        disp.axes.set_title(os.path.basename(json_file_path))
    else:
        disp.axes.set_title(plot_title)

    # DISPLAY INTEGRATED EVENT ##############################################

    disp.image = image_array

    #disp.set_limits_minmax(0, 9000)
    disp.set_limits_percent(70)        # TODO

    # PLOT ##################################################################

    plt.savefig(output_file_path)

    if not quiet:
        plt.show()


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a JSON file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--title", "-t", default=None,
                        metavar="STRING",
                        help="The plot's title")

    parser.add_argument("--geometry", "-g", default=None, required=True,
                        metavar="FILE",
                        help="A JSON file defining the geometry of the camera")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    quiet = args.quiet
    plot_title = args.title
    json_geometry_file_path = args.geometry
    json_file_path = args.fileargs[0]

    if args.output is None:
        output_file_path = "json_image.pdf"
    else:
        output_file_path = args.output

    # DISPLAY IMAGE ###########################################################

    plot_json_image(json_file_path, output_file_path, json_geometry_file_path, quiet, plot_title)

