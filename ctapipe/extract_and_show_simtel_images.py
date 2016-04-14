#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract simulated camera images from a simtel file.

Inspired by ctapipe/examples/read_hessio_single_tel.py
"""

import argparse

import ctapipe
import ctapipe.visualization
#from ctapipe.utils.datasets import get_example_simtelarray_file
from ctapipe.io.hessio import hessio_event_source

from matplotlib import pyplot as plt


def show_image(simtel_file_path, tel_num=1, channel=0, event_index=0):

    max_events = 5

    # GET EVENT #############################################################

    # Source is a python generator.
    # It contains ctapipe.core.Container instances ("event").
    #
    # Source contains few events (usually 0, 1 or 2)
    source = hessio_event_source(simtel_file_path, allowed_tels=[tel_num], max_events=max_events)

    event_list = list(source)
    event = event_list[event_index]

    # INIT PLOT #############################################################

    x, y = event.meta.pixel_pos[tel_num]
    geom = ctapipe.io.CameraGeometry.guess(x, y)
    disp = ctapipe.visualization.CameraDisplay(geom, title='CT%d' % tel_num)
    disp.enable_pixel_picker()
    #disp.add_colorbar()

    disp.axes.set_title('CT{:03d}, event {:010d}'.format(tel_num, event.dl0.event_id))

    # DISPLAY TIME-VARYING EVENT ############################################

    #data = event.dl0.tel[tel_num].adc_samples[channel]
    #for ii in range(data.shape[1]):
    #    disp.image = data[:, ii]
    #    disp.set_limits_percent(70)
    #    plt.savefig('CT{:03d}_EV{:010d}_S{:02d}.png'.format(tel_num, event.dl0.event_id, ii))

    # DISPLAY INTEGRATED EVENT ##############################################

    disp.image = event.dl0.tel[tel_num].adc_sums[channel]
    disp.set_limits_percent(70)
    plt.savefig('CT{:03d}_EV{:010d}.png'.format(tel_num, event.dl0.event_id))

    # PLOT ##################################################################

    plt.show()


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, default=1,
                        metavar="INTEGER",
                        help="The telescope number to query")

    parser.add_argument("--channel", "-c", type=int, default=0,
                        metavar="INTEGER",
                        help="The channel number to query")

    parser.add_argument("--event", "-e", type=int, default=0,
                        metavar="INTEGER",
                        help="The event to extract")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    channel = args.channel
    event_index = args.event
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    show_image(simtel_file_path, tel_num, channel, event_index)

