#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Display the telarray layout defined in a given simtel file.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source

import numpy as np
from matplotlib import pyplot as plt


def plot_telarray_layout(simtel_file_path, show_labels=False):

    # GET EVENT ###############################################################

    source = hessio_event_source(simtel_file_path)

    for event in source:
        #######################################################################
        # WARNING:                                                            #
        # event.meta.optical_foclen and event.meta.tel_pos are only filled    #
        # when source is traversed !                                          #
        # The current value of these two variables is not the actual value    #
        # for the current event but the cumulated value of past events !      #
        #######################################################################

        print("Event", event.dl0.event_id)
        #print("tels_with_trigger", event.trig.tels_with_trigger)
        #print("tels_with_data", event.dl0.tels_with_data)
        #print("optical_foclen", event.meta.optical_foclen)
        #print("tel_pos", event.meta.tel_pos)

    # Print values

    print()
    print("optical_foclen:")
    for telid, foclen in event.meta.optical_foclen.items():
        print(" - TEL {:03d}: {}".format(telid, foclen))

    print()
    print("tel_pos:")
    for telid, position in event.meta.tel_pos.items():
        print(" - TEL {:03d}: {}".format(telid, position))

    # Make a numpy array of telescopes position

    tel_list = []
    for tel_id, tel_pos in event.meta.tel_pos.items():
        tel_id = int(tel_id)
        tel_pos = [float(v.value) for v in tel_pos]
        tel_foclen = float(event.meta.optical_foclen[tel_id].value)
        tel_list.append([tel_id, *tel_pos, tel_foclen])

    tel_array = np.array(tel_list)
    #print(len(tel_array))

    # PLOT ####################################################################

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    
    # Patches method ##################

    #for tel_id, pos_x, pos_y, pos_z, tel_foclen in tel_list:
    #    ax.add_patch(plt.Circle((pos_x, pos_y), radius=tel_foclen, color='red'))

    #max_foclen = float(np.max(tel_array[:,4]))
    #margin = 2. * max_foclen

    #ax.set_xlim([np.min(tel_array[:,1]) - margin, np.max(tel_array[:,1]) + margin])
    #ax.set_ylim([np.min(tel_array[:,2]) - margin, np.max(tel_array[:,2]) + margin])

    # Scatter method ##################

    ax.scatter(tel_array[:,1],    # x
               tel_array[:,2],    # y
               s=tel_array[:,4],  # radius
               c=tel_array[:,4],  # color
               alpha=0.75)

    ## Highlight some telescopes
    #ax.scatter(tel_array[:,1],    # x
    #           tel_array[:,2],    # y
    #           s=tel_array[:,4],  # radius
    #           c="gray",  # color
    #           alpha=0.25)

    #for n in range(102-1, 125):
    #    ax.scatter(tel_array[n,1],    # x
    #               tel_array[n,2],    # y
    #               s=32,  # radius
    #               c="red")  # color

    if show_labels:
        for tel_id, pos_x, pos_y, pos_z, tel_foclen in tel_list:
            ax.text(pos_x + tel_foclen/2., pos_y, str(tel_id), fontsize=9)

    #ax.set_title("Telescopes position for " + simtel_file_path)
    ax.set_title("Telescopes position", fontsize=16)

    ax.set_xlabel("x position (m)", fontsize=16)
    ax.set_ylabel("y position (m)", fontsize=16)

    plt.show()


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display the telarray layout defined in a given simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--labels", "-l", action="store_true",
                        help="Show telescopes name")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    show_labels = args.labels
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    plot_telarray_layout(simtel_file_path, show_labels)

