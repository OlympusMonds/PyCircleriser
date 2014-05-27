#============================================================================
# Name        : circ-pic.py
# Author      : Luke Mondy
# ============================================================================
#
# Copyright (C) 2012 Mondy Luke
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ============================================================================

from __future__ import division
import sys
import Image, ImageDraw
import argparse
import numpy as np
from math import sqrt

HAVE_PYPRIND = True
try:
    import pyprind
except ImportError:
    HAVE_PYPRIND = False

LOGGING = False

def log(message):
    global LOGGING
    if LOGGING:
        print message
        sys.stdout.flush()


def getImage(image, scale=1.0, grey=True):
    try:
        log("Opening image: %s" % image)
        im = Image.open(image)
    except Exception as e:
        error_msg = ("Image file you provided:\n{image}\ndoes not exist! Here's what the computer"
                     "says:\n{exception}".format(image=image, exception=e))
        sys.exit(error_msg)

    if scale != 1.0:
        im = im.resize(tuple(int(i * scale) for i in im.size))

    if grey:
        im = im.convert('L')
    return im


def overlapping(c1, c2):
    # circle data type:
    #   (x, y, rad)
    dist = sqrt( (c2[0] - c1[0])**2 + (c2[1] - c1[1])**2 ) # This sqrt is killin' me...
    if c1[2] + c2[2] > dist:
        return True
    return False


def render(circles, path, params, imsize):
    log("Rendering...")

    if params['bgimg']:
        bg = getImage(params['bgimg'], grey=False)
        bgim = bg.resize(imsize)
        bgpix = bgim.load()

    col = params['bgcolour']
    col = 255 if col > 255 else col
    col = 0 if col < 0 else col
    bgcolour = (col, col, col)

    outline = (0, 0, 0)
    if params['nooutline']:
        outline = None
    
    final = Image.new('RGB', imsize, bgcolour)
    draw = ImageDraw.Draw(final)

    im_x, im_y = imsize
    
    for y in range(im_y):
        for x in range(im_x):
            circle_radius = circles[x,y]
            if circle_radius != 0:
                bb = (x - circle_radius, y - circle_radius, 
                      x + circle_radius, y + circle_radius)
                fill = bgpix[x, y] if params['bgimg'] else (255, 255, 255)
                draw.ellipse(bb, fill=fill, outline=outline)
    del draw
    final.save(params['outimg'])


def circlerise(params):
    global LOGGING
    global HAVE_PYPRIND

    interval = params['interval']
    maxrad = params['maxrad']
    scale = params['scale']
    
    im = getImage(params['circimg'], scale)
    
    pixels = im.load()
    circles = np.zeros(im.size, int)

    """ 
    === Algorithm ===
    For each pixel in the original image, determine its
    "grey" brightness, and determine an appropriate radius
    for that.
    Now look in the local region for other circles (local
    is determined by the max_radius of other circles + the
    radius of the current potential circle).
    If there is some circles nearby, check to see if the
    new circle will overlap with it or not. If all nearby
    circles won't overlap, then record the radius in a 2D
    array that corresponds to the image.
    """

    im_x, im_y = im.size
    skips = 0

    if LOGGING  and HAVE_PYPRIND :
        progress = pyprind.ProgBar(im_y, stream=1)

    for y in range(0, im_y, interval):
        prev_rad = 0
        closeness = 0
        for x in range(0, im_x, interval):
            closeness += 1

            # Determine radius
            greyval = pixels[x, y]
            radius = int(maxrad * (greyval/255))
            if radius == 0:
                radius = 1

            # If we are still going to be inside the last circle
            # placed on the same X row, save time and skip.
            if prev_rad + radius >= closeness:
                skips += 1
                continue
            
            bb = [x - radius - maxrad,  # Define bounding box.
                  y - radius - maxrad, 
                  x + radius + maxrad, 
                  y + radius + maxrad]

            
            if bb[0] < 0:       # Ensure the bounding box is OK with 
                bb[0] = 0       # edges. We don't need to check the 
            if bb[1] < 0:       # outer edges because it's OK for the
                bb[1] = 0       # centre to be right on the edge.
            if bb[2] >= im_x:
                bb[2] = im_x - 1
            if bb[3] >= im_y:
                bb[3] = im_y - 1
            
            c1 = (x, y, radius)
            
            # Use bounding box and numpy to extract the local area around the
            # circle. Then use numpy to do a boolean operating to give a 
            # true/false matrix of whether circles are nearby.
            local_area = circles[bb[0]:bb[2], bb[1]:bb[3]]
            circle_nearby = local_area != 0
           
            coords_of_local_circles = np.where(circle_nearby)
            radii_of_local_cirles = np.expand_dims(local_area[circle_nearby], axis=0)  # Need the extra dim for next step
            nrby_cirles = np.vstack([coords_of_local_circles, radii_of_local_cirles])
            nrby_cirles = nrby_cirles.transpose()

            any_overlaps_here = False
            if nrby_cirles.shape[0] == 0:
                circles[x,y] = radius
                prev_rad = radius
                closeness = 0
            else:
                for n in nrby_cirles:
                    c2 = (n[0]+bb[0], n[1]+bb[1], n[2]) 
                    overlap = overlapping(c1, c2)        
                    if overlap:
                        any_overlaps_here = True
                        break
                # Look if any nearby circles overlap. If any do, don't make
                # a circle here.
                if not any_overlaps_here:               
                    circles[x, y] = radius 
                    prev_rad = radius
                    closeness = 0
        if LOGGING is True and HAVE_PYPRIND is True:
            progress.update()

    log("Avoided {skips} calculations".format(skips=skips))

    render(circles, "", params, im.size)



def main(argv=None):    
    parser = argparse.ArgumentParser(description="Using imgcirc!")

    addarg = parser.add_argument # just for cleaner code
    
    addarg("--circimg", type=str, required=True,
            help="The image that will make up the circles.", )

    addarg("--interval", type=int, default=1, 
            help="Interval between pixels to look at in the circimg. 1 means all pixels.")
    
    addarg("--bgimg", type=str, 
            help="An image to colour the circles with. Will be resized as needed.")
    
    addarg("--outimg", type=str, required=True,
            help="Filename for the outputted image.")
    
    addarg("--maxrad", type=int, default=10,
            help="Max radius of a circle (corresponds to a white pixel)")
    
    addarg("--scale", type=float, default=1,
            help="Percent to scale up the circimg (sometimes makes it look better).")

    addarg("--bgcolour", type=int, default=255,
            help="Grey-scale val from 0 to 255")

    addarg("--nooutline", action='store_true', default=False,
            help="When specified, no outline will be drawn on circles.")

    addarg("--log", action='store_true', default=False,
            help="Write progress to stdout.")
    
    parsed_args = parser.parse_args()
    params = dict(parsed_args.__dict__)

    global LOGGING
    if params["log"] is True:
        LOGGING = True

    log("Begin circlerising...")
    circlerise(params)


if __name__ == "__main__":
    sys.exit(main())
