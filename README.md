PyCircleriser
=============

Turns images into clusters of circles, with the radius determined by pixel brightness.

Dependencies
============
 - PIL
 - Numpy
 - ProgressBar

Examples
========
A random face from Google images:

![face](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/images/face-2.jpg)

to this:

![circle face](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/outputs/face-2.jpg)

![monet](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/images/monet-starry.jpg)

to this:

![monet](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/outputs/monet-starry.jpg)


To do
=====
 - Add option to render progressively (to make a gif or whatnot)
 - General speed ups (see lineprofile.txt)
 - Log option does not suppress progress bar (maybe just remove logging?)
 - ProgressBar is good, but makes the code somewhat unlibrary-able (read up on ProgressBar - maybe it has options?)