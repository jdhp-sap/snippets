#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
... TODO
"""

__all__ = ['extract_image',
           'crop_sctcam_image',
           'crop_astri_image']

import argparse
from astropy.io import fits
import numpy as np
import os

import ctapipe
from ctapipe.io.hessio import hessio_event_source

def extract_image(simtel_file_path, tel_num, event_id, channel=0):

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

    # CHECK THE IMAGE GEOMETRY (ASTRI AND SCTCAM ONLY) ######################

    x, y = event.meta.pixel_pos[tel_num]
    foclen = event.meta.optical_foclen[tel_num]
    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

    if geom.pix_type != "rectangular":
        raise ValueError("The input image is not a valide ASTRI or SCTCam telescope image.")

    # GET AND CROP THE IMAGE ################################################

    image = event.dl0.tel[tel_num].adc_sums[channel]         # 1D numpy array

    if geom.cam_id == "ASTRI":
        cropped_img = crop_astri_image(image)
    elif geom.cam_id == "SCTCam":
        cropped_img = crop_sctcam_image(image)
    else:
        raise ValueError("The input image is not a valide ASTRI or SCTCam telescope image.")

    # GET AND CROP THE PHOTOELECTRON IMAGE ##################################

    pe_image = event.mc.tel[tel_num].photo_electrons       # 1D numpy array

    if geom.cam_id == "ASTRI":
        cropped_pe_img = crop_astri_image(pe_image)
    elif geom.cam_id == "SCTCam":
        cropped_pe_img = crop_sctcam_image(pe_image)
    else:
        raise ValueError("The input image is not a valide ASTRI or SCTCam telescope image.")

    return (cropped_img, cropped_pe_img)


def crop_sctcam_image(input_img):
    """
    Crop images comming form "SCTCam" telescopes in order to get regular 2D "rectangular"
    images directly usable with most image processing tools.

    Parameters
    ----------
    input_img : numpy.array
        The image to crop

    Returns
    -------
    A numpy.array containing the cropped image.
    """

    raise Exception("Not yet implemented")


def crop_astri_image(input_img):
    """
    Crop images comming form "ASTRI" telescopes in order to get regular 2D "rectangular"
    images directly usable with most image processing tools.

    Parameters
    ----------
    input_img : numpy.array
        The image to crop

    Returns
    -------
    A numpy.array containing the cropped image.
    """

    # Check the image
    if len(input_img) != (37*64):
        raise ValueError("The input image is not a valide ASTRI telescope image.")

    # Make the transformation map
    img_map = np.zeros([8*5, 8*5], dtype=int)

    img_map[0*8:1*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 29 * 64
    img_map[0*8:1*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 30 * 64
    img_map[0*8:1*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 31 * 64
    img_map[0*8:1*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 32 * 64
    img_map[0*8:1*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 33 * 64

    img_map[1*8:2*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 23 * 64
    img_map[1*8:2*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 24 * 64
    img_map[1*8:2*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 25 * 64
    img_map[1*8:2*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 26 * 64
    img_map[1*8:2*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 27 * 64

    img_map[2*8:3*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 16 * 64
    img_map[2*8:3*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 17 * 64
    img_map[2*8:3*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 18 * 64
    img_map[2*8:3*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 19 * 64
    img_map[2*8:3*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 20 * 64

    img_map[3*8:4*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] +  9 * 64
    img_map[3*8:4*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 10 * 64
    img_map[3*8:4*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 11 * 64
    img_map[3*8:4*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 12 * 64
    img_map[3*8:4*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 13 * 64

    img_map[4*8:5*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] +  3 * 64
    img_map[4*8:5*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] +  4 * 64
    img_map[4*8:5*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] +  5 * 64
    img_map[4*8:5*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] +  6 * 64
    img_map[4*8:5*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] +  7 * 64

    # Make the output image
    cropped_img = input_img[[img_map.ravel()]].reshape([8*5, 8*5])

    return cropped_img


def save_fits(img, pe_img, output_file_path):
    """
    img is the image and it should be a 2D or a 3D numpy array with values.
    """

    if img.ndim not in (2, 3):
        raise Exception("The input image should be a 2D or a 3D numpy array.")

    # http://docs.astropy.org/en/stable/io/fits/appendix/faq.html#how-do-i-create-a-multi-extension-fits-file-from-scratch
    hdu0 = fits.PrimaryHDU(img)
    hdu1 = fits.ImageHDU(pe_img)

    hdu_list = fits.HDUList([hdu0, hdu1])

    if os.path.isfile(output_file_path):
        os.remove(output_file_path)

    hdu_list.writeto(output_file_path)


def main():

    # PARSE OPTIONS ###########################################################

    desc = "TODO."
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

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    channel = args.channel
    event_id = args.event
    simtel_file_path = args.fileargs[0]

    if args.output is None:
        output_file_path = "TEL{:03d}_EV{:05d}_CH{:03d}.fits".format(tel_num, event_id, channel)
    else:
        output_file_path = args.output

    # EXTRACT AND CROP THE IMAGE ##############################################

    (cropped_img, cropped_pe_img) = extract_image(simtel_file_path, tel_num, event_id, channel)

    # SAVE THE IMAGE ##########################################################

    save_fits(cropped_img, cropped_pe_img, output_file_path)


if __name__ == "__main__":
    main()

