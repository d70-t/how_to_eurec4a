#!/usr/bin/env python
# coding: utf-8

# # Reading cloud radar data
# The high resolution data has about 500 MB per file, which when read in over a remote source can lead to long wait times.
# To reduce the wait times the data can be read in lazily using dask.
# Intake will this do this by default.
# Let's obtain the EUREC4A intake catalog:

# In[1]:


import eurec4a
cat = eurec4a.get_intake_catalog()


# ## Available products
# The `LIMRAD94` cloud radar offers multiple products which can be accessed using names and additional parameters.
# Let's see which products and parameters are available for the cloud radar.
# For the parameters, we are also interested in their valid range:

# In[2]:


for key, source in cat.Meteor.LIMRAD94.items():
    desc = source.describe()
    user_parameters = desc.get("user_parameters", [])
    if len(user_parameters) > 0:
        params = " (" + ", ".join(p["name"] for p in user_parameters) + ")"
    else:
        params = ""
    print(f"{key}{params}: {desc['description']}")
    for parameter in user_parameters:
        print(f"    {parameter['name']}: {parameter['min']} ... {parameter['max']} default: {parameter['default']}")
    print()


# ## Radar reflectivity
# We'll have a look at the `high_res` data in version 1.1. We'll keep the default date for simplicity:

# In[3]:


ds = cat.Meteor.LIMRAD94.high_res(version=1.1).to_dask()
ds


# Explore the dataset and choose the variable you want to work with.
# The variables are loaded lazily, i.e. only when their content is really required to complete the operation.
# An example which forces the data to load is plotting, in this case only the radar reflectivity will be loaded.

# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
ds.Zh.plot(x='time', cmap="Spectral_r")  # plot the variable with time as the x axis
plt.ylim(0, 3000)

