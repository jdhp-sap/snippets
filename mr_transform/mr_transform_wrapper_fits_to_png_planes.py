#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation: http://docs.astropy.org/en/stable/io/fits/index.html

import argparse
from astropy.io import fits

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


MR_OUTPUT_FILE_PATH = "out.fits"

# PARSE OPTIONS ###############################################################

parser = argparse.ArgumentParser(description="MrTransform wrapper.")

parser.add_argument("filearg", nargs=1, metavar="FILE",
                    help="the FITS file to process")

args = parser.parse_args()

input_file_path = args.filearg[0]


# EXECUTE MR_TRANSFORM ########################################################

# TODO: improve the following lines
cmd = 'mr_transform -n5 "{}" out'.format(input_file_path)
os.system(cmd)

# TODO: improve the following lines
cmd = "mv out.mr {}".format(MR_OUTPUT_FILE_PATH)
os.system(cmd)


# READ THE MR_TRANSFORM OUTPUT FILE ###########################################

# Open the FITS file
hdu_list = fits.open(MR_OUTPUT_FILE_PATH)

for hdu_id, hdu in enumerate(hdu_list):             # TODO: ONLY ONE HDU EXPECTED ???
    data = hdu.data   # "hdu.data" is a Numpy Array

    if data.ndim != 3:
        raise Exception("The input FITS file should contain only one (2D) image.")

    for img_index, img in enumerate(data):
        fig = plt.figure(figsize=(8.0, 8.0))
        ax = fig.add_subplot(111)
        ax.imshow(img, interpolation='nearest', cmap=cm.gray)
        plt.savefig("HDU{}_{}.png".format(hdu_id, img_index))

# Close the FITS file
hdu_list.close()

