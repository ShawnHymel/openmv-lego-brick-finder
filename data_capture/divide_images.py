#!/usr/bin/env python3

"""
Divide Images

Script to break image files into smaller, sub-images that are used to train a 
machine learning model.

You will need the following packages (install via pip):
 * shutil
 * Pillow

Example call:
python divide_images.py -i "../../../Python/datasets/lego/raw/background"
    -o "../../../Python/datasets/lego/edited/background" -n "background" 
    -w 32 -t 32 -l 10

The MIT License (MIT)

Copyright (c) 2020 Shawn Hymel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import argparse
import struct
from os import makedirs, listdir, rename
from os.path import isdir, join, exists

import shutil
from PIL import Image

import utils

# Authorship
__author__ = "Shawn Hymel"
__copyright__ = "Copyright 2020, Shawn Hymel"
__license__ = "MIT"
__version__ = "0.1"

# Settings
file_suffix = ".bmp"

################################################################################
# Main

###
# Parse command line arguments

# Script arguments
parser = argparse.ArgumentParser(description="Image curation tool that divides "
                                                "each image in a directory "
                                                "into a set of sub-images.")
parser.add_argument('-i',
                   '--in_dir',
                   action='store',
                   dest='in_dir',
                   type=str,
                   required=True,
                   help="Directory where the raw, large background images are "
                        "stored")   
parser.add_argument('-o',
                   '--out_dir',
                   action='store',
                   dest='out_dir',
                   type=str,
                   required=True,
                   help="Directory where the sub-images are to be stored")
parser.add_argument('-n',
                   '--name',
                   action='store',
                   dest='name',
                   type=str,
                   required=True,
                   help="Prefix name of each image")
parser.add_argument('-w',
                   '--width',
                   action='store',
                   dest='width',
                   type=str,
                   required=True,
                   help="Desired width of sub-image")
parser.add_argument('-t',
                   '--height',
                   action='store',
                   dest='height',
                   type=str,
                   required=True,
                   help="Desired height of sub-image")
parser.add_argument('-l',
                   '--hop_length',
                   action='store',
                   dest='hop_length',
                   type=str,
                   required=True,
                   help="Hop distance (in pixels) from start of one sub-image "
                        "window to the next, horizontally and vertically")

# Parse arguments
args = parser.parse_args()
in_dir = args.in_dir
out_dir = args.out_dir
file_prefix = args.name
sub_w = int(args.width)
sub_h = int(args.height)
hop = int(args.hop_length)

###
# Welcome screen

# Print tool welcome message
print("-----------------------------------------------------------------------")
print("Dataset Curation Tool")
print("v" + __version__)
print("-----------------------------------------------------------------------")

###
# Set up output directory

# Delete output directory if it already exists
if isdir(out_dir):
    print("WARNING: Output directory already exists:")
    print(out_dir)
    print("This tool will delete the output directory and everything in it.")
    resp = utils.query_yes_no("Continue?")
    if resp:
        print("Deleting and recreating output directory.")
        #rename(out_dir, out_dir + '_') # One way to deal with "cannot access"
        shutil.rmtree(out_dir)
        time.sleep(1.0)
    else:
        print("Please delete directory to continue. Exiting.")
        exit()

# Create output dir
if not exists(out_dir):
    makedirs(out_dir)
else:
    print("ERROR: Output directory could not be deleted. Exiting.")
    exit()

###
# Save sub-images

# Counter for filename
file_count = 0

# Initialize top-left markers
px_left = 0
px_top = 0

# Get original files
file_list = [name for name in listdir(in_dir)]

# Go through each image, cropping out sub-images
for name in file_list:

    # Open image and get dimensions
    file_path = join(in_dir, name)
    im = Image.open(file_path)
    width, height = im.size

    # Crop and save, crop and save
    while(px_top + sub_h <= height):
        while(px_left + sub_w <= width):
                
            # Crop a portion
            im_crop = im.crop((px_left, px_top, px_left + sub_w, px_top + sub_h))

            # Save sub-image
            out_file = file_prefix + "_" + str(file_count) + file_suffix
            im_crop.save(join(out_dir, out_file))

            # Add a little something
            file_count += 1

            # Incrememnt our pixa left
            px_left += hop

        # Increment our pixa top
        px_top += hop
        px_left = 0

# Say we're done
print("Done!")
exit()