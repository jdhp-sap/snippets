#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Display the pixel layout of the givent telescope as defined in a given simtel file.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source

import numpy as np
from matplotlib import pyplot as plt


def plot_pixels_layout(simtel_file_path, tel_id):

    source = hessio_event_source(simtel_file_path, allowed_tels=[tel_id])

    for event in source:
        #######################################################################
        # CAUTION:                                                            #
        # event.meta.optical_foclen and event.meta.tel_pos are only filled    #
        # when source is traversed !                                          #
        # The current value of these two variables is not the actual value    #
        # for the current event but the cumulated value of past events !      #
        #######################################################################
        print("Event", event.dl0.event_id)

    (pos_x_list, pos_y_list) = event.meta.pixel_pos[tel_id]
    pos_x_list = [float(pos.value) for pos in pos_x_list]
    pos_y_list = [float(pos.value) for pos in pos_y_list]

    assert len(pos_x_list) == len(pos_y_list)

    # PLOT ####################################################################

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    
    # Scatter method ##################

    ax.scatter(pos_x_list,    # x
               pos_y_list,    # y
               s=0.2,  # radius
               c="black",  # color
               alpha=0.75)

    ax.plot(pos_x_list,    # x
            pos_y_list,    # y
            "k-",
            alpha=0.25)

    for pixel_index in range(len(pos_x_list)):
        ax.text(pos_x_list[pixel_index], pos_y_list[pixel_index], str(pixel_index), fontsize=9)

    ax.set_title("Pixels position (telescope {})".format(tel_id), fontsize=16)

    ax.set_xlabel("x position (m)", fontsize=16)
    ax.set_ylabel("y position (m)", fontsize=16)

    plt.show()


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display the pixel layout for the given telescope as defined in a given simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, required=True,
                        metavar="INTEGER",
                        help="The telescope to query (telescope number)")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_id = args.telescope
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    plot_pixels_layout(simtel_file_path, tel_id)

