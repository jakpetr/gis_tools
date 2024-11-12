#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import random

def sample_csv_files(folder_path, sample_size=200, output_file="sampled_combined.csv"):
    # list to pull 'sample' data
    sampled_data = []
    
    # loop over each csv file in a specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            # read the csv files
            try:
                df = pd.read_csv(file_path)
                
                # check if the file has more rows than the sample size(s)
                if len(df) > sample_size:
                    sampled_df = df.sample(n=sample_size, random_state=1)  # random sample with a fixed seed
                else:
                    sampled_df = df  # if not enough rows, take all rows (shouldn't be an issue here)
                
                # append the sampled data with a new column for file identification (state)
                sampled_df['source_file'] = filename
                sampled_data.append(sampled_df)
            
            except Exception as e:
                print(f"Could not process file {filename}: {e}")
    
    # concatenate all sampled data into a single df
    combined_df = pd.concat(sampled_data, ignore_index=True)
    
    # save to the output csv file
    combined_df.to_csv(output_file, index=False)
    print(f"Sampled data saved to {output_file}")

# use the function
folder_path = R"D:\jake_gwre\gwre\address"  # replace with the path to specified folder
sample_csv_files(folder_path)


# In[2]:


import os
import pandas as pd

def sample_csv_files_to_excel(folder_path, sample_size=200, output_file="sampled_combined.xlsx"):
    # List to hold sampled data from each file
    sampled_data = []
    
    # Loop over each CSV file in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            # Read the CSV file
            try:
                df = pd.read_csv(file_path)
                
                # Check if the file has more rows than the sample size
                if len(df) > sample_size:
                    sampled_df = df.sample(n=sample_size, random_state=1)  # Random sample with a fixed seed
                else:
                    sampled_df = df  # If not enough rows, take all
                
                # Append the sampled data with a new column for file identification
                sampled_df['source_file'] = filename
                sampled_data.append(sampled_df)
            
            except Exception as e:
                print(f"Could not process file {filename}: {e}")
    
    # Concatenate all sampled data into a single DataFrame
    combined_df = pd.concat(sampled_data, ignore_index=True)
    
    # Save to the output Excel file
    with pd.ExcelWriter(output_file) as writer:
        combined_df.to_excel(writer, index=False, sheet_name="Sampled Data")
    
    print(f"Sampled data saved to {output_file}")

# Use the function
folder_path = R"D:\jake_gwre\gwre\address"  # Replace with the path to your folder
sample_csv_files_to_excel(folder_path)


# In[3]:


pip install openpyxl


# In[4]:


import os
import pandas as pd

def sample_csv_files_to_excel(folder_path, sample_size=200, output_file="sampled_combined.xlsx"):
    # List to hold sampled data from each file
    sampled_data = []
    
    # Loop over each CSV file in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            # Read the CSV file
            try:
                df = pd.read_csv(file_path)
                
                # Check if the file has more rows than the sample size
                if len(df) > sample_size:
                    sampled_df = df.sample(n=sample_size, random_state=1)  # Random sample with a fixed seed
                else:
                    sampled_df = df  # If not enough rows, take all
                
                # Append the sampled data with a new column for file identification
                sampled_df['source_file'] = filename
                sampled_data.append(sampled_df)
            
            except Exception as e:
                print(f"Could not process file {filename}: {e}")
    
    # Concatenate all sampled data into a single DataFrame
    combined_df = pd.concat(sampled_data, ignore_index=True)
    
    # Save to the output Excel file
    with pd.ExcelWriter(output_file) as writer:
        combined_df.to_excel(writer, index=False, sheet_name="Sampled Data")
    
    print(f"Sampled data saved to {output_file}")

# Use the function
folder_path = R"D:\jake_gwre\gwre\address"  # Replace with the path to your folder
sample_csv_files_to_excel(folder_path)


# In[5]:


import os
import geopandas as gpd
import pandas as pd

def sample_geopackage_files(folder_path, output_folder, sample_size=100):
    # ensure output folder exists (specified folder in a place with enough storage)
    os.makedirs(output_folder, exist_ok=True)
    
    # loop over each gpkg file in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".gpkg"):
            file_path = os.path.join(folder_path, filename)
            
            # read the geopackage file
            try:
                gdf = gpd.read_file(file_path)
                
                # filter rows with 'COMMERCIAL_PROP_PTS' >= 1 and 'RESIDENTIAL_PROP_PTS' >= 1
                commercial_sample = gdf[gdf['COMMERCIAL_PROP_PTS'] >= 1].sample(n=min(sample_size, len(gdf)), random_state=1)
                residential_sample = gdf[gdf['RESIDENTIAL_PROP_PTS'] >= 1].sample(n=min(sample_size, len(gdf)), random_state=1)
                
                # combine both samples and reset index (spatial?)
                combined_sample = pd.concat([commercial_sample, residential_sample], ignore_index=True)
                
                # define output excel file path (excel because csv will delmit prematurely)
                excel_output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_sampled.xlsx")
                
                # export to excel file
                with pd.ExcelWriter(excel_output_path) as writer:
                    combined_sample.to_excel(writer, index=False, sheet_name="Sampled Data")
                
                print(f"Sampled data saved to {excel_output_path}")
            
            except Exception as e:
                print(f"Could not process file {filename}: {e}")

def combine_excel_files(output_folder, final_output_file="combined_sampled_data.xlsx"):
    # list to hold data from each excel file
    combined_data = []
    
    # loop over each excel file in the specified output folder
    for filename in os.listdir(output_folder):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(output_folder, filename)
            
            # read the excel file
            df = pd.read_excel(file_path)
            df['source_file'] = filename  # Add column to track source
            combined_data.append(df)
    
    # concatenate all data into a single df
    final_combined_df = pd.concat(combined_data, ignore_index=True)
    
    # export final combined df to excel file
    final_combined_df.to_excel(final_output_file, index=False)
    print(f"Final combined data saved to {final_output_file}")

# define folder paths
folder_path = R"D:\jake_gwre\gwre\address\gpkgs"  # replace with specified folder path
output_folder = R"D:\jake_gwre\gwre\address\excel_files"  # replace with specified output folder for excel files

# run the functions
sample_geopackage_files(folder_path, output_folder)
combine_excel_files(output_folder)


# In[ ]:




