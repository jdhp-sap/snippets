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


def plot_json_image(json_file_path, output_file_path=None, plot_photoelectron=False, quiet=False, plot_title=None):

    with open(json_file_path, "r") as fd:
        image_dict = json.load(fd)

    # GET THE TELESCOPE'S GEOMETRY ##########################################

    x = astropy.units.quantity.Quantity(image_dict['pixel_pos_x']) * astropy.units.m
    y = astropy.units.quantity.Quantity(image_dict['pixel_pos_y']) * astropy.units.m
    foclen = image_dict['foclen'] * astropy.units.m

    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

    # GET IMAGE #############################################################

    if plot_photoelectron:
        image_array = np.array(image_dict["photoelectron_image"])
    else:
        image_array = np.array(image_dict["image"])

    # INIT PLOT #############################################################

    disp = ctapipe.visualization.CameraDisplay(geom)
    disp.enable_pixel_picker()
    disp.add_colorbar()

    if plot_title is None:
        title = "EV{:03d} TEL{:03d} ({})".format(image_dict["event_id"], image_dict["tel_id"], image_dict["camera_id"])
        disp.axes.set_title(title)
    else:
        disp.axes.set_title(plot_title)

    # DISPLAY INTEGRATED EVENT ##############################################

    disp.image = image_array

    #disp.set_limits_minmax(0, 9000)
    disp.set_limits_percent(70)        # TODO

    # PLOT ##################################################################

    if output_file_path is None:
        output_file_path = "EV{:03d}_TEL{:03d}{}.pdf".format(
                image_dict["event_id"],
                image_dict["tel_id"],
                "_PE" if plot_photoelectron else ""
                )

    plt.savefig(output_file_path)

    if not quiet:
        plt.show()


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a JSON file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--photoelectron", "-p", action="store_true",
                        help="Plot the photoelectron image")

    parser.add_argument("--title", "-t", default=None,
                        metavar="STRING",
                        help="The plot's title")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    quiet = args.quiet
    plot_photoelectron = args.photoelectron
    plot_title = args.title
    output_file_path = args.output

    json_file_path = args.fileargs[0]

    # DISPLAY IMAGE ###########################################################

    plot_json_image(json_file_path, output_file_path, plot_photoelectron, quiet, plot_title)

