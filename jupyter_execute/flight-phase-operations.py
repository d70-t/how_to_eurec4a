#!/usr/bin/env python
# coding: utf-8

# # How to work with flight phase segmentation files

# In[1]:


import datetime
import eurec4a


# In[2]:


meta = eurec4a.get_flight_segments()
meta.keys()


# ## 1. map `segment_id`s to `segment`s
# This can be useful for further queries based on specific segment properties.
# In addition to the original properties in each `segment`, the `platform_id` and `flight_id` are also stored.

# In[3]:


segments = [{**s,
             "platform_id": platform_id,
             "flight_id": flight_id
            }
            for platform_id, flights in meta.items()
            for flight_id, flight in flights.items()
            for s in flight["segments"]
           ]


# In[4]:


segments_by_segment_id = {s["segment_id"]: s for s in segments}


# ## 2. list `flight_id`s

# In[5]:


flight_ids = [flight_id
              for platform_id, flights in meta.items()
              for flight_id, flight in flights.items()
              ]
flight_ids


# List `flight_id` for a specified day, here February 5

# In[6]:


flight_id = [flight_id
             for platform_id, flights in meta.items()
             for flight_id, flight in flights.items()
             if flight["date"] == datetime.date(2020,2,5)
             ]
flight_id


# ## 3. list flight segmentation `kinds`
# A segment is an object which includes at minimum a `segment_id`, `name`, `start` and `end` time.

# In[7]:


kinds = set(k for s in segments for k in s["kinds"])
kinds


# ## 4. List of common properties in all `segments`

# In[8]:


set.intersection(*(set(s.keys()) for s in segments))


# In[9]:


segment_ids_by_kind = {kind: [segment["segment_id"]
                              for segment in segments
                              if kind in segment["kinds"]]
    for kind in kinds
}


# ## 5. Further random examples:
# * total number of all circles flown during EUREC4A / ATOMIC

# In[10]:


len(segment_ids_by_kind["circle"])


# * How much time did HALO and P3 spend circling?

# In[11]:


circling_time = sum([s["end"] - s["start"]
                     for s in segments
                     if "circling" in s["kinds"]
                    ], datetime.timedelta())
circling_time


# * get `segment_id` for all circles on a given day sorted by the start time, here February 5

# In[12]:


segments_ordered_by_start_time = list(sorted(segments, key=lambda s: s["start"]))


# In[13]:


circles_Feb05 = [s["segment_id"]
                 for s in segments_ordered_by_start_time
                 if "circle" in s["kinds"]
                 and s["start"].date() == datetime.date(2020,2,5)
                 and s["platform_id"] == "HALO"
                ]
circles_Feb05


# * select all `dropsondes` with the quality flag `GOOD` from the first circle on February 5.

# In[14]:


circles_Feb05[0]


# In[15]:


segments_by_segment_id[circles_Feb05[0]]["dropsondes"]["GOOD"]

