#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import the goods
import geopandas as gpd
from datetime import datetime

# load the shapefile
shapefile_path = R"your\path\here\mudslide_working.shp"
gdf = gpd.read_file(shapefile_path)

# function to convert date format from text
def reformat_date(date_str):
    try:
        # strip any surrounding whitespace and parse the date string (helpful)
        date_obj = datetime.strptime(date_str.strip(), '%m/%d/%Y')
        # format to 'Month day, year'
        return date_obj.strftime('%B %d, %Y')
    except (ValueError, AttributeError):
        # return the original string if it’s not a valid date format or is NULL
        return date_str

# apply the date reformatting function to the 'start_date' field
gdf['start_date'] = gdf['start_date'].apply(reformat_date)

# save the changes back to a new shapefile with the specified name
output_shapefile_path = 'mudslide_date_fix.shp'
gdf.to_file(R"your\path\here\mudslide_date_fix.shp")

print("Date format updated and saved to 'mudslide_date_fix.shp'.")

