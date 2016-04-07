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

parser.add_argument("--number_of_scales", "-n", type=int, default=4, metavar="INTEGER",
                    help="number of scales used in the multiresolution transform (default: 4)")
parser.add_argument("filearg", nargs=1, metavar="FILE",
                    help="the FITS file to process")

args = parser.parse_args()

number_of_scales = args.number_of_scales
input_file_path = args.filearg[0]


# EXECUTE MR_TRANSFORM ########################################################

# TODO: improve the following lines
cmd = 'mr_transform -n{} "{}" out'.format(number_of_scales, input_file_path)
os.system(cmd)

# TODO: improve the following lines
cmd = "mv out.mr {}".format(MR_OUTPUT_FILE_PATH)
os.system(cmd)


# READ THE MR_TRANSFORM OUTPUT FILE ###########################################

# Open the FITS file
hdu_list = fits.open(MR_OUTPUT_FILE_PATH)

if len(hdu_list) != 1:
    raise Exception("Unexpected error: the output FITS file should contain only one HDU.")

data = hdu_list[0].data   # "hdu.data" is a Numpy Array

if data.ndim != 3:
    raise Exception("Unexpected error: the output FITS file should contain a 3D array.")

for img_index, img in enumerate(data):
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.imshow(img, interpolation='nearest', cmap=cm.gray)
    plt.savefig("mr_{}.png".format(img_index))

# Close the FITS file
hdu_list.close()

