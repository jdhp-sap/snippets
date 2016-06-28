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
import pyhessio

from matplotlib import pyplot as plt

def get_mc_calibration_coeffs(tel_id):
    """
    Get the calibration coefficients from the MC data file to the
    data. This is ahack (until we have a real data structure for the
    calibrated data), it should move into `ctapipe.io.hessio_event_source`.

    RETURNS
    -------
    (pedestal, gains) : arrays of the pedestal and pe/dc ratios.
    """
    pedestal = pyhessio.get_pedestal(tel_id)[0]
    gains = pyhessio.get_calibration(tel_id)[0]

    return pedestal, gains


def show_gains_image(simtel_file_path, output_file_path, tel_num, quiet=False):

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path, allowed_tels=[tel_num])

    # TODO
    for ev in source:
        event = ev

    # INIT PLOT #############################################################

    x, y = event.meta.pixel_pos[tel_num]
    foclen = event.meta.optical_foclen[tel_num]
    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

    disp = ctapipe.visualization.CameraDisplay(geom, title='CT%d' % tel_num)
    disp.enable_pixel_picker()
    disp.add_colorbar()

    disp.axes.set_title('Telescope {:03d}'.format(tel_num))

    # DISPLAY INTEGRATED EVENT ##############################################

    pedestal, gains = get_mc_calibration_coeffs(tel_num)
    disp.image = gains

    #disp.set_limits_minmax(0, 9000)
    disp.set_limits_percent(70)        # TODO

    # PLOT ##################################################################

    plt.savefig(output_file_path)

    if not quiet:
        plt.show()


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, required=True,
                        metavar="INTEGER",
                        help="The telescope to query (telescope number)")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    quiet = args.quiet
    simtel_file_path = args.fileargs[0]

    if args.output is None:
        output_file_path = "TEL{:03d}_GAIN.pdf".format(tel_num)
    else:
        output_file_path = args.output

    # DISPLAY IMAGES ##########################################################

    show_gains_image(simtel_file_path, output_file_path, tel_num, quiet)

