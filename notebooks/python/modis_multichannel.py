
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Changes-to-modis_level1b_read" data-toc-modified-id="Changes-to-modis_level1b_read-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Changes to modis_level1b_read</a></span></li><li><span><a href="#Introduction" data-toc-modified-id="Introduction-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Reading-modis-data" data-toc-modified-id="Reading-modis-data-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Reading modis data</a></span><ul class="toc-item"><li><span><a href="#Using-pydf-to-get-metadata" data-toc-modified-id="Using-pydf-to-get-metadata-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Using pydf to get metadata</a></span></li><li><span><a href="#Find-all-the-datasets-using-pyhdf.SD.datasets()" data-toc-modified-id="Find-all-the-datasets-using-pyhdf.SD.datasets()-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Find all the datasets using pyhdf.SD.datasets()</a></span></li><li><span><a href="#open-one-of-the-datasets-(number-4,-EV_1KM_Emissive)-and-get-its-shape-and-data-type" data-toc-modified-id="open-one-of-the-datasets-(number-4,-EV_1KM_Emissive)-and-get-its-shape-and-data-type-3.3"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>open one of the datasets (number 4, EV_1KM_Emissive) and get its shape and data type</a></span></li><li><span><a href="#Get-the-first-row-of-the-first-channel-and-find-its-numpy-dtype" data-toc-modified-id="Get-the-first-row-of-the-first-channel-and-find-its-numpy-dtype-3.4"><span class="toc-item-num">3.4&nbsp;&nbsp;</span>Get the first row of the first channel and find its numpy dtype</a></span></li><li><span><a href="#get-all-the-rows-and-columns-for-the-first-channel" data-toc-modified-id="get-all-the-rows-and-columns-for-the-first-channel-3.5"><span class="toc-item-num">3.5&nbsp;&nbsp;</span>get all the rows and columns for the first channel</a></span></li><li><span><a href="#Find-the-attributes-for-EV_1KM_Emissive" data-toc-modified-id="Find-the-attributes-for-EV_1KM_Emissive-3.6"><span class="toc-item-num">3.6&nbsp;&nbsp;</span>Find the attributes for EV_1KM_Emissive</a></span></li><li><span><a href="#Print-the-first-1000-characters-of-the-Metadata.0-string" data-toc-modified-id="Print-the-first-1000-characters-of-the-Metadata.0-string-3.7"><span class="toc-item-num">3.7&nbsp;&nbsp;</span>Print the first 1000 characters of the Metadata.0 string</a></span></li></ul></li><li><span><a href="#Now-write-channels-out-into-a-new-hdf" data-toc-modified-id="Now-write-channels-out-into-a-new-hdf-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Now write channels out into a new hdf</a></span><ul class="toc-item"><li><span><a href="#find-the-index-for-channel-30" data-toc-modified-id="find-the-index-for-channel-30-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>find the index for channel 30</a></span></li><li><span><a href="#Let-python-figure-this-out" data-toc-modified-id="Let-python-figure-this-out-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>Let python figure this out</a></span></li><li><span><a href="#Read-channel-30-at-index-9-into-a-numpy-array-of-type-uint16" data-toc-modified-id="Read-channel-30-at-index-9-into-a-numpy-array-of-type-uint16-4.3"><span class="toc-item-num">4.3&nbsp;&nbsp;</span>Read channel 30 at index 9 into a numpy array of type uint16</a></span></li></ul></li><li><span><a href="#Calibrate-the-raw-counts-for-both-channels" data-toc-modified-id="Calibrate-the-raw-counts-for-both-channels-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Calibrate the raw counts for both channels</a></span></li><li><span><a href="#Write-the-calibrated-channel-out-for-safekeeping" data-toc-modified-id="Write-the-calibrated-channel-out-for-safekeeping-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Write the calibrated channel out for safekeeping</a></span></li><li><span><a href="#Move-the-file-to-data_dir" data-toc-modified-id="Move-the-file-to-data_dir-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Move the file to data_dir</a></span></li></ul></div>

# # Changes to modis_level1b_read
# 
# This notebook shows how to write both channel 30 and channel 31 out to an hdf file
# called modis_chans.hdf.  It uses two new functions to avoid repetiion
# 
# ```python
# get_index 
# ```
#    
# defined in section 3.2 and 
# 
# ```python
# write_chan 
# ```
#    
# defined in section 5

# In[1]:


from pathlib import Path
from pyhdf.SD import SD, SDC
import pprint
import numpy as np
from matplotlib import pyplot as plt
import context
from a301.utils.data_read import download


# # Introduction
# 
# This notebook assumes that you have gone to the LAADS DAAC archive and downloaded a Modis Level1b 5 minute granule from the Aqua satellite (a MYD021KM hdf file).  Below we use the pyhdf module to read a single channel (channel 30) centered at 9.7 microns according to [the Modis channel listing](https://modis.gsfc.nasa.gov/about/specifications.php).  We plot the raw counts from that channel using the 
# [matplotlib imshow](https://matplotlib.org/examples/images_contours_and_fields/image_demo.html) function to display the raw image
# 
# If you don't have a MYD021KM file you can grab mine by changing
# 
#      get_data=False
#   
# to True in the next cell.
#      
#      

# In[19]:


get_data=False
if get_data:
    modis_file="MYD021KM.A2013222.2110.061.2018047235850.hdf"
    download(modis_file)
    #
    # now move this from the notebooks folder to the data folder
    #
    
#Path.cwd finds the "current working directory"
this_dir=Path.cwd()
#move up one one folder and down to data
data_dir = this_dir.parent / Path('data')


# # Reading modis data

# ## Using pydf to get metadata
# 
# I can convert the filename from a Path object to a string object and pass it to pyhdf.SD
# to find out how many datasets and attributes there are in the file
# 
# In the cell below I use [f-strings](https://realpython.com/python-f-strings/) to simplify the print command,
# and split the string up across multiple lines by enclosing it in a tuple.  This works because
# when python sees that the individual lines aren't separated by a comma, it concatenates them together.
# The character \n means "newline"
# 
# Note that I need to construct the full path to the data file so pyhdf can find it. pyhdf was
# written before pathlib (which was introduced in python 3.5), 
# so I need to convert the Path object to a simple string using str()

# In[3]:


hdf_files=list(data_dir.glob("MYD021KM*2110*.hdf"))
hdf_files
file_name = str(data_dir / Path(hdf_files[0]))
print(f'reading {file_name}')
the_file = SD(file_name, SDC.READ)
stars='*'*50
print((f'\n{stars}\nnumber of datasets, number of attributes'
       f'={the_file.info()}\n{stars}\n'
       f'\nHere is the help file for the info funtion:\n'))
help(SD.info)


# ## Find all the datasets using pyhdf.SD.datasets()
# 
# The datasets method creates a dictionary holding pointers to the 31 datasets.
# List them below:

# In[4]:


datasets_dict = the_file.datasets()

for idx,sds in enumerate(datasets_dict.keys()):
    print(idx,sds)


# ## open one of the datasets (number 4, EV_1KM_Emissive) and get its shape and data type

# In[5]:


longwave_data = the_file.select('EV_1KM_Emissive') # select sds
print(longwave_data.info())
help(longwave_data.info)


# ## Get the first row of the first channel and find its numpy dtype
# 
# (unit16 is "unsigned 16 bit integer", which is how the modis raw counts are stored)

# In[6]:


data_row = longwave_data[0,0,:] # get sds data
print(data_row.shape,data_row.dtype)


# ## get all the rows and columns for the first channel

# In[7]:


longwave_data[0,:,:]


# ## Find the attributes for EV_1KM_Emissive

# In[8]:


pprint.pprint(longwave_data.attributes() )


# ## Print the first 1000 characters of the Metadata.0 string
# 
# Date, orbit number, etc. are stored in a long string attribute called 'StructMetadata.0'.  The \t character is a tab stop.

# In[9]:


pprint.pprint(the_file.attributes()['StructMetadata.0'][:1000])


# # Now write channels out into a new hdf

# In[10]:


longwave_bands = the_file.select('Band_1KM_Emissive')


# In[11]:


longwave_bands.attributes()


# Note that only channels 20 to 36 are in the Emissive dataset (see [the Modis channel listing](https://modis.gsfc.nasa.gov/about/specifications.php))

# ## find the index for channel 30
# 
# Count the following and convince yourself that channel 30 is index 9, starting from 0

# In[12]:


band_nums=longwave_bands.get()
print(f'here are the modis channels in the emissive dataset \n{band_nums}')


# ## Let python figure this out
# 
# We don't want to have to count, so use numpy.searchsorted to find the the index with value closest to 30
# 
# We need to turn that index (type int64) into a plain python int so it can be used to specify the channel
# (float doesn't work)

# In[13]:


def get_index(band_nums,chan_num):
    """
    given the longwave_bands vecto from the level1b file, 
    find the index of the channel chan_num in the dataset
    
    Parameters
    ----------
    
    band_nums: numpy float vector
       list of channel numbers
       
    chan_num: float or int
       channel number to get index for
       
    Returns
    -------
    
    the_index: int
        index of channel in modis image

    """
    ch_index=np.searchsorted(band_nums,chan_num)
    return int(ch_index)


ch30_index=get_index(band_nums,30.)
ch31_index=get_index(band_nums,31.)
print(f'channel 30 is located at index {ch30_index} and channel 31 at {ch31_index}')


# ## Read channel 30 at index 9 into a numpy array of type uint16

# In[14]:


ch30_data = longwave_data[ch30_index,:,:]
ch31_data = longwave_data[ch31_index,:,:]
print(ch30_data.shape)
print(ch30_data.dtype)


# # Calibrate the raw counts for both channels
# 
# To turn the raw counts into pixel radiances, you need to apply equation 5.8 on p. 36 of the 
# [modis users guide](https://www.dropbox.com/s/ckd3dv4n7nxc9p0/modis_users_guide.pdf?dl=0):
# 
# $Radiances = (RawData - offset) \times scale$
# 
# We have just read the RawData,  the offset and the scale are stored in two vectors that are attributes of the Emissive dataset.  Make a version of the figure above, but plot Channel 30 radiance (in W/m^2/micron/sr), rather than raw counts.
# 
# 

# In[15]:


scales=longwave_data.attributes()['radiance_scales']
offsets=longwave_data.attributes()['radiance_offsets']
ch30_scale=scales[ch30_index]
ch30_offset=offsets[ch30_index]
ch31_scale=scales[ch31_index]
ch31_offset=offsets[ch31_index]
print(f'ch30 scale: {ch30_scale}, ch30 offset: {ch30_offset}')
print(f'ch31 scale: {ch31_scale}, ch31 offset: {ch31_offset}')


# In[16]:


ch30_calibrated =(ch30_data - ch30_offset)*ch30_scale
ch31_calibrated =(ch31_data - ch31_offset)*ch31_scale


# # Write the calibrated channel out for safekeeping
# 
# Follow the example here: https://hdfeos.org/software/pyhdf.php

# In[17]:


def write_chan(sd,numpy_array,chan_name):
    """
    given an open pyhdf SD object, a numpy_array and a 
    string channel name, write the channel out to the sd
    """
    # Create a dataset
    sds = sd.create(chan_name, SDC.FLOAT64, ch30_calibrated.shape)

    # Fill the dataset with a fill value
    sds.setfillvalue(0)

    # Set dimension names
    dim1 = sds.dim(0)
    dim1.setname("row")
    dim2 = sds.dim(1)
    dim2.setname("col")

    # Assign an attribute to the dataset
    sds.units = "W/m^2/micron/sr"

    # Write data
    sds[:,:] = numpy_array

    # Close the dataset
    sds.endaccess()

# Create an HDF file
outname="modis_chans.hdf"
sd = SD(outname, SDC.WRITE | SDC.CREATE)

#
# write out two channels
#
write_chan(sd,ch30_calibrated,'ch30')
write_chan(sd,ch31_calibrated,'ch31')

# Flush and close the HDF file
sd.end()


# # Move the file to data_dir

# In[18]:


local_file = Path.cwd() / Path(outname)
to_file = data_dir / Path(outname)
local_file.rename(to_file)

