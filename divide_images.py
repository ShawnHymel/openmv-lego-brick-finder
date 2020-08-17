#!/usr/bin/env python3

"""
Divide Images

Script to break image files into smaller, sub-images that are used to train a 
machine learning model.

You will need the following packages (install via pip):

Example call:
python divide_images.py -i "../../Python/datasets/lego/raw/background"
    -o "../../Python/datasets/lego/edited/background" -w 28 -h 28 -l 14

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

import argparse
from os import makedirs, listdir, rename
from os.path import isdir, join, exists

# Authorship
__author__ = "Shawn Hymel"
__copyright__ = "Copyright 2020, Shawn Hymel"
__license__ = "MIT"
__version__ = "0.1"

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
sub_w = args.width
sub_h = args.height
hop = args.hop_length

###
# Welcome screen

# Print tool welcome message
print("-----------------------------------------------------------------------")
print("Dataset Curation Tool")
print("v" + __version__)
print("-----------------------------------------------------------------------")

# TEST
print(in_dir)
print(out_dir)
print(sub_w)
print(sub_h)
print(hop)