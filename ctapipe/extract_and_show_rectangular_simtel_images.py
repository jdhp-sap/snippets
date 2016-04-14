#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract simulated camera images from a simtel file.

Inspired by ctapipe/examples/read_hessio_single_tel.py
"""

import argparse
import os

import ctapipe
import ctapipe.visualization
from ctapipe.utils.datasets import get_example_simtelarray_file
from ctapipe.io.hessio import hessio_event_source

import numpy as np

import PIL.Image as pil_img # PIL.Image is a module not a class...


def extract_image(simtel_file_path, tel_num=1, channel=0, event_index=0):

    # CONFIG ################################################################

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

    # DISPLAY TIME-VARYING EVENT ############################################

    #data = event.dl0.tel[tel_num].adc_samples[channel]
    #for ii in range(data.shape[1]):
    #    image = data[:, ii]

    #    file_name = 'CT{:03d}_EV{:010d}_S{:02d}.png'.format(tel_num, event.dl0.event_id, ii))
    #    save_image(image, file_name)

    # DISPLAY INTEGRATED EVENT ##############################################

    image = event.dl0.tel[tel_num].adc_sums[channel]

    return image


def save_image(image, file_name):

    # NORMALIZE PIXELS VALUE ##################################

    image -= image.min()
    image /= image.max()
    image *= 255
    
    # CROP ####################################################

    # A dirty hack to get truely rectangular images without blank parts in borders...
    num_px_skipped = 8*8*4
    image = image[num_px_skipped:-num_px_skipped] 

    # SAVE THE IMAGE ##########################################

    mode = "L"       # Grayscale

    pil_image = pil_img.new(mode, (48, 32))  # TODO
    pil_image.putdata(image)

    pil_image.save(file_name)


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Extract simulated camera images from a simtel file."
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

    parser.add_argument("--output", "-o", default=None,
                        metavar="PATH",
                        help="The path of the output file")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    channel = args.channel
    event_index = args.event
    output_file_path = args.output
    simtel_file_path = args.fileargs[0]

    base_file_path = os.path.basename(simtel_file_path)
    base_file_path = os.path.splitext(base_file_path)[0]

    # MAKE IMAGES #############################################################

    img = extract_image(simtel_file_path, tel_num, channel, event_index)

    if output_file_path is None:
        output_file_path = '{}_TL{:03d}_EV{:010d}.png'.format(base_file_path,
                                                              tel_num,
                                                              event_index)
    save_image(img, output_file_path)

