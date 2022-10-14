# MSBACN
Python project to find location based on an image of the night sky

This project is very much still in progress, and is not able to be run on systems other than the laptop I designed it on as of now. 
Much of the fine tuning for the field of view of the image and rotation of the image are unfinished, 
and the system to automatically find the values is not yet finished, so the values used are values specifically created to work with the set of images I collected and tested with.

The commented sections are often results of troubleshooting, so they may be helpful in seeing the thought process behind developing the system.


detectBrightSpots.py is for finding the locations of stars in images and exports a txt file with their relative locations to be compared against, used as a shell command.
rotatePoints.py, convertCoord.py, and compareCoordinates.py are all dependencies for photoSkyPlot.py
rotatePoints is used to generate new plots of star locations in the sky to account for the top of the image not being pointed due north
convertCoord is used to convert points from altitude and azimuth which signify location in the sky to x and y coordinates which can be compared to what the image points appear to be
photoSkyPlot is the main file, it combindes the functions of all the dependencies generates plots for a variety of locations around the earth to see which fits the image best
