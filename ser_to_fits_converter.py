import ser_reader as sr
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from astropy.io import fits
import sys

filenames = sys.argv[1:]

def ser_to_cube(filename):
    """
    Making a data cube consisting of all 25 frames from the .ser
    video file, where axis 0 and 1 are x and y coordinates in the
    image and axis 2 is the frame within the .ser video file.
    """

    data = sr.reader(filename)
    cont = True
    i = 0

    while (cont):
        try:
            temp = data.getImg(i)[:,:,0]
            i = i + 1
        except: 
            cont = False
    
    num_frame = i - 1
    array = np.zeros((1000,1000,num_frame))
    
    for i in range(num_frame):
        try:
            array[:,:,i] = data.getImg(i)[:,:,0]
        except:
            print("one frame is fucked")
            pass
    return array, num_frame

def make_one_fits(array, frame_num):

    frame_num = str(frame_num)
    if (array.shape != (1000,1000)):
        """
        Raise an exception if the size of the input array is not the
        correct size required for writing the fits file, avoiding
        future errors.
        """
        raise Exception("Incorrect array shape. Shape must be (1000, 1000), but you input a " + str(array.shape) + " sized array.")    
    else:
        """
        Write a single fits file consisting of the date, time,
        exposure time, and the frame number in the .ser video file.
        """
        str_frame_num = str('%0*d' % (3, int(frame_num)))
        fits_filename = date + "_" + time + "_" + exptime + "_" + str_frame_num + ".fits"
        hdu = fits.PrimaryHDU(array)
        hdu.writeto(fits_filename)
        
        """
        Now editing the fits header to match the details of the
        data.
        """
        with fits.open(fits_filename, 'update') as f:
            for hdu in f:
                hdu.header['TARGET'] = 'Sol'
                hdu.header['DATE'] = date
                hdu.header['TIME'] = time
                hdu.header['FRAME'] = frame_num
    return

total_fits_files = 0
for filename in filenames:
    date = filename[8:18]
    time = filename[19:25]
    exptime = filename[26:31]
    cube, num_frame = ser_to_cube(filename)

    for i in range(0,num_frame):
        make_one_fits(cube[:,:,i], i)
    
    total_fits_files = total_fits_files + num_frame
print("Converted " + str(len(filenames)) + " .ser files into " + str(total_fits_files) + " .fits files.")
