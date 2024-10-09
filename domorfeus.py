from morfeus import BuriedVolume, read_xyz 
import os
import glob
import pandas as pd

compounds = []
above_ring = []
below_ring = []
above_minus_below = []

# Define the action you want to perform on each XYZ file
def process_xyz_file(file_path):
    # Replace this with your actual action
    #print(f"Processing {file_path}")
    elements,coordinates = read_xyz(file_path)
    bv = BuriedVolume(elements, coordinates, 13, z_axis_atoms=[76], excluded_atoms=[1,2,3,4,5,6,16,31,32,17,18,19,20,22,24,27]) #CHANGE THIS FOR EACH FILE
    bv.octant_analysis()
    sum_first_4_items = sum(value for key, value in bv.octants['percent_buried_volume'].items() if key in (0, 1, 3, 2))
    sum_last_4_items = sum(value for key, value in bv.octants['percent_buried_volume'].items() if key in (7, 6, 4, 5))
    
    compounds.append(file_path)
    above_ring.append(sum_last_4_items)
    below_ring.append(sum_first_4_items)
    difference_of = sum_last_4_items - sum_first_4_items
    #print("Difference: "+str(difference_of))
    above_minus_below.append(difference_of)
    
    #print("compound: "+str(file_path)+"\nbelow ring: "+ str(sum_first_4_items) + "\nabove ring: "+ str(sum_last_4_items)) 

# Get a list of all XYZ files in the current directory
xyz_files = glob.glob("*.xyz")

# Check if there are any XYZ files
if not xyz_files:
    print("No XYZ files found in the current directory.")
else:
    # Iterate through the XYZ files and perform the action
    print("DID YOU CHANGE YOUR INDEXES????")
    for file_path in xyz_files:
        process_xyz_file(file_path)
    
    
    data = {
        "Compund": compounds,
        "vbur_above": above_ring,
        "vbur_below": below_ring,
        "vbur_above_minus_below": above_minus_below
    }
    # Create a Pandas DataFrame from the dictionary
    df = pd.DataFrame(data)
    # Save the DataFrame to an Excel file
    output_file = "output.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Data written to {output_file}")
    
    average_amb = sum(above_minus_below) / len(above_minus_below)
    
    print("Summary (top-bottom):")
    print("vbur_min: " + str(min(above_minus_below)))
    print("vbur_max: " + str(max(above_minus_below)))
    print("vbur_avg: " + str(average_amb))
    