#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract simulated camera images from a simtel file.

Inspired by ctapipe/examples/read_hessio_single_tel.py
"""

import argparse

import ctapipe
import ctapipe.visualization
from ctapipe.io.hessio import hessio_event_source

from matplotlib import pyplot as plt


def show_image(simtel_file_path, output_file_path, tel_num, event_id, channel=0, quiet=False):

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path, allowed_tels=[tel_num])

    event = None

    for ev in source:
        if int(ev.dl0.event_id) == event_id:
            event = ev
            break

    if event is None:
        raise Exception("Error: event '{}' not found for telescope '{}'.".format(event_id, tel_num))

    # INIT PLOT #############################################################

    x, y = event.meta.pixel_pos[tel_num]
    foclen = event.meta.optical_foclen[tel_num]
    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

    disp = ctapipe.visualization.CameraDisplay(geom, title='CT%d' % tel_num)
    disp.enable_pixel_picker()
    disp.add_colorbar()

    disp.axes.set_title('Telescope {:03d}, Event {:05d}'.format(tel_num, event_id))

    # DISPLAY TIME-VARYING EVENT ############################################

    #data = event.dl0.tel[tel_num].adc_samples[channel]
    #for ii in range(data.shape[1]):
    #    disp.image = data[:, ii]
    #    disp.set_limits_percent(70)   # TODO
    #    plt.savefig('CT{:03d}_EV{:05d}_S{:02d}.png'.format(tel_num, event_id, ii), bbox_inches='tight')

    # DISPLAY INTEGRATED EVENT ##############################################

    # The image "event.dl0.tel[tel_num].adc_sums[channel]" is a 1D numpy array (dtype=int32)
    disp.image = event.dl0.tel[tel_num].adc_sums[channel]

    #disp.set_limits_minmax(0, 9000)
    disp.set_limits_percent(70)        # TODO

    # PLOT ##################################################################

    plt.savefig(output_file_path, bbox_inches='tight')

    if not quiet:
        plt.show()


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, required=True,
                        metavar="INTEGER",
                        help="The telescope to query (telescope number)")

    parser.add_argument("--channel", "-c", type=int, default=0,
                        metavar="INTEGER",
                        help="The channel number to query")

    parser.add_argument("--event", "-e", type=int, required=True,
                        metavar="INTEGER",
                        help="The event to extract (event ID)")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    channel = args.channel
    event_id = args.event
    quiet = args.quiet
    simtel_file_path = args.fileargs[0]

    if args.output is None:
        output_file_path = "TEL{:03d}_EV{:05d}_CH{:03d}.pdf".format(tel_num, event_id, channel)
    else:
        output_file_path = args.output

    # DISPLAY IMAGES ##########################################################

    show_image(simtel_file_path, output_file_path, tel_num, event_id, channel, quiet)

