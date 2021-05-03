#!/usr/bin/env python
# coding: utf-8

# # Show the intake catalog
# 
# The eurec4a intake catalog is maintained on github at [eurec4a/eurec4a-intake](https://github.com/eurec4a/eurec4a-intake). The structure of the files however does not represent the structure of the catalog. In order to get a quick overview about its contents, here's a little script which prints out the current catalog tree.

# In[1]:


import eurec4a


# In[2]:


cat = eurec4a.get_intake_catalog()


# In[3]:


def tree(cat, level=0):
    prefix = " " * (3*level)
    try:
        for child in list(cat):
            parameters = [p["name"] for p in cat[child].describe().get("user_parameters", [])]
            if len(parameters) > 0:
                parameter_str = " (" + ", ".join(parameters) + ")"
            else:
                parameter_str = ""
            print(prefix + str(child) + parameter_str)
            tree(cat[child], level+1)
    except:
        pass


# In[4]:


tree(cat)


# There's also a graphical user interface (GUI) implemented in intake. The GUI additionally requires the `panel` python package and it interactively queries the catalog, so it doesn't work nicely in a book. This is why the following lines of code are commented out, but they can be used in an interactive notebook.

# In[5]:


#import intake
#intake.gui.add(cat)
#intake.gui.panel

