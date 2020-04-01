# Simple-Pansharpening-Algorithms
Python implementation of some simple algorithms for pansharpening remote sensing images

This repository contains a function which takes as input multispectral and panchromatic remote sensing images, and outputs a pansharpened 
version of the multispectral image using either one of the following algorithms:
- Simple Brovey
- Simple Mean
- ESRI
- Brovey

This function is mainly adapted from the source code written by Vladimir Osin in his Kaggle Kernel 'Panchromatic Sharpening' in the link
https://www.kaggle.com/resolut/panchromatic-sharpening. 

The implementation in this repository is mainly to adapt his code to accept raster multispectral and panchromatic files as inputs instead 
of the images in their array form, generalize the code for accepting multispectral images with differing number of bands and band order, 
and also to generate the raster pansharpened image file as well.

Requirements:
- cv2
- gc
- numpy
- rasterio


A zoomed - in portion of a GeoEye - 1 sample image (courtesy of European Space Agency) is used to illustrate the Brovey pansharpening technique.


Test Multispectral Image (Courtesy of European Space Agency):
![Alt text](https://github.com/ThomasWangWeiHong/Simple-Pansharpening-Algorithms/blob/master/Test_MS.JPG)

Test Panchromatic Image (Courtesy of European Space Agency):
![Alt text](https://github.com/ThomasWangWeiHong/Simple-Pansharpening-Algorithms/blob/master/Test_Pan.JPG)

Pansharpened Image (Simple Brovey):
![Alt text](https://github.com/ThomasWangWeiHong/Simple-Pansharpening-Algorithms/blob/master/Test_PSH_Simple_Brovey.JPG)

Pansharpened Image (Brovey with weight of 0.15):
![Alt text](https://github.com/ThomasWangWeiHong/Simple-Pansharpening-Algorithms/blob/master/Test_PSH_Brovey_015.JPG)
