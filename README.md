PyCircleriser
=============

Turns images into clusters of circles, with the radius determined by pixel brightness.

Dependencies
============
 - PIL
 - Numpy
 - PyPrind (optional)

Examples
========
A random face from Google images:

![face](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/images/face-2.jpg)

to this:

![circle face](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/outputs/face-2.jpg)

Using the command:

```python PyCircleriser.py --circimg images/face-2.jpg --outimg outputs/face-2.jpg --log```

![monet](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/images/monet-starry.jpg)

to this:

![monet](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/outputs/monet-starry.jpg)

Using the command:

```python PyCircleriser.py --circimg images/monet-starry.jpg --outimg outputs/monet-starry.jpg --log```

There are also a few modifiers you can use, for example:

```python PyCircleriser.py --circimg images/monet-starry.jpg --outimg outputs/monet-starry_flags.jpg --bgimg images/monet-starry.jpg --bgcolour 0 --log --nooutline```

![monet](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/outputs/monet-starry_flags.jpg)

And another example, with a different background colouring, and scaling (which often can improve the look of an output):

```python PyCircleriser.py --circimg images/face-2.jpg --outimg outputs/face-2-colour.jpg --log --bgimg images/union-jack.png --scale 2```

![circle face](https://raw.githubusercontent.com/OlympusMonds/PyCircleriser/master/outputs/face-2-colour.jpg)

To do
=====
 - Add option to render progressively (to make a gif or whatnot)
 - General speed ups (see lineprofile.txt)

Help
====
I'm no noob, but I'm hardly a pro (and I never get code reviews), so if you find some code odd or inefficient, please let me know or submit a pull request. I would be super appreciative.
