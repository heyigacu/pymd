import pandas as pd
import subprocess
import os
from itertools import combinations
import numpy as np

def read_first_column(filename):
    return pd.read_csv(filename, delimiter=' ', usecols=[0], header=None).squeeze()


def twofile_to_onefile(file1, file2, output_file):
    col1_file1 = read_first_column(file1)
    col1_file2 = read_first_column(file2)
    merged_columns = pd.concat([col1_file1, col1_file2], axis=1, ignore_index=True)
    merged_columns.to_csv(output_file, sep=' ', index=False, header=False)



def process_gamd_log(input_file, output_file, temperature, frame=1000):
    """
    Process the gamd.log file to compute values and save to output_file.
    Removes the first three lines of headers from the input file before processing.

    Parameters:
    input_file (str): Path to the input file (e.g., 'gamd.log').
    output_file (str): Path to the output file (e.g., 'weights.log').
    temperature (float): Temperature value to be used in the calculations.
    """
    
    # Remove the first three lines from the input file
    temp_file = 'temp_gamd.log'
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    # Write the data without the first three lines to a temporary file
    with open(temp_file, 'w') as outfile:
        outfile.writelines(lines[3:(3+frame)])
    
    # Read the temporary file without headers
    data = pd.read_csv(temp_file, delim_whitespace=True, header=None)
    
    # Extract the required columns (7th, 8th, and 2nd columns)
    col7 = data[6]  # 7th column
    col8 = data[7]  # 8th column
    col2 = data[1]  # 2nd column
    
    # Perform calculations
    result = (col7 + col8) / (0.001987 * temperature)
    
    # Create output DataFrame
    output = pd.DataFrame({
        'Result': result,
        'Col2': col2,
        'Sum': col7 + col8
    })
    
    # Save to the output file
    output.to_csv(output_file, sep=' ', index=False, header=False)


def extract_second_column(input_file, output_file):
    """
    Extracts the second column from the input file and saves it to the output file, excluding the header.

    Parameters:
    input_file (str): Path to the input file.
    output_file (str): Path to the output file.
    """
    # Read the input file, skipping the header
    df = pd.read_csv(input_file, delim_whitespace=True, header=0)
    
    # Extract the second column (index 1)
    second_column = df[df.columns[1]]
    
    # Save the second column to the output file
    second_column.to_csv(output_file, index=False, header=False)



def run_shell_scripts(Emax, cutoff, binx, biny, binz, data_1ds, data_2ds, data_3ds, T):
    # Get the current working directory
    workdir = os.getcwd()
    
    # Define the paths to the shell scripts
    reweight_1d_script = './reweight-1d.sh'
    reweight_2d_script = './reweight-2d.sh'
    reweight_3d_script = './reweight-3d.sh'
    
    # Run the reweight-1d.sh script
    for data_1d in data_1ds:
        subprocess.run([reweight_1d_script, str(Emax), str(cutoff), str(binx), data_1d, str(T)],
                    cwd=workdir, check=True)
    
    # Run the reweight-2d.sh script
    for data_2d in data_2ds:
        subprocess.run([reweight_2d_script, str(Emax), str(cutoff), str(binx), str(biny), data_2d, str(T)],
                    cwd=workdir, check=True)
    
    # Run the reweight-3d.sh script
    for data_3d in data_3ds:
        subprocess.run([reweight_3d_script, str(Emax), str(cutoff), str(binx), str(biny), str(binz), data_3d, str(T)],
                    cwd=workdir, check=True)





def generate_combinations(elements):
    """
    Generate all unique pairs (combinations of 2) from the given list of elements.

    Parameters:
    elements (list): A list of elements to generate pairs from.

    Returns:
    list: A list of tuples, where each tuple is a unique pair of elements.
    """
    # Generate all combinations of 2 elements
    pairs = list(combinations(elements, 2))
    
    return pairs


def pmf2frame(input_2d_path='rmsdrg.dat', pmf_path='pmf.dat', extract_coordinate_path='extract_coordinate.txt', extract_frame_in_path='extract_frame.in', interval=1):
    file1 = pd.read_csv(input_2d_path,sep='\s+',header=0)
    file1.columns = ['A','B']
    file2 = pd.read_csv(pmf_path, header=None, sep='\s+')
    file2.columns = ['X','Y','Z']

    def find_top(top):
        top_min_indices = file2['Z'].nsmallest(top).index
        top_min_values = file2.loc[top_min_indices, ['X', 'Y']].values
        return top_min_values
    
    def find_0():
        top_min_indices = file2[file2['Z']==0].index
        top_min_values = file2.loc[top_min_indices, ['X', 'Y']].values
        return top_min_values

    matching_indices = []
    for value in find_0():
        x, y = value
        distances = np.sqrt((file1['A'] - x) ** 2 + (file1['B'] - y) ** 2)
        min_index = distances.idxmin()
        matching_indices.append(min_index)

    top_min_values = find_0()
    print(top_min_values)
    print(file1.iloc[matching_indices,:])
    print("Matching indices in file1 for the smallest three values in file2:", matching_indices)

    with open(extract_coordinate_path,'w') as f:
        f.write('Frame\tX\tY\tZ\n')
        for i,index in enumerate(matching_indices):
            f.write('{}\t{}\t{}\t{}\n'.format(index+1,top_min_values[i][0],top_min_values[i][1],0))

    with open(extract_frame_in_path,'w') as f:
        f.write('parm nowat.prmtop\n')
        for index in  matching_indices:
            f.write('trajin nowat.dcd {} {}\ntrajout frame_{}.pdb pdb\nrun\nclear trajin\n'.format((index+1)*interval,(index+1)*interval,(index+1)*interval))
        f.write('quit\n')

# Example usage
if __name__ == "__main__":
    input_file = 'gamd.log'
    output_file = 'weights.dat'
    Emax = 60
    cutoff = 10
    binx = 0.1
    biny = 0.1
    binz = 0.1
    T = 310
    process_gamd_log(input_file, output_file, T, frame=5000)
    searched = True
    if searched:
        searched_fileds = ['rmsd', 'rg']
        searched_1d = []
        for filed in searched_fileds:
            extract_second_column(filed+'.dat', filed+'_.dat')
            searched_1d.append(filed+'_.dat')
        pairs = generate_combinations(searched_fileds)
        searched_2d = []
        for pair in pairs:
            filed1, filed2 = pair
            twofile_to_onefile(f'{filed1}_.dat',f'{filed2}_.dat',f'{filed1}{filed2}.dat')
            searched_2d.append(f'{filed1}{filed2}.dat')
        data_1ds = searched_1d
        data_2ds = searched_2d
        data_3ds = []
        run_shell_scripts(Emax, cutoff, binx, biny, binz, data_1ds, data_2ds, data_3ds, T)

    else:
        data_1ds = ['rmsd_.dat']
        data_2ds = ['rmsdrg.dat']
        data_3ds = []        
        run_shell_scripts(Emax, cutoff, binx, biny, binz, data_1ds, data_2ds, data_3ds, T)
        

