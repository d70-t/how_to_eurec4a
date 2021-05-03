#!/usr/bin/env python
# coding: utf-8

# # SMART dataset
# 
# The following script exemplifies the access and usage of SMART data measured during EUREC4A. The Spectral Modular Airborne Radiation measurement sysTem (SMART) measures downward irradiances in the solar spectral range between 300 nm and 2200 nm.
# 
# More information on the dataset can be found in {cite}`Stevens:2019` and {cite}`Wendisch:2001`. If you have questions or if you would like to use the data for a publication, please don't hesitate to get in contact with the dataset authors as stated in the dataset attributes `contact` or `author`.

# In[1]:


get_ipython().run_line_magic('pylab', 'inline')


# ## Get data
# * To load the data we first load the EUREC4A meta data catalogue. More information on the catalog can be found [here](https://github.com/eurec4a/eurec4a-intake#eurec4a-intake-catalogue).

# In[2]:


import eurec4a


# In[3]:


cat = eurec4a.get_intake_catalog()
list(cat.HALO.SMART)


# * We can further specify the platform, instrument, if applicable dataset level or variable name, and pass it on to dask.
# 
# *Note: have a look at the attributes of the xarray dataset `ds` for all relevant information on the dataset, such as author, contact, or citation infromation.*

# In[4]:


ds_smart = cat.HALO.SMART.spectral_irradiances['HALO-0205'].to_dask()
ds_smart


# The available dataset includes irradiances for six selected wavelengths (422nm, 532nm, 648nm, 858nm, 1238nm, 1638nm). The full dataset is available on demand. Contact the dataset authors as stated in the dataset attributes `contact`.
# 
# First Quickplot of whole flight (one wavelength)

# In[5]:


ds_smart.F_down_solar_wl_422.plot()


# ## Load HALO flight phase information
# All HALO flights were split up into flight phases or segments to allow for a precise selection in time and space of a circle or calibration pattern. For more information have a look at the respective [github repository](https://github.com/eurec4a/halo-flight-phase-separation).

# In[6]:


meta = eurec4a.get_flight_segments()


# We select the flight phase we are interested in, e.g. the second circle on February 5 by it’s segment_id.

# In[7]:


segments = {s["segment_id"]: {**s, "flight_id": flight["flight_id"]}
             for platform in meta.values()
             for flight in platform.values()
             for s in flight["segments"]
            }
seg = segments["HALO-0205_c2"]


# We transfer the information from our flight segment selection to our radar and radiometer data in the xarray dataset.

# In[8]:


ds_smart_selection = ds_smart.sel(time=slice(seg["start"], seg["end"]))


# ## Plots

# We plot the spectral irradiances from different wavelengths measured with SMART during the selected flight segment.

# In[9]:


mpl.rcParams['font.size'] = 12

fig, ax = plt.subplots()
wl_list=[422,532,648,858,1238,1638]
for i in wl_list:
    ds_smart_selection[f'F_down_solar_wl_{i}'].plot(label =f'{i} nm')
ax.legend()
ax.set_ylabel('Spectral downward irradiance / Wm$^{-2}$nm$^{-1}$')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

