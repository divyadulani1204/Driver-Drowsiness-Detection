# Face_Detection_Haar_Cascade

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

## For further technical details click [here](https://viswalahiri.github.io/Face_Detection_Haar_Cascade/scripts/)

## Description

Face detection performed with the help of the Haar Cascade Frontal Face Model.

Implemented with [OpenCV](https://pypi.org/project/opencv-python/) (Python 3) in Python, this repository contains code that enables the use of Computer Vision algorithms and facilities. These faces can be further used as inputs to a facial recognition model.

## About Haar-Cascade

The Haar-Cascade algorithm is a machine learning object detection algorithm, that can be used to identify specific objects based upon the features that are found in an image or many images played together (i.e., video).

## Prerequisites and Installation

This package assumes you use Python 3.x.

Expected package dependencies are listed in the "requirements.txt" file for PIP, you need to run the following command to get dependencies:

pip install -r requirements.txt


## Examples

### Input

Use a folder with one/multiple photo(s) with one or more faces, as an input for the algorithm.


<p align = "center" ><img src="assets/family.jpg"> </p>



### Execution

Run main.py.



> Enter Path Where Images Exists.
C:\SPECIFY_PATH_OF_EXISTANCE
> Enter Path Where You Would Like to Push.
C:\SPECIFY_PATH_TO_PUSH

### Output

Photos corresponding to individual faces get pushed to the folder specified in path

<p align = "center" ><img src="assets/detected_faces.gif"> </p>
