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

def get_mc_calibration_coeffs(tel_id):
    """
    Get the calibration coefficients from the MC data file to the
    data. This is ahack (until we have a real data structure for the
    calibrated data), it should move into `ctapipe.io.hessio_event_source`.

    RETURNS
    -------
    (pedestal, gains) : arrays of the pedestal and pe/dc ratios.
    """

    pedestal = pyhessio.get_pedestal(tel_id)
    gains = pyhessio.get_calibration(tel_id)

    return pedestal, gains


def show_pedestal_image(simtel_file_path, tel_num):

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

    # DISPLAY INTEGRATED EVENT ##############################################

    pedestal, gains = get_mc_calibration_coeffs(tel_num)

    print("pedestal:", pedestal)
    print("gains:", gains)


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, required=True,
                        metavar="INTEGER",
                        help="The telescope to query (telescope number)")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    show_pedestal_image(simtel_file_path, tel_num)

