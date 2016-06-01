#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot the mean of input images (stored in JSON files).
"""

import argparse
import astropy

import ctapipe
import ctapipe.io
import ctapipe.visualization

import json

import matplotlib.pyplot as plt
import numpy as np

def fetch_images(json_file_path_list):

    image_dict_list = []

    # For each json file...
    for json_file_path in json_file_path_list:
        print(json_file_path)
        with open(json_file_path, "r") as fd:
            image_dict = json.load(fd)
            image_dict_list.append(image_dict)

    return image_dict_list


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Plot the mean of input images (stored in JSON files).")

    parser.add_argument("--photoelectron", "-p", action="store_true",
                        help="Plot the photoelectron image")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON files to process")

    args = parser.parse_args()

    process_photoelectron = args.photoelectron
    output_file_path = args.output
    quiet = args.quiet

    json_file_path_list = args.fileargs

    # FETCH IMAGES ############################################################

    image_dict_list = fetch_images(json_file_path_list)

    image_list = []
    for image_dict in image_dict_list:
        if process_photoelectron:
            image_list.append(image_dict["photoelectron_image"])
        else:
            image_list.append(image_dict["image"])

    image_array = np.array(image_list)

    # MAKE STATISTICS #########################################################

    image_mean = np.mean(image_array, axis=0)

    # GET THE TELESCOPE'S GEOMETRY ##########################################

    image_dict = image_dict_list[0]
    x = astropy.units.quantity.Quantity(image_dict['pixel_pos_x']) * astropy.units.m
    y = astropy.units.quantity.Quantity(image_dict['pixel_pos_y']) * astropy.units.m
    foclen = image_dict['foclen'] * astropy.units.m

    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

    # INIT PLOT #############################################################

    disp = ctapipe.visualization.CameraDisplay(geom)
    disp.enable_pixel_picker()
    disp.add_colorbar()

    title = "EV{:03d} TEL{:03d} ({})".format(image_dict["event_id"], image_dict["tel_id"], image_dict["camera_id"])
    disp.axes.set_title(title)

    # DISPLAY INTEGRATED EVENT ##############################################

    disp.image = image_mean

    #disp.set_limits_minmax(0, 9000)
    disp.set_limits_percent(70)        # TODO

    # PLOT ##################################################################

    if output_file_path is None:
        output_file_path = "EV{:03d}_TEL{:03d}{}_MEAN.pdf".format(
                image_dict["event_id"],
                image_dict["tel_id"],
                "_PE" if process_photoelectron else ""
                )

    plt.savefig(output_file_path)

    if not quiet:
        plt.show()

