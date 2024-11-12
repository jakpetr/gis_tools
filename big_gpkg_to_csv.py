# import the goods
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




